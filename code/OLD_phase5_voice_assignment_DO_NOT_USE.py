import argparse
import pandas as pd

# ---- 1) Mapping: cluster -> topic label ----
cluster_topic_map = {
    0: "Journalism & AI Disruption",
    1: "AI Creativity & Copyright",
    2: "General University Content",
    3: "Law & Governance Discourse",
    4: "Innovation & Entrepreneurship Ecosystem",
    5: "AI & Future Work",
    6: "AI in Healthcare",
    7: "LLM Ethics & Risk",
    8: "Academic Integrity & GenAI",
    9: "GenAI in Peer Review",
    10: "AI & Assessment Values",
    11: "AI Research Leadership",
    12: "AI Societal Impact",
    13: "AI Governance & Strategy",
}

# ---- 2) Mapping: cluster -> narrative voice ----
cluster_voice_map = {
    0: "Marketing",
    1: "Risk",
    2: "Admin",
    3: "Admin",
    4: "Innovator",
    5: "Risk",
    6: "Innovator",
    7: "Risk",
    8: "Pedagogical",
    9: "Admin",
    10: "Pedagogical",
    11: "Innovator",
    12: "Risk",
    13: "Admin",
}

def main():
    parser = argparse.ArgumentParser(
        description="Assign topic labels + narrative voices to semantic clusters."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Input semantic CSV (e.g. data/semantic/hype_top50_semantic.csv)",
    )
    parser.add_argument(
        "--output",
        required=True,
        help="Output CSV with topic_label + voice columns",
    )
    args = parser.parse_args()

    print(f"[INFO] Loading {args.input} ...")
    df = pd.read_csv(args.input)

    if "cluster_id" not in df.columns:
        raise ValueError("Input file must contain 'cluster_id' column.")

    # Add topic label + voice
    df["topic_label"] = df["cluster_id"].map(cluster_topic_map)
    df["voice"] = df["cluster_id"].map(cluster_voice_map)

    df.to_csv(args.output, index=False)
    print(f"[INFO] Saved with topic_label + voice → {args.output}")

    # Voice counts + percentages
    counts = df["voice"].value_counts()
    perc = df["voice"].value_counts(normalize=True) * 100

    print("\nVoice Distribution (counts):")
    print(counts)

    print("\nVoice Distribution (%):")
    print(perc.round(2))


if __name__ == "__main__":
    main()