import torch
import sys
import os

# Add src to path
sys.path.append(os.path.abspath("src"))

from virtual_lab.epitope_mapping.features import FeatureExtractor

def main():
    extractor = FeatureExtractor(embed_dim=1280)
    pdb_file = "data/structures/pdb4aei.ent"
    
    if not os.path.exists(pdb_file):
        print(f"File not found: {pdb_file}")
        return

    print(f"--- Testing Feature Extraction on {pdb_file} ---")
    # We'll use use_mock=False to test real ESM-2 and PDB parsing
    # Warning: This will load ESM-2 (8M) which is several MBs but feasible.
    features = extractor.extract_features([pdb_file], use_mock=False)
    
    print(f"Features shape: {features.shape}")
    if features.shape[0] > 0:
        print(f"Successfully extracted embeddings for {features.shape[0]} residues.")
        print(f"First residue embedding slice: {features[0, :5]}")
    else:
        print("Failed to extract features.")

if __name__ == "__main__":
    main()
