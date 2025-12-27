import torch
import sys
import os
sys.path.append(os.path.join(os.getcwd(), 'src'))
from torch.utils.data import DataLoader
from virtual_lab.epitope_mapping.model import EpitopeClassifier, train_model
from virtual_lab.epitope_mapping.dataset import EpitopeDataset, generate_synthetic_data

def main():
    print("=== Epitope Mapping Training Pipeline ===")
    
    # Configuration
    EMBED_DIM = 320
    HIDDEN_DIM = 256
    BATCH_SIZE = 32
    EPOCHS = 5
    LR = 1e-3
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
    
    print(f"Device: {DEVICE}")
    
    # 1. Generate Synthetic Data
    print("\n[1] Generating Synthetic Data...")
    train_feats, train_lbls = generate_synthetic_data(n_samples=2000, embed_dim=EMBED_DIM)
    val_feats, val_lbls = generate_synthetic_data(n_samples=500, embed_dim=EMBED_DIM)
    
    train_dataset = EpitopeDataset(train_feats, train_lbls)
    val_dataset = EpitopeDataset(val_feats, val_lbls)
    
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE)
    
    print(f"Training Samples: {len(train_dataset)}")
    print(f"Validation Samples: {len(val_dataset)}")
    
    # 2. Initialize Model
    print("\n[2] Initializing Model...")
    model = EpitopeClassifier(embed_dim=EMBED_DIM, hidden_dim=HIDDEN_DIM)
    
    # 3. Train
    print("\n[3] Starting Training Loop...")
    history = train_model(
        model=model,
        train_loader=train_loader,
        val_loader=val_loader,
        epochs=EPOCHS,
        lr=LR,
        device=DEVICE
    )
    
    # 4. Results
    final_acc = history["val_acc"][-1] if history["val_acc"] else 0.0
    print(f"\nTraining Complete. Final Validation Accuracy: {final_acc:.4f}")
    
    if final_acc > 0.6:
        print("SUCCESS: Model learned from synthetic data (Acc > 0.6)")
    else:
        print("WARNING: Model performance is low. Check synthetic generation logic.")

if __name__ == "__main__":
    main()
