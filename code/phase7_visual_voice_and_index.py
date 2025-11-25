import os
import pandas as pd
import matplotlib.pyplot as plt

INPUT = "data/semantic/ai_positioning_index.csv"
OUT_DIR = "visuals"


def ensure_outdir():
    if not os.path.exists(OUT_DIR):
        os.makedirs(OUT_DIR)


def plot_voice_distribution(df):
    """
    For each dataset (row), create a bar chart of the 5 GANIS voices.
    Uses the percentages already stored in ai_positioning_index.csv.
    """
    voices = ["Innovator", "Risk", "Admin", "Pedagogical", "Marketing"]

    for dataset, row in df.iterrows():
        values = [row.get(v, 0.0) for v in voices]

        plt.figure()
        plt.bar(voices, values)
        plt.ylabel("Percentage of documents")
        plt.ylim(0, 100)
        plt.title(f"Voice Distribution – {dataset}")

        out_path = os.path.join(OUT_DIR, f"voice_distribution_{dataset}.png")
        plt.tight_layout()
        plt.savefig(out_path, dpi=200)
        plt.close()
        print(f"[INFO] Saved voice distribution plot → {out_path}")


def plot_ai_positioning_scores(df):
    """
    Bar chart of AI Optimism Index per dataset.
    (Promotion vs Governance / Risk)
    """
    plt.figure()
    datasets = df.index.tolist()
    # 🔁 Updated to use the new metric name from phase6
    scores = df["AI_Optimism_Index"].tolist()

    plt.bar(datasets, scores)
    plt.ylabel("AI Optimism Index")
    plt.title("AI Optimism Index by Dataset")
    plt.xticks(rotation=15)

    out_path = os.path.join(OUT_DIR, "ai_optimism_index.png")
    plt.tight_layout()
    plt.savefig(out_path, dpi=200)
    plt.close()
    print(f"[INFO] Saved AI Optimism Index plot → {out_path}")

def main():
    ensure_outdir()

    print(f"[INFO] Loading {INPUT} ...")
    df = pd.read_csv(INPUT, index_col="dataset")

    # 1) Voice distribution per dataset
    plot_voice_distribution(df)

    # 2) AI Positioning Score comparison
    plot_ai_positioning_scores(df)

    print("\n[DONE] Phase 7 visuals (voice + index) generated.")


if __name__ == "__main__":
    main()