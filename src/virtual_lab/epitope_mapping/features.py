import torch
import numpy as np
from typing import List, Dict

class FeatureExtractor:
    def __init__(self, embed_dim: int = 320):
        self.embed_dim = embed_dim

    def get_sequence_from_pdb(self, pdb_file: str) -> str:
        """
        Extract the amino acid sequence from a PDB file using Biopython.
        """
        from Bio import PDB
        parser = PDB.PDBParser(QUIET=True)
        try:
            structure = parser.get_structure("protein", pdb_file)
            ppb = PDB.PPBuilder()
            sequence = ""
            for pp in ppb.build_peptides(structure):
                sequence += str(pp.get_sequence())
            return sequence
        except Exception as e:
            print(f"Error parsing PDB {pdb_file}: {e}")
            return ""

    def extract_features(self, pdb_files: List[str], use_mock: bool = False) -> torch.Tensor:
        """
        Extract features using ESM-2 (or mock).
        """
        if use_mock:
            print(f"Extracting features (MOCK) from {len(pdb_files)} structures...")
            n_residues = 300 
            return torch.randn(n_residues, self.embed_dim)

        print(f"Extracting features (ESM-2) from {len(pdb_files)} structures...")
        
        # Lazy load model to avoid overhead if not used
        if not hasattr(self, 'model'):
            from transformers import EsmModel, AutoTokenizer
            model_name = "facebook/esm2_t6_8M_UR50D" # Standard lightweight version
            print(f"Loading ESM-2 model ({model_name})...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = EsmModel.from_pretrained(model_name)
            self.model.eval()

        features_list = []
        for pdb in pdb_files:
            sequence = self.get_sequence_from_pdb(pdb)
            if not sequence:
                print(f"Warning: Empty sequence for {pdb}, skipping.")
                continue
            
            inputs = self.tokenizer(sequence, return_tensors="pt")
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # last_hidden_state: (Batch, Seq_Len, Dim)
            # We want to remove the special [CLS] and [SEP] tokens at start/end
            # ESM tokenizer adds <cls> and <eos>
            emb = outputs.last_hidden_state.squeeze(0) # (Seq_Len_with_tokens, Dim)
            # Remove first and last token
            emb = emb[1:-1, :]
            
            print(f"Extracted {emb.shape[0]} residue embeddings from {pdb}")
            features_list.append(emb)
            
        # Return the concatenated features if multiple, or just the first
        return torch.cat(features_list, dim=0) if features_list else torch.empty(0, self.embed_dim)

    def compute_glycan_features(self, pdb_file: str):
        """
        Compute glycan-specific features like density or shielding.
        """
        pass
