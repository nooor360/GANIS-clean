import pandas as pd
from pathlib import Path

BASE = Path("data/semantic")

FILES = [
    ("hype_top50", BASE / "hype_top50_with_voice.csv"),
    ("hype_ge1000", BASE / "hype_ge1000_with_voice.csv"),
    ("control_top50", BASE / "control_top50_with_voice.csv"),
    ("control_ge1000", BASE / "control_ge1000_with_voice.csv"),
]

VOICES = ["Innovator", "Risk", "Admin", "Marketing", "Pedagogical"]


def main():
    rows = []

    for name, path in FILES:
        print(f"\n=== {name} ===")
        df = pd.read_csv(path)

        counts = df["voice"].value_counts()
        proportions = (counts / len(df) * 100).round(2)

        print("Counts:")
        print(counts)
        print("\nPercentages:")
        print(proportions)

        row = {"dataset": name, "n_docs": len(df)}
        for v in VOICES:
            row[f"{v}_pct"] = float(proportions.get(v, 0.0))
        rows.append(row)

    out_df = pd.DataFrame(rows)
    out_path = BASE / "voice_fingerprints_summary.csv"
    out_df.to_csv(out_path, index=False)
    print(f"\n✅ Saved voice fingerprint summary to {out_path}")


if __name__ == "__main__":
    main()