# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Optional
from torch.utils.data import DataLoader

class GraphConvolution(nn.Module):
    """
    Simple GCN Layer: H = ReLU( (A + I) * X * W )
    """
    def __init__(self, in_features, out_features):
        super(GraphConvolution, self).__init__()
        self.linear = nn.Linear(in_features, out_features)

    def forward(self, x, adj):
        # adj is (Batch, N, N)
        # x is (Batch, N, In)
        
        # Add self-loops (Identity)
        batch_size, num_nodes, _ = adj.size()
        I = torch.eye(num_nodes, device=adj.device).unsqueeze(0).expand(batch_size, -1, -1)
        adj_hat = adj + I
        
        # Normalize (simplistic row normalization)
        degree = adj_hat.sum(dim=2, keepdim=True).clamp(min=1.0)
        adj_norm = adj_hat / degree
        
        # Message Passing
        support = self.linear(x) # (Batch, N, Out)
        output = torch.bmm(adj_norm, support) # (Batch, N, N) @ (Batch, N, Out) -> (Batch, N, Out)
        
        return F.relu(output)

class GraphEpitopeClassifier(nn.Module):
    """
    GNN-based Epitope Classifier (Prototype for SE(3)-Transformer)
    """
    def __init__(self, input_dim=320, hidden_dim=64):
        super(GraphEpitopeClassifier, self).__init__()
        self.gcn1 = GraphConvolution(input_dim, hidden_dim)
        self.gcn2 = GraphConvolution(hidden_dim, hidden_dim)
        self.fc = nn.Linear(hidden_dim, 1)

    def forward(self, x, adj):
        # x: (Batch, N, 320)
        # adj: (Batch, N, N)
        
        h = self.gcn1(x, adj)
        h = F.dropout(h, p=0.2, training=self.training)
        h = self.gcn2(h, adj)
        
        logits = self.fc(h) # (Batch, N, 1)
        output = torch.sigmoid(logits)
        return output

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
    model: nn.Module, 
    train_loader: DataLoader, 
    val_loader: Optional[DataLoader] = None,
    epochs: int = 10,
    lr: float = 1e-3,
    device: str = "cpu"
) -> dict:
    """
    Train the Classifier.
    """
    model.to(device)
    optimizer = torch.optim.AdamW(model.parameters(), lr=lr)
    criterion = nn.BCELoss() # Simplified to BCELoss for prototype (since GCN outputs probs)
    
    history = {"train_loss": [], "val_loss": [], "val_acc": []}
    
    print(f"Starting training on {device} for {epochs} epochs...")
    
    for epoch in range(epochs):
        model.train()
        total_loss = 0
        
        for batch in train_loader:
            # Handle variable return (Tuple vs Tensor)
            if len(batch) == 3:
                x, adj, y = batch
                x, adj, y = x.to(device), adj.to(device), y.to(device)
                probs = model(x, adj).squeeze()
            else:
                x, y = batch
                x, y = x.to(device), y.to(device)
                probs = model(x).squeeze()
            
            optimizer.zero_grad()
            loss = criterion(probs, y.float().squeeze())
            loss.backward()
            optimizer.step()
            
            total_loss += loss.item()
            
        avg_loss = total_loss / len(train_loader)
        history["train_loss"].append(avg_loss)

        # Validation
        if val_loader is not None:
            model.eval()
            val_loss = 0.0
            correct = 0
            total = 0
            with torch.no_grad():
                for batch in val_loader:
                    if len(batch) == 3:
                        x, adj, y = batch
                        x, adj, y = x.to(device), adj.to(device), y.to(device)
                        probs = model(x, adj).squeeze()
                    else:
                        x, y = batch
                        x, y = x.to(device), y.to(device)
                        probs = model(x).squeeze()
                    val_loss += criterion(probs, y.float().squeeze()).item()
                    preds = (probs > 0.5).float()
                    correct += (preds == y.float().squeeze()).sum().item()
                    total += y.numel()
            avg_val_loss = val_loss / len(val_loader)
            val_acc = correct / total if total > 0 else 0.0
            history["val_loss"].append(avg_val_loss)
            history["val_acc"].append(val_acc)
            print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_loss:.4f} | Val Loss: {avg_val_loss:.4f} | Val Acc: {val_acc:.4f}")
        else:
            print(f"Epoch {epoch+1}/{epochs} | Train Loss: {avg_loss:.4f}")

    return history
