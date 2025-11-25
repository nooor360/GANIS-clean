import math
from collections import Counter

import numpy as np
import pandas as pd

# -------- CONFIG --------
RAW_DATA_PATH = "data/Final_table_results.xlsx"
OUTPUT_PATH = "data/ganis_phase2_clean.csv"

# thresholds – chosen based on std dev analysis (approx 1.5 std devs below mean)
MIN_WORDS = 50          # Increased from 30 to 50 (30 is often just a header/footer)
MIN_CHAR_ENTROPY = 4.0  # Increased from 3.5 to 4.0 (Garbage is usually < 3.8)
MIN_TTR = 0.25

# boilerplate keywords (lowercase)
BOILERPLATE_KEYWORDS = [
    "cookie", "cookies", "cookie settings", "privacy policy",
    "terms and conditions", "terms of use", "data protection",
    "javascript", "enable javascript", "consent", "gdpr",
    "all rights reserved"
]

def calculate_text_entropy(text: str) -> float:
    """
    Calculates Character-level Shannon entropy in bits.
    Low entropy (< 3.8) indicates repetitive, low-information text (garbage).
    """
    if not text or not isinstance(text, str):
        return 0.0
    counts = Counter(text)
    total = sum(counts.values())
    probs = [c / total for c in counts.values()]
    return -sum(p * math.log2(p) for p in probs)

def type_token_ratio(text: str) -> float:
    """Unique words / total words."""
    if not text or not isinstance(text, str):
        return 0.0
    tokens = [t for t in text.split() if t.isalpha() or any(ch.isalnum() for ch in t)]
    if not tokens:
        return 0.0
    types = set(tokens)
    return len(types) / len(tokens)


def contains_boilerplate(row) -> bool:
    """Check content_text, Title, bigrams, trigrams for boilerplate phrases."""
    fields = []
    for col in ["content_text", "Title", "top_bigrams", "top_trigrams"]:
        if col in row and isinstance(row[col], str):
            fields.append(row[col].lower())
    joined = " ".join(fields)
    return any(kw in joined for kw in BOILERPLATE_KEYWORDS)


# -------- MAIN PIPELINE --------
def main():
    print("Loading data...")
    try:
        df = pd.read_excel(RAW_DATA_PATH)
    except FileNotFoundError:
        print(f"ERROR: Could not find {RAW_DATA_PATH}. Please check your data folder.")
        return

    # keep only English pages with decent language score
    if "lang_detected" in df.columns:
        df = df[df["lang_detected"] == "en"]
    if "lang_score" in df.columns:
        df = df[df["lang_score"] >= 0.8]

    # basic null cleanup
    df = df.dropna(subset=["content_text"])

    print("Calculating text statistics (entropy, TTR)...")
    df["char_entropy"] = df["content_text"].astype(str).apply(calculate_text_entropy)
    df["ttr"] = df["content_text"].astype(str).apply(type_token_ratio)

    # use existing word count if present, otherwise compute
    if "raw_word_count" in df.columns:
        df["word_count"] = df["raw_word_count"]
    else:
        df["word_count"] = df["content_text"].astype(str).apply(
            lambda t: len(t.split())
        )

    print("-" * 40)
    print(f"Initial Dataset Size: {len(df)}")
    
    # --- SENSITIVITY ANALYSIS (The "Pro" Move) ---
    mean_ent = df["char_entropy"].mean()
    std_ent = df["char_entropy"].std()
    print(f"STATS: Mean Entropy: {mean_ent:.2f} +/- {std_ent:.2f}")
    print(f"THRESHOLD JUSTIFICATION: Setting MIN_CHAR_ENTROPY to {MIN_CHAR_ENTROPY}")
    print(f"(Targeting texts approx {(mean_ent - MIN_CHAR_ENTROPY)/std_ent:.1f} std devs below mean)")
    print("-" * 40)

    # low-information filters
    mask_words = df["word_count"] >= MIN_WORDS
    mask_entropy = df["char_entropy"] >= MIN_CHAR_ENTROPY
    mask_ttr = df["ttr"] >= MIN_TTR

    df_lowinfo_removed = df[mask_words & mask_entropy & mask_ttr]
    dropped_count = len(df) - len(df_lowinfo_removed)
    print(f"Low-Info Filter Removed: {dropped_count} rows")

    # boilerplate removal
    print("Flagging boilerplate pages...")

    # Make explicit copy to avoid SettingWithCopyWarning
    df_lowinfo_removed = df_lowinfo_removed.copy()

    df_lowinfo_removed["is_boilerplate"] = df_lowinfo_removed.apply(
        contains_boilerplate, axis=1
    )
    df_clean = df_lowinfo_removed[~df_lowinfo_removed["is_boilerplate"]]

    boilerplate_count = len(df_lowinfo_removed) - len(df_clean)
    print(f"Boilerplate Filter Removed: {boilerplate_count} rows")
    print(f"Final Clean Dataset: {len(df_clean)} rows")

    # save cleaned base dataset for later phases
    df_clean.to_csv(OUTPUT_PATH, index=False)
    print(f"Saved cleaned dataset to {OUTPUT_PATH}")

    # quick summary for you to inspect
    print(df_clean[["char_entropy", "ttr", "word_count"]].describe())


if __name__ == "__main__":
    main()