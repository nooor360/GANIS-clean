import pandas as pd
import random

DATA_PATH = "data/ganis_phase2_clean.csv"
OUTPUT_SAMPLE = "data/ganis_llm_sample.csv"

SAMPLE_SIZE = 400  # random sample for manual + AI validation

def main():
    df = pd.read_csv(DATA_PATH)

    print("Columns:", df.columns.tolist())

    # Use correct column names from your dataset
    sample_df = df.sample(SAMPLE_SIZE)

    sample_df = sample_df[[
        "the_domain",
        "the_country",
        "the_rank",
        "Labels",
        "content_text"
    ]]

    sample_df.to_csv(OUTPUT_SAMPLE, index=False)
    print(f"✅ LLM validation sample saved to {OUTPUT_SAMPLE}")
    print("Open this file and check which domains produce garbage content.")


if __name__ == "__main__":
    main()