import pandas as pd
import plotly.express as px
import os

# --- CONFIG ---
# We match the SEMANTIC file (coordinates) with the VOICE file (labels)
DATA_PAIRS = {
    "Hype_Top50": {
        "coords": "data/semantic/hype_top50_semantic.csv",
        "voice": "data/semantic/hype_top50_with_voice.csv"
    },
    "Hype_General": {
        "coords": "data/semantic/hype_ge1000_semantic.csv",
        "voice": "data/semantic/hype_ge1000_with_voice.csv"
    },
    "Control_Top50": {
        "coords": "data/semantic/control_top50_semantic.csv",
        "voice": "data/semantic/control_top50_with_voice.csv"
    },
    "Control_General": {
        "coords": "data/semantic/control_ge1000_semantic.csv",
        "voice": "data/semantic/control_ge1000_with_voice.csv"
    }
}

# Custom GANIS Brand Colors
COLOR_MAP = {
    "Innovator": "#00CC96",   # Green/Teal (Positive)
    "Risk": "#EF553B",        # Red (Warning)
    "Admin": "#636EFA",       # Blue (Corporate)
    "Marketing": "#AB63FA",   # Purple (Creative)
    "Pedagogical": "#FFA15A", # Orange (Teaching)
    "Unassigned": "#D3D3D3"   # Grey (Noise)
}

def main():
    print("Generating Interactive Semantic Maps (HTML)...")
    
    # Ensure visuals folder exists
    os.makedirs("visuals", exist_ok=True)

    for label, paths in DATA_PAIRS.items():
        semantic_path = paths["coords"]
        voice_path = paths["voice"]

        if not os.path.exists(semantic_path) or not os.path.exists(voice_path):
            print(f"⚠️ Skipping {label} (Missing files)")
            continue
            
        print(f"Processing {label}...")
        try:
            # Load Coordinates
            df_coords = pd.read_csv(semantic_path)
            # Load Voices
            df_voice = pd.read_csv(voice_path)
            
            # MERGE STRATEGY: 
            # We merge on file_name to ensure data aligns perfectly.
            if len(df_coords) != len(df_voice):
                print(f"⚠️ Warning: Row count mismatch for {label}. Merging on file_name.")
                df = pd.merge(df_coords, df_voice[['file_name', 'voice']], on='file_name', how='left')
            else:
                # Fast merge if lengths match
                df = df_coords.copy()
                df['voice'] = df_voice['voice']

        except Exception as e:
            print(f"Error reading {label}: {e}")
            continue
        
        # 1. Check for required columns (CORRECTED: looking for umap_x, umap_y)
        required_cols = ['umap_x', 'umap_y', 'voice']
        if not all(col in df.columns for col in required_cols):
            print(f"⚠️ Missing columns in {label} after merge. Columns found: {df.columns.tolist()}")
            continue

        # 2. Fill missing voices
        df["voice"] = df["voice"].fillna("Unassigned")

        # 3. Prepare Hover Data
        hover_data = {}
        if "Title" in df.columns: hover_data["Title"] = True
        if "the_name" in df.columns: hover_data["the_name"] = True
        if "cluster_id" in df.columns: hover_data["cluster_id"] = True
        
# 4. Generate Interactive Plot
        fig = px.scatter(
            df, 
            x='umap_x', 
            y='umap_y', 
            color='voice',
            hover_data=hover_data,
            title=f"GANIS Interactive Map: {label}",
            color_discrete_map=COLOR_MAP,
            template="plotly_white",
            opacity=0.75
        )

        # 5. Polish the Look
        fig.update_traces(marker=dict(size=6, line=dict(width=0.5, color='DarkSlateGrey')))
        fig.update_layout(
            legend_title_text='Narrative Voice',
            xaxis_title="Semantic Dimension 1",
            yaxis_title="Semantic Dimension 2",
            hovermode='closest'
        )
        
        # 6. Save as HTML
        output_filename = f"visuals/interactive_map_{label.lower()}.html"
        fig.write_html(output_filename)
        print(f"✅ Saved interactive map to {output_filename}")

if __name__ == "__main__":
    main()