import matplotlib.pyplot as plt

# Global pipeline stage counts from your actual logs
STAGES = [
    "Raw scraped",
    "Low-info filtered",
    "Boilerplate removed",
    "Domain blacklist applied",
    "Germany+UK + AI-label subset",
]

COUNTS = [
    34364,  # Initial size
    33932,  # After low-information filter
    30166,  # After boilerplate removal
    29251,  # After domain blacklist
    4915,   # After country + label selection (HYPE + CONTROL)
]

plt.figure()
plt.plot(STAGES, COUNTS, marker="o")
plt.xlabel("Pipeline stage")
plt.ylabel("Number of documents")
plt.title("Garbage Removal and Focused Selection Across GANIS Pipeline")
plt.xticks(rotation=20)

out_path = "visuals/garbage_removal_comparison.png"
plt.tight_layout()
plt.savefig(out_path, dpi=200)
plt.close()

print(f"[INFO] Saved Garbage Removal Comparison → {out_path}")