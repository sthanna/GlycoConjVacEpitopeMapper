import torch
import torch.nn as nn
from typing import Optional, Tuple
from torch.utils.data import DataLoader

class EpitopeClassifier(nn.Module):
    def __init__(self, embed_dim: int = 1280, hidden_dim: int = 256):
        super().__init__()
        self.fc1 = nn.Linear(embed_dim, hidden_dim)
        self.act = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        self.fc2 = nn.Linear(hidden_dim, 1) # Binary classification
        # Note: We will use BCEWithLogitsLoss for stability, so forward optionally returns logits

    def forward(self, x: torch.Tensor, return_logits: bool = False) -> torch.Tensor:
        h = self.act(self.fc1(x))
        h = self.dropout(h)
        logits = self.fc2(h)
        if return_logits:
            return logits
        probs = torch.sigmoid(logits)
        return probs

def train_model(
    model: EpitopeClassifier, 
    train_loader: DataLoader, 
    val_loader: Optional[DataLoader] = None,
    epochs: int = 10,
    lr: float = 1e-3,
    device: str = "cpu"
) -> dict:
    """
    Train the EpitopeClassifier.
    
    Args:
        model: Instance of EpitopeClassifier
        train_loader: DataLoader for training data
        val_loader: DataLoader for validation data (optional)
        epochs: Number of epochs
        lr: Learning rate
        device: 'cpu' or 'cuda'
        
    Returns:
        history (dict): Training logs (loss, acc)
    """
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = nn.BCEWithLogitsLoss()
    
    history = {"train_loss": [], "val_loss": [], "val_acc": []}
    
    print(f"Starting training on {device} for {epochs} epochs...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for features, labels in train_loader:
            features, labels = features.to(device), labels.to(device)
            
            optimizer.zero_grad()
            logits = model(features, return_logits=True).squeeze()
            
            # Ensure labels are float for BCE and match shape
            loss = criterion(logits, labels.float().squeeze())
            
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        history["train_loss"].append(avg_loss)
        
        # Validation
        val_log = ""
        if val_loader:
            model.eval()
            val_loss = 0
            correct = 0
            total = 0
            with torch.no_grad():
                for v_feat, v_lbl in val_loader:
                    v_feat, v_lbl = v_feat.to(device), v_lbl.to(device)
                    v_logits = model(v_feat, return_logits=True).squeeze()
                    v_loss = criterion(v_logits, v_lbl.float().squeeze())
                    val_loss += v_loss.item()
                    
                    preds = (torch.sigmoid(v_logits) > 0.5).float()
                    correct += (preds == v_lbl.squeeze()).sum().item()
                    total += len(v_lbl)
            
            avg_val_loss = val_loss / len(val_loader)
            val_acc = correct / total if total > 0 else 0
            history["val_loss"].append(avg_val_loss)
            history["val_acc"].append(val_acc)
            val_log = f" | Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f}"
            
        print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_loss:.4f}{val_log}")
        
    return history
