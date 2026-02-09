# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
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

    def compute_glycan_features(self, pdb_file: str) -> Dict:
        """
        Compute glycan-specific features like density or shielding from a PDB file.

        Returns a dict with per-residue SASA values and glycan neighbor counts
        within a contact radius, which serve as proxies for glycan shielding.
        """
        from Bio import PDB
        from Bio.PDB import SASA

        parser = PDB.PDBParser(QUIET=True)
        try:
            structure = parser.get_structure("protein", pdb_file)
        except Exception as e:
            print(f"Error parsing PDB {pdb_file}: {e}")
            return {"sasa": np.array([]), "glycan_neighbor_counts": np.array([])}

        model = structure[0]

        # Compute residue-level SASA
        sr = SASA.ShrakeRupley()
        sr.compute(model, level="R")

        residues = [r for r in model.get_residues() if r.id[0] == " "]
        sasa_values = np.array([r.sasa for r in residues], dtype=np.float32)

        # Count sugar/glycan residues (HETATM with common glycan names) near each residue
        glycan_resnames = {"NAG", "MAN", "BMA", "FUC", "GAL", "SIA", "GLC"}
        glycan_atoms = [
            atom
            for r in model.get_residues()
            if r.resname.strip() in glycan_resnames
            for atom in r.get_atoms()
        ]

        contact_radius = 10.0  # Angstroms
        neighbor_counts = np.zeros(len(residues), dtype=np.int32)

        if glycan_atoms:
            glycan_coords = np.array([a.get_coord() for a in glycan_atoms])
            for i, res in enumerate(residues):
                centroid = np.mean([a.get_coord() for a in res.get_atoms()], axis=0)
                dists = np.linalg.norm(glycan_coords - centroid, axis=1)
                neighbor_counts[i] = int(np.sum(dists < contact_radius))

        return {
            "sasa": sasa_values,
            "glycan_neighbor_counts": neighbor_counts,
        }
