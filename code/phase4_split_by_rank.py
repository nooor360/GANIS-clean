import pandas as pd
import os

HYPE_PATH = "data/ganis_hype_set.csv"
CONTROL_PATH = "data/ganis_control_set.csv"


def load_with_rank(path):
    df = pd.read_csv(path)
    if "the_rank" not in df.columns:
        raise ValueError(f"'the_rank' column not found in {path}")
    # make sure rank is numeric
    df["the_rank_num"] = pd.to_numeric(df["the_rank"], errors="coerce")
    return df


def split_by_rank(df, label):
    # Top 50 (rank <= 50)
    top50 = df[df["the_rank_num"] <= 50].copy()

    # Rank >= 1000
    ge1000 = df[df["the_rank_num"] >= 1000].copy()

    # For info only: middle range that we ignore in this experiment
    mid = df[(df["the_rank_num"] > 50) & (df["the_rank_num"] < 1000)].copy()

    print(f"\n=== {label} ===")
    print(f"Total rows: {len(df)}")
    print(f"  Top 50 (<= 50):       {len(top50)}")
    print(f"  Middle (51–999):      {len(mid)} (ignored for GANIS analysis)")
    print(f"  ≥ 1000:               {len(ge1000)}")

    return top50, ge1000


def main():
    print("[INFO] Loading HYPE and CONTROL sets...")
    hype = load_with_rank(HYPE_PATH)
    control = load_with_rank(CONTROL_PATH)

    hype_top50, hype_ge1000 = split_by_rank(hype, "HYPE (news/media)")
    ctrl_top50, ctrl_ge1000 = split_by_rank(control, "CONTROL (policy/admin)")

    os.makedirs("data", exist_ok=True)

    hype_top50.to_csv("data/ganis_hype_top50.csv", index=False)
    hype_ge1000.to_csv("data/ganis_hype_ge1000.csv", index=False)
    ctrl_top50.to_csv("data/ganis_control_top50.csv", index=False)
    ctrl_ge1000.to_csv("data/ganis_control_ge1000.csv", index=False)

    print("\n[INFO] Saved:")
    print("  data/ganis_hype_top50.csv")
    print("  data/ganis_hype_ge1000.csv")
    print("  data/ganis_control_top50.csv")
    print("  data/ganis_control_ge1000.csv")
    print("\n[DONE] Phase 4 rank split complete.")


if __name__ == "__main__":
    main()