import argparse
import os
import pandas as pd

# 1) Per-file: cluster_id -> topic label

CLUSTER_TOPIC_LABELS = {
    # HYPE – Top 50 (already fully defined)
    "hype_top50": {
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
    },

    # HYPE – Rank ≥ 1000
    "hype_ge1000": {
        0: "Law & Degree Content",
        1: "Student Life & Opportunities",
    },

    # CONTROL – Top 50
    "control_top50": {
        0: "Postgraduate Law Programmes",
        1: "AI Guidance & Infrastructure",
    },

    # CONTROL – Rank ≥ 1000
    "control_ge1000": {
        0: "Campus Operations & Sustainability",
        1: "Student Administration & Access",
        2: "Law Education Pathways",
    },
}

# -----------------------------
# 2) Per-file: cluster_id → GANIS Voice
# -----------------------------

CLUSTER_VOICES = {
    # HYPE – Top 50 (your main narrative clusters)
    "hype_top50": {
        0: "Marketing",     # Journalism & AI Disruption
        1: "Risk",          # AI Creativity & Copyright
        2: "Admin",         # General University Content (noise)
        3: "Admin",         # Law & Governance Discourse
        4: "Innovator",     # Innovation & Entrepreneurship Ecosystem
        5: "Risk",          # AI & Future Work
        6: "Innovator",     # AI in Healthcare
        7: "Risk",          # LLM Ethics & Risk
        8: "Pedagogical",   # Academic Integrity & GenAI
        9: "Admin",         # GenAI in Peer Review
        10: "Pedagogical",  # AI & Assessment Values
        11: "Innovator",    # AI Research Leadership
        12: "Risk",         # AI Societal Impact
        13: "Admin",        # AI Governance & Strategy
        -1: "Admin"  
    },

    # HYPE – Rank ≥ 1000
    "hype_ge1000": {
        0: "Admin",      # Law & Degree Content
        1: "Marketing",  # Student Life & Opportunities
    },

    # CONTROL – Top 50
    "control_top50": {
        0: "Admin",        # Postgraduate Law Programmes
        1: "Pedagogical",  # AI Guidance & Infrastructure
    },

    # CONTROL – Rank ≥ 1000
    "control_ge1000": {
        0: "Admin",  # Campus Operations & Sustainability
        1: "Admin",  # Student Administration & Access
        2: "Admin",  # Law Education Pathways
    },
}


def detect_prefix(input_path: str) -> str:
    """
    Infer prefix from filename:
    e.g. hype_top50_semantic.csv → hype_top50
    """
    base = os.path.basename(input_path)
    if base.endswith("_semantic.csv"):
        return base.replace("_semantic.csv", "")
    # fallback: strip extension
    return os.path.splitext(base)[0]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True,
                        help="Path to *_semantic.csv")
    parser.add_argument("--output", required=True,
                        help="Where to save *_with_voice.csv")
    args = parser.parse_args()

    prefix = detect_prefix(args.input)
    if prefix not in CLUSTER_VOICES:
        raise ValueError(
            f"Unknown prefix '{prefix}'. "
            f"Add it to CLUSTER_VOICES and CLUSTER_TOPIC_LABELS."
        )

    topic_map = CLUSTER_TOPIC_LABELS.get(prefix, {})
    voice_map = CLUSTER_VOICES[prefix]

    print(f"[INFO] Prefix detected: {prefix}")
    print(f"[INFO] Loading {args.input} ...")
    df = pd.read_csv(args.input)

    # Optional topic labels
    if topic_map:
        df["topic_label"] = df["cluster_id"].map(topic_map)

    # Required: GANIS voice
    df["voice"] = df["cluster_id"].map(voice_map)

    # ✅ Explicitly label any unmapped / NaN clusters as "Noise"
    df["voice"] = df["voice"].fillna("Noise")

    df.to_csv(args.output, index=False)
    print(f"[INFO] Saved with topic_label + voice → {args.output}")

    vc = df["voice"].value_counts(dropna=False)
    perc = (vc / len(df) * 100).round(2)

    print("\nVoice Distribution (counts):")
    print(vc)
    print("\nVoice Distribution (%):")
    print(perc)


if __name__ == "__main__":
    main()