import pandas as pd

DATA_PATH = "data/ganis_phase2_clean.csv"

def main():
    df = pd.read_csv(DATA_PATH)

    print("\n=== Sample rows ===")
    print(df[["the_country", "the_rank", "Labels"]].head(20))

    print("\n=== Unique countries (top 20) ===")
    print(df["the_country"].value_counts().head(20))

    print("\n=== Unique Labels (top 20) ===")
    print(df["Labels"].value_counts().head(20))


if __name__ == "__main__":
    main()