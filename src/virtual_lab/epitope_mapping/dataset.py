import torch
from torch.utils.data import Dataset
from typing import List, Tuple

class EpitopeDataset(Dataset):
    def __init__(self, features: torch.Tensor, labels: torch.Tensor):
        """
        Args:
            features (torch.Tensor): Tensor of shape (N_residues, embed_dim)
            labels (torch.Tensor): Tensor of shape (N_residues, 1) or (N_residues,)
        """
        self.features = features
        self.labels = labels

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.labels[idx]

def generate_synthetic_data(
    n_samples: int = 1000, 
    embed_dim: int = 1280
) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Generate synthetic data for training verification.
    
    Args:
        n_samples (int): Number of residues to simulate.
        embed_dim (int): Dimension of feature embeddings (default ESM-2 dim).
        
    Returns:
        features, labels
    """
    # Random features roughly normal
    features = torch.randn(n_samples, embed_dim)
    
    # Synthetic labels: Simple function of features to make it learnable
    # e.g., if sum of first 10 dims > X, then label 1
    # This ensures the model *can* learn something (loss should decrease)
    
    # Linear projection to logits
    true_weights = torch.randn(embed_dim, 1)
    digits = features @ true_weights
    probs = torch.sigmoid(digits)
    labels = (probs > 0.5).float()
    
    return features, labels
