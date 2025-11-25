import os
import pandas as pd
import matplotlib.pyplot as plt

FILES = [
    "data/semantic/hype_top50_semantic.csv",
    "data/semantic/hype_ge1000_semantic.csv",
    "data/semantic/control_top50_semantic.csv",
    "data/semantic/control_ge1000_semantic.csv",
]

OUT_DIR = "visuals"


def ensure_outdir():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)


def plot_umap(file_path):
    df = pd.read_csv(file_path)

    name = os.path.basename(file_path).replace("_semantic.csv", "")

    if not {"umap_x", "umap_y", "cluster_id"}.issubset(df.columns):
        print(f"[SKIP] {file_path} missing UMAP columns")
        return

    plt.figure(figsize=(6, 5))
    plt.scatter(df["umap_x"], df["umap_y"], c=df["cluster_id"], s=12)
    plt.title(f"UMAP Semantic Map – {name}")
    plt.xlabel("UMAP-1")
    plt.ylabel("UMAP-2")

    out_path = os.path.join(OUT_DIR, f"umap_{name}.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()

    print(f"[INFO] Saved UMAP → {out_path}")


def main():
    ensure_outdir()
    for file in FILES:
        plot_umap(file)

    print("\n✅ All UMAP Semantic Maps generated.")


if __name__ == "__main__":
    main()