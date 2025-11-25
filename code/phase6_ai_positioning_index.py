import pandas as pd

# Where the voiced datasets live
DATASETS = {
    "hype_top50": "data/semantic/hype_top50_with_voice.csv",
    "hype_ge1000": "data/semantic/hype_ge1000_with_voice.csv",
    "control_top50": "data/semantic/control_top50_with_voice.csv",
    "control_ge1000": "data/semantic/control_ge1000_with_voice.csv",
}

# The 5 GANIS voices
ALL_VOICES = ["Innovator", "Risk", "Admin", "Pedagogical", "Marketing"]

OUTPUT = "data/semantic/ai_positioning_index.csv"


def main():
    rows = []

    for name, path in DATASETS.items():
        print(f"[INFO] Processing {name} from {path} ...")
        try:
            df = pd.read_csv(path)
        except FileNotFoundError:
            print(f"WARNING: File {path} not found. Skipping.")
            continue

        if "voice" not in df.columns:
            raise ValueError(f"'voice' column not found in {path}")

        # Percentages per voice
        vc = df["voice"].value_counts(normalize=True) * 100.0

        row = {"dataset": name}
        for v in ALL_VOICES:
            row[v] = float(vc.get(v, 0.0))  # fill 0 if voice missing

        # Governance Coherence = Admin + Pedagogical
        row["Governance_Coherence"] = row["Admin"] + row["Pedagogical"]

        # ---------------------------------------------------------
        # METRIC UPDATE: AI Optimism Index
        # Formula: (Innovator + Marketing) / (Risk + Governance + 1)
        # Reason: A Ratio avoids negative numbers and represents "Promotion vs Control"
        # The +1 in denominator prevents division by zero.
        # ---------------------------------------------------------
        
        promotion_score = row["Innovator"] + row["Marketing"]
        control_score = row["Risk"] + row["Governance_Coherence"]
        
        row["AI_Optimism_Index"] = promotion_score / (control_score + 1.0)

        rows.append(row)

    out_df = pd.DataFrame(rows).set_index("dataset")
    out_df = out_df.sort_values("AI_Optimism_Index", ascending=False)

    out_df.to_csv(OUTPUT)
    print(f"\n✅ AI Optimism Index saved to: {OUTPUT}\n")

    # Show a nice summary in terminal
    print(out_df[[
        "Innovator",
        "Risk",
        "Admin",
        "AI_Optimism_Index"
    ]])


if __name__ == "__main__":
    main()