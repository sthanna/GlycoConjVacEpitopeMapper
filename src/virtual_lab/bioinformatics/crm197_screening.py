import sys
import os
import numpy as np
from Bio.PDB import PDBParser, SASA, Selection

import warnings

# Suppress PDB warnings
warnings.filterwarnings('ignore')

def calculate_centroid(residue):
    """Calculate the geometric center of a residue's atoms."""
    coords = [atom.get_coord() for atom in residue]
    return np.mean(coords, axis=0)

def get_min_distance_to_zone(residue, zone_atoms):
    """
    Calculate the minimum Euclidean distance from a residue's centroid 
    to any atom in the forbidden zone.
    """
    # Use NZ nitrogen for Lysine if available (active conjugation site)
    if residue.resname == 'LYS' and 'NZ' in residue:
        source_coord = residue['NZ'].get_coord()
    else:
        source_coord = calculate_centroid(residue)
        
    min_dist = float('inf')
    
    # Vectorized approach for speed
    zone_coords = np.array([atom.get_coord() for atom in zone_atoms])
    dists = np.linalg.norm(zone_coords - source_coord, axis=1)
    return np.min(dists)

def main():
    print("=== Tier 1 Screening: CRM197 Conjugation Site Selection ===")
    
    # 1. Load Structure
    pdb_path = "data/structures/pdb4ae1.ent"
    parser = PDBParser()
    structure = parser.get_structure("CRM197", pdb_path)
    model = structure[0] # Assume first model
    
    print(f"Loaded Structure: {pdb_path}")

    # Use only Chain A
    chain_a = model['A']
    all_residues = list(chain_a.get_residues())
    print(f"Analyzing Chain A: {len(all_residues)} residues.")
    ppz_ranges = [
        range(271, 291), # Python range is exclusive at end, so 291
        range(321, 341),
        range(411, 431)
    ]
    
    all_residues = list(model.get_residues())
    
    # Identify Zone Atoms
    zone_atoms = []
    for res in all_residues:
        # Note: PDB residue numbering might not be 1-indexed perfectly, 
        # using res.id[1] is standard.
        if any(res.id[1] in r for r in ppz_ranges):
            zone_atoms.extend(res.get_atoms())
            
    print(f"Defined Protected Presentation Zones (PPZs): {len(zone_atoms)} atoms.")
    
    # 3. Calculate SASA
    print("Calculating SASA (Solvent Accessible Surface Area)...")
    sr = SASA.ShrakeRupley()
    sr.compute(model, level="R") # Residue level
    
    # 4. Filter Lysines
    candidates = []
    lysines = [r for r in all_residues if r.resname == 'LYS']
    
    print(f"Found {len(lysines)} Lysine residues.")
    print("\nProcessing Candidates...")
    print(f"{'ResID':<10} | {'SASA (A^2)':<12} | {'Dist to PPZ (A)':<15} | {'Status'}")
    print("-" * 55)
    
    for lys in lysines:
        res_id = lys.id[1]
        sasa = lys.sasa
        
        # Calculate Distance to PPZ
        dist = get_min_distance_to_zone(lys, zone_atoms)
        
        # Criteria
        is_far_enough = dist >= 15.0
        is_exposed = sasa > 40.0
        
        status = "PASS" if (is_far_enough and is_exposed) else "FAIL"
        
        if status == "PASS":
            candidates.append({
                'resid': res_id,
                'sasa': sasa,
                'dist': dist
            })
            
        print(f"LYS {res_id:<6} | {sasa:<12.2f} | {dist:<15.2f} | {status}")

    # 5. Output Top Candidates
    candidates.sort(key=lambda x: x['sasa'], reverse=True)
    
    print("\n=== TOP 5 CANDIDATE SITES ===")
    print("Criteria: SASA > 40 A^2 AND Dist to PPZ > 15 A")
    print(f"{'Rank':<5} | {'ResID':<10} | {'SASA':<10} | {'Dist to PPZ'}")
    
    output_lines = ["Rank,ResID,SASA,Dist_to_PPZ"]
    
    for i, c in enumerate(candidates[:5]):
        print(f"{i+1:<5} | LYS {c['resid']:<6} | {c['sasa']:<10.2f} | {c['dist']:.2f}")
        output_lines.append(f"{i+1},{c['resid']},{c['sasa']:.2f},{c['dist']:.2f}")
        
    # Save Report
    os.makedirs("data/tier1_report", exist_ok=True)
    with open("data/tier1_report/top_candidates.csv", "w") as f:
        f.write("\n".join(output_lines))
        
    print("\nReport saved to data/tier1_report/top_candidates.csv")

if __name__ == "__main__":
    main()
