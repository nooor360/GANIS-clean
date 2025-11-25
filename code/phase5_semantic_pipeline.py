import argparse
from pathlib import Path

import pandas as pd
from sentence_transformers import SentenceTransformer
import umap.umap_ as umap
import hdbscan


def build_text_field(row):
    """
    Build the text we embed: Title + content_text.
    Falls back gracefully if columns are missing.
    """
    title = str(row.get("Title", "") or "")
    body = str(row.get("content_text", "") or "")
    text = (title.strip() + "\n\n" + body.strip()).strip()
    return text


def main(args):
    input_path = Path(args.input)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Loading dataset from {input_path} ...")
    df = pd.read_csv(input_path)
    print(f"[INFO] Loaded {len(df)} rows.")

    # Build text field for embedding
    print("[INFO] Building text_for_embedding field (Title + content_text) ...")
    df["text_for_embedding"] = df.apply(build_text_field, axis=1)

    # Basic length filter so we don't embed tiny boilerplate
    df["word_count_calc"] = df["text_for_embedding"].str.split().str.len()
    before_filter = len(df)
    df = df[df["word_count_calc"] >= args.min_words].reset_index(drop=True)
    print(f"[INFO] Filtered by min_words={args.min_words}: {before_filter} -> {len(df)} rows.")

    if len(df) == 0:
        print("[WARN] No rows left after filtering. Exiting.")
        return

    # Load Sentence Transformer model
    print(f"[INFO] Loading SentenceTransformer model: {args.model_name} ...")
    model = SentenceTransformer(args.model_name)

    texts = df["text_for_embedding"].tolist()
    print(f"[INFO] Encoding {len(texts)} documents to embeddings ...")
    embeddings = model.encode(
        texts,
        batch_size=args.batch_size,
        show_progress_bar=True
    )

    # UMAP dimensionality reduction (to 2D for visualization)
    print("[INFO] Running UMAP dimensionality reduction ...")
    reducer = umap.UMAP(
        n_components=2,
        n_neighbors=args.n_neighbors,
        min_dist=0.1,
        metric="cosine",
        random_state=42,
    )
    emb_2d = reducer.fit_transform(embeddings)

    # HDBSCAN clustering on the 2D projections
    print("[INFO] Running HDBSCAN clustering ...")
    clusterer = hdbscan.HDBSCAN(
        min_cluster_size=args.min_cluster_size,
        min_samples=args.min_samples,
        metric="euclidean",
        cluster_selection_method="eom",
    )
    cluster_labels = clusterer.fit_predict(emb_2d)

    df["umap_x"] = emb_2d[:, 0]
    df["umap_y"] = emb_2d[:, 1]
    df["cluster_id"] = cluster_labels

    print("\n=== Cluster label counts (including -1 noise) ===")
    print(df["cluster_id"].value_counts().sort_index())

    # Save semantic CSV (for plotting later)
    out_csv = output_dir / f"{args.output_prefix}_semantic.csv"
    df.to_csv(out_csv, index=False)
    print(f"\n[INFO] Saved semantic CSV to: {out_csv}")

    # Prepare cluster samples file for LLM topic labeling
    samples_path = output_dir / f"{args.output_prefix}_cluster_samples.txt"
    print(f"[INFO] Writing cluster samples for LLM to: {samples_path}")

    with open(samples_path, "w", encoding="utf-8") as f:
        for cid in sorted(df["cluster_id"].unique()):
            if cid == -1:
                cname = "NOISE / MISC (-1)"
            else:
                cname = f"Cluster {cid}"

            sub = (
                df[df["cluster_id"] == cid]
                .sort_values("word_count_calc", ascending=False)
                .head(args.samples_per_cluster)
            )

            f.write(f"==== {cname} (n={len(sub)}) ====\n")

            for _, row in sub.iterrows():
                uni = str(row.get("the_name", ""))
                title = str(row.get("Title", "")).strip()
                f.write(f"\n--- DOC: {uni} | {title[:140]}\n")

                body = str(row.get("content_text", "") or "")
                words = body.split()
                snippet = " ".join(words[: args.words_per_snippet])
                f.write(snippet + "\n")

            f.write("\n\n")

    print("[DONE] Phase 4 semantic pipeline complete for this file.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input",
        required=True,
        help="Path to input CSV (e.g. data/ganis_hype_top50.csv)",
    )
    parser.add_argument(
        "--output_prefix",
        required=True,
        help="Prefix for output files (e.g. hype_top50)",
    )
    parser.add_argument(
        "--output_dir",
        default="data/semantic",
        help="Directory to save outputs (default: data/semantic)",
    )

    # Model & embedding options
    parser.add_argument(
        "--model_name",
        default="all-MiniLM-L6-v2",
        help="SentenceTransformer model (default: all-MiniLM-L6-v2)",
    )
    parser.add_argument(
        "--batch_size",
        type=int,
        default=16,
        help="Batch size for embedding (default: 16)",
    )

    # Filters / clustering hyperparameters
    parser.add_argument(
        "--min_words",
        type=int,
        default=30,
        help="Minimum words in text_for_embedding to keep a doc (default: 30)",
    )
    parser.add_argument(
        "--n_neighbors",
        type=int,
        default=15,
        help="UMAP n_neighbors (default: 15)",
    )
    parser.add_argument(
        "--min_cluster_size",
        type=int,
        default=10,
        help="HDBSCAN min_cluster_size (default: 10)",
    )
    parser.add_argument(
        "--min_samples",
        type=int,
        default=5,
        help="HDBSCAN min_samples (default: 5)",
    )

    # LLM sample settings
    parser.add_argument(
        "--samples_per_cluster",
        type=int,
        default=5,
        help="Number of docs per cluster to export for LLM (default: 5)",
    )
    parser.add_argument(
        "--words_per_snippet",
        type=int,
        default=120,
        help="Words per doc snippet in LLM file (default: 120)",
    )

    args = parser.parse_args()
    main(args)