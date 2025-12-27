
import os
import json
import torch
import pandas as pd
import numpy as np
from pathlib import Path

# Paths
CANDIDATES_CSV = "data/tier1_report/top_candidates.csv"
TRAINING_REPORT = "data/training_report/model_metrics.txt"
DYNAMIC_FEATURES = "data/processed_features/dynamic_features.pt"
OUTPUT_JSON = "dashboard/public/data.json"

def main():
    print("=== Exporting Pipeline Data for Dashboard ===")
    
    # 1. Load Candidates
    try:
        df_candidates = pd.read_csv(CANDIDATES_CSV)
        candidates_list = df_candidates.to_dict(orient='records')
        print(f"Loaded {len(candidates_list)} candidates.")
    except Exception as e:
        print(f"Error loading candidates: {e}")
        candidates_list = []

    # 2. Load Training Metrics
    try:
        df_metrics = pd.read_csv(TRAINING_REPORT)
        metrics_list = df_metrics.to_dict(orient='records')
        print(f"Loaded {len(metrics_list)} training epochs.")
    except Exception as e:
        print(f"Error loading metrics: {e}")
        metrics_list = []

    # 3. Load Dynamic Features (RMSF)
    try:
        dynamic_feats = torch.load(DYNAMIC_FEATURES, weights_only=False)
        rmsf_data = {}
        for site_key, tensor in dynamic_feats.items():
            # tensor is (N_atoms, 1)
            # We want to downsample or provide summary for plotting
            values = tensor.squeeze().numpy().tolist()
            # Downsample to ~100 points for visualization if too large
            if len(values) > 100:
                step = len(values) // 100
                values = values[::step][:100]
            
            rmsf_data[site_key] = values
        print(f"Loaded RMSF data for {len(rmsf_data)} sites.")
    except Exception as e:
        print(f"Error loading dynamic features: {e}")
        rmsf_data = {}

    # 4. Consolidate
    data = {
        "project": "MenA-CRM197 Epitope Mapping",
        "timestamp": pd.Timestamp.now().isoformat(),
        "candidates": candidates_list,
        "training_history": metrics_list,
        "rmsf_profiles": rmsf_data,
        "summary": {
            "top_site": candidates_list[0]['ResID'] if candidates_list else None,
            "final_loss": metrics_list[-1]['Loss'] if metrics_list else None,
            "status": "Pipeline Complete"
        }
    }

    # 5. Save
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(data, f, indent=2)
    
    print(f"Data exported successfully to {OUTPUT_JSON}")

if __name__ == "__main__":
    main()
