import json
import csv
import random
import os
from pathlib import Path
from typing import Dict, List, Any

class SyntheticDataGenerator:
    """Generates synthetic data for the Virtual Lab Phase 2 simulation."""

    def __init__(self, output_dir: Path):
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_structure_validation_report(self, filename: str = "structure_validation.json") -> Dict[str, Any]:
        """Generates a synthetic report comparing AlphaFold 3 vs GLYCAM geometry."""
        
        # Simulate some minor deviations but generally acceptable results
        phosphate_rmsd = random.uniform(0.8, 1.8) 
        regraft_needed = phosphate_rmsd > 1.5
        
        report = {
            "timestamp": "2026-05-12T09:00:00Z",
            "target": "MenA-CRM197",
            "af3_model_confidence_plddt": [random.uniform(85, 98) for _ in range(5)], # Sample of residues
            "glycan_geometry_check": {
                "phosphate_backbone_rmsd_angstrom": round(phosphate_rmsd, 3),
                "bond_length_deviations_sigma": round(random.uniform(0.5, 2.8), 2),
                "status": "REQUIRES_REGRAFT" if regraft_needed else "PASS",
                "message": "Phosphate geometry deviation high." if regraft_needed else "Geometry within GLYCAM tolerance."
            },
            "linker_modeling": {
                "chemistry": "Reductive Amination",
                "parameters": "GAFF2",
                "charge_check": "PASS"
            }
        }
        
        filepath = self.output_dir / filename
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=4)
            
        return report

    def generate_md_trajectory_log(self, filename: str = "trajectory_log.csv", num_frames: int = 100) -> str:
        """Generates a CSV log file mimicking an OpenMM simulation output."""
        
        filepath = self.output_dir / filename
        
        headers = ["Frame", "Time_ns", "PotentialEnergy_kJ_mol", "Temperature_K", "Rg_MenA_Angstrom", "SASA_TCell_Epitopes_nm2"]
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(headers)
            
            # Initial state
            Rg = 12.0
            SASA = 15.0
            
            for i in range(num_frames):
                frame = i * 10 
                time_ns = frame / 10.0
                
                # Random walk simulation
                Rg += random.uniform(-0.1, 0.1)
                SASA += random.uniform(-0.2, 0.2)
                
                # Constrain values to realistic ranges
                Rg = max(8.0, min(16.0, Rg))
                SASA = max(5.0, min(25.0, SASA))
                
                energy = -500000 + random.uniform(-500, 500)
                temp = 300 + random.uniform(-2, 2)
                
                writer.writerow([frame, time_ns, int(energy), round(temp, 1), round(Rg, 2), round(SASA, 2)])
                
        return str(filepath)
