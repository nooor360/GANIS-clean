# GANIS Validation Audit

## Methodology
To ensure the integrity of the semantic pipeline, we performed a manual "Human-in-the-Loop" audit of the clustering results. We randomly sampled 20 documents from the **"Innovator"** cluster in the **Top 50** dataset to verify they genuinely discussed innovation/research rather than administrative policy.

## Audit Results (Sample N=20)
- **Correctly Classified:** 18
- **Incorrectly Classified:** 2
- **Accuracy:** 90%

### Error Analysis
The two misclassified documents were:
1. **Grant Policy Document:** It mentioned "innovation" frequently but was actually a policy document (Should be 'Admin').
2. **Hiring Announcement:** Discussed hiring an "Innovation Lead" (Should be 'Admin' or 'Marketing').

### Mitigation
We updated the stop-word list in Phase 3 to exclude generic "HR" terms, which improved separation between "Doing Innovation" and "Hiring for Innovation."