
import os
import torch
import numpy as np
import pandas as pd
from Bio.PDB import PDBParser
from torch.utils.data import Dataset, DataLoader
import torch.nn as nn
import torch.optim as optim

# Import internal modules (assuming run from project root)
import sys
sys.path.append(os.path.join(os.getcwd(), 'src'))
from virtual_lab.epitope_mapping.model import GraphEpitopeClassifier
from virtual_lab.epitope_mapping.features import FeatureExtractor

class HybridEpitopeDataset(Dataset):
    """
    Hybrid Dataset combining Real Protein Embeddings (ESM-2) with Synthetic Glycan Data.
    """
    def __init__(self, pdb_path, candidate_sites_csv, num_samples=50):
        self.pdb_path = pdb_path
        self.num_samples = num_samples
        
        # 1. Load Real Protein Data
        print(f"Extracting ESM-2 features from {pdb_path}...")
        extractor = FeatureExtractor()
        # extract_features returns shape (N, 320)
        self.protein_feats = extractor.extract_features([pdb_path])
        self.protein_len = self.protein_feats.shape[0]
        self.embed_dim = self.protein_feats.shape[1] # Should be 320 for esm2_t6_8M
        
        # 2. Load Candidates
        df = pd.read_csv(candidate_sites_csv)
        self.target_indices = df['ResID'].values - 1 # PDB 1-based to 0-based
        print(f"Target Conjugation Sites (0-indexed): {self.target_indices}")
        
    def __len__(self):
        return self.num_samples

    def __getitem__(self, idx):
        # 1. Protein Features (Static)
        # Shape: (N_prot, 320)
        prot_x = self.protein_feats.clone().detach()
        
        # 2. Synthetic Glycan Features (Dynamic/Randomized)
        # MenA Repeat: [ManNAc - P]n -> approx 10 nodes for a short chain
        num_glycan_nodes = 10 
        glycan_x = torch.randn(num_glycan_nodes, self.embed_dim) 
        
        # 3. Combine
        x = torch.cat([prot_x, glycan_x], dim=0) # (N_prot + N_glyc, 320)
        
        # 4. Generate Synthetic Labels
        # Logic: Target indices = 1 (Epitope), Neighbors = 1, Others = 0
        # This simulates a "successful" conjugation where the target site becomes immunogenic
        y = torch.zeros(x.shape[0])
        
        # Mark targets as positive
        for target_idx in self.target_indices:
            if target_idx < self.protein_len:
                y[target_idx] = 1.0
                # Spread to neighbors (simulating epitope footprint)
                if target_idx > 0: y[target_idx - 1] = 1.0
                if target_idx < self.protein_len - 1: y[target_idx + 1] = 1.0
        
        # Mark random glycan nodes as positive (immunodominant sugar)
        for i in range(num_glycan_nodes):
            if torch.rand(1) > 0.5:
                y[self.protein_len + i] = 1.0
                
        # 5. Adjacency Matrix (Fully connected for prototype)
        num_nodes = x.shape[0]
        adj = torch.ones(num_nodes, num_nodes)
        
        return x, adj, y.float()

def train_prototype():
    print("=== Phase 4: Prototype Model Training (ESM-2 + GNN) ===")
    
    # Paths
    pdb_file = "data/structures/pdb4ae1.ent"
    candidates_file = "data/tier1_report/top_candidates.csv"
    
    # Config
    BATCH_SIZE = 4
    EPOCHS = 10
    LR = 0.001
    
    # Data
    dataset = HybridEpitopeDataset(pdb_file, candidates_file)
    dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
    
    # Model (GraphEpitopeClassifier)
    model = GraphEpitopeClassifier(input_dim=320, hidden_dim=64)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=LR)
    
    print(f"\nModel Initialized: GraphEpitopeClassifier(input_dim=320)")
    print("Starting Training Loop...")
    
    # Save Report
    os.makedirs("data/training_report", exist_ok=True)
    report_path = "data/training_report/model_metrics.txt"
    
    with open(report_path, "w") as f:
        f.write("Epoch,Loss\n")
        
        for epoch in range(EPOCHS):
            epoch_loss = 0
            for batch_idx, (x, adj, y) in enumerate(dataloader):
                optimizer.zero_grad()
                
                # Forward
                output = model(x, adj) # Output shape (Batch, Nodes, 1)
                output = output.squeeze(-1) # (Batch, Nodes)
                
                # Loss
                loss = criterion(output, y)
                loss.backward()
                optimizer.step()
                
                epoch_loss += loss.item()
            
            avg_loss = epoch_loss / len(dataloader)
            print(f"Epoch {epoch+1}/{EPOCHS} - Loss: {avg_loss:.4f}")
            f.write(f"{epoch+1},{avg_loss:.4f}\n")
            
    # Save Checkpoint
    os.makedirs("data/checkpoints", exist_ok=True)
    torch.save(model.state_dict(), "data/checkpoints/prototype_model.pt")
    print("\nTraining Complete.")
    print(f"Model saved to data/checkpoints/prototype_model.pt")
    print(f"Metrics saved to {report_path}")

if __name__ == "__main__":
    train_prototype()
