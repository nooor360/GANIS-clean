import os
import pandas as pd

DATA_PATH = "data/ganis_phase2_clean.csv"
BLACKLIST_PATH = "data/domain_blacklist.txt"

OUTPUT_HYPE = "data/ganis_hype_set.csv"
OUTPUT_CONTROL = "data/ganis_control_set.csv"


def load_blacklist(path: str):
    """
    Load domain blacklist from a simple text file (one domain per line).
    Lines that are empty or start with '#' are ignored.
    """
    if not os.path.exists(path):
        print(f"[INFO] No blacklist file found at {path}. Skipping domain filtering.")
        return set()

    domains = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            if line.startswith("#"):
                continue
            domains.append(line)

    blacklist = set(domains)
    print(f"[INFO] Loaded {len(blacklist)} blacklisted domains from {path}")
    return blacklist


def remove_blacklisted_domains(df: pd.DataFrame, blacklist: set) -> pd.DataFrame:
    """
    Remove rows whose domain column matches any entry in the blacklist.
    Tries to guess the correct domain column name.
    """
    if not blacklist:
        return df

    # Try to guess which column holds the domain
    domain_col = None
    for cand in ["the_domain", "domain_root", "root_domain", "domain", "Domain"]:
        if cand in df.columns:
            domain_col = cand
            break

    if domain_col is None:
        print("[WARN] No domain column found (tried domain_root/root_domain/domain/Domain).")
        print("[WARN] Skipping domain blacklist filtering.")
        return df

    before = len(df)
    df = df[~df[domain_col].isin(blacklist)].copy()
    after = len(df)
    removed = before - after
    print(f"[INFO] Domain filtering: removed {removed} rows using blacklist.")
    return df


def main():
    print(f"[INFO] Loading dataset from {DATA_PATH} ...")
    df = pd.read_csv(DATA_PATH)
    print(f"[INFO] Loaded {len(df)} rows total.")

    # 1) Remove blacklisted domains
    blacklist = load_blacklist(BLACKLIST_PATH)
    df = remove_blacklisted_domains(df, blacklist)

    # 2) Filter by country: Germany + United Kingdom
    target_countries = {"Germany", "United Kingdom"}
    before_country = len(df)
    df = df[df["the_country"].isin(target_countries)].copy()
    after_country = len(df)
    print(f"[INFO] Country filter (Germany + UK): {before_country} -> {after_country} rows.")

    # 3) Build HYPE (News/Media) and CONTROL (Policy/Admin) masks based on Labels
    labels = df["Labels"].astype(str)

    # HYPE: anything with "news" OR "media"
    hype_mask = labels.str.contains("news", case=False, na=False) | \
                labels.str.contains("media", case=False, na=False)

    # CONTROL: anything with "policy" OR "administrative communications",
    # but NOT in HYPE (to keep sets cleanly separated)
    control_mask = (
        labels.str.contains("policy", case=False, na=False) |
        labels.str.contains("administrative communications", case=False, na=False)
    ) & ~hype_mask

    hype_df = df[hype_mask].copy()
    control_df = df[control_mask].copy()

    print("\n[INFO] Subset sizes AFTER all filters (country + blacklist + label logic):")
    print(f"  HYPE (news/media) rows:    {len(hype_df)}")
    print(f"  CONTROL (policy/admin) rows: {len(control_df)}")

    # 4) Save out to CSV
    os.makedirs(os.path.dirname(OUTPUT_HYPE), exist_ok=True)

    hype_df.to_csv(OUTPUT_HYPE, index=False)
    control_df.to_csv(OUTPUT_CONTROL, index=False)

    print(f"\n[INFO] Saved HYPE set to:    {OUTPUT_HYPE}")
    print(f"[INFO] Saved CONTROL set to: {OUTPUT_CONTROL}")
    print("\n[DONE] Phase 3 selection complete.")


if __name__ == "__main__":
    main()