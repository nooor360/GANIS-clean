# GANIS: Generative AI Narrative Intelligence System
### *A Semantic Pipeline for Decoding University AI Strategies*

**Status:** 🏆 Hackathon Submission (Track 5)  
**Team:** GANIS

## 🚀 Project Goal
To prove that universities utilize a **"Dual-Narrative Strategy"** regarding Generative AI:
1.  **High-Entropy Marketing:** Selling AI as a revolutionary partner to students and press.
2.  **Low-Entropy Control:** Policing AI as a threat in internal policy and governance documents.

## 🧠 Core Hypothesis
*"Universities optimize for **Reputation** in the news (Innovation Voice), but optimize for **Liability** in policy (Risk/Admin Voice)."*

We introduce the **AI Optimism Index**, a novel metric to quantify this gap.

See visuals/interactive_map_hype_top50.html for an interactive exploration of the semantic clusters.

## How to Reproduce (GANIS Track 5)

```bash
# 1) set up environment
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 2) start from raw Excel in data/Final_table_results.xlsx
python code/garbage_filter.py

# 3) build country + label subsets
python code/phase3_selection.py
python code/phase4_split_by_rank.py

# 4) semantic clustering + voices
python code/phase5_semantic_pipeline.py --input data/ganis_hype_top50.csv     --output_prefix hype_top50
python code/phase5_semantic_pipeline.py --input data/ganis_hype_ge1000.csv   --output_prefix hype_ge1000
python code/phase5_semantic_pipeline.py --input data/ganis_control_top50.csv --output_prefix control_top50
python code/phase5_semantic_pipeline.py --input data/ganis_control_ge1000.csv --output_prefix control_ge1000
python code/phase5_voice_assignment_multi.py --input data/semantic/hype_top50_semantic.csv     --output data/semantic/hype_top50_with_voice.csv
python code/phase5_voice_assignment_multi.py --input data/semantic/hype_ge1000_semantic.csv    --output data/semantic/hype_ge1000_with_voice.csv
python code/phase5_voice_assignment_multi.py --input data/semantic/control_top50_semantic.csv  --output data/semantic/control_top50_with_voice.csv
python code/phase5_voice_assignment_multi.py --input data/semantic/control_ge1000_semantic.csv --output data/semantic/control_ge1000_with_voice.csv

# 5) compute index + visuals
python code/phase6_ai_positioning_index.py
python code/phase7_visual_garbage_comparison.py
python code/phase7_visual_umap_map.py
python code/phase7_visual_voice_and_index.py