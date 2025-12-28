
import os
import torch
import numpy as np
from pathlib import Path

# Try to import mdtraj for real MD handling
try:
    import mdtraj as md
    HAS_MDTRAJ = True
except ImportError:
    HAS_MDTRAJ = False

SIMULATION_DIR = "data/simulations"

def calculate_rmsf(trajectory):
    """
    Calculate Root Mean Square Fluctuation (RMSF).
    Traj shape: (Frames, Atoms, 3)
    Output shape: (Atoms, 1) normalized
    """
    # 1. Center trajectory (remove COM drift)
    mean_struc = np.mean(trajectory, axis=0) # (Atoms, 3)
    
    # 2. Calculate variance
    diff = trajectory - mean_struc
    sq_diff = diff ** 2
    avg_sq_diff = np.mean(sq_diff, axis=0)
    
    # 3. RMSF
    rmsf = np.sqrt(np.sum(avg_sq_diff, axis=1)) # (Atoms,)
    
    # Normalize for ML input [0, 1]
    rmsf_norm = (rmsf - np.min(rmsf)) / (np.max(rmsf) - np.min(rmsf) + 1e-6)
    return rmsf_norm

def main():
    print("=== Extracting Dynamic Features from MD Trajectories ===")
    
    output_tensors = {}
    sim_dirs = [d for d in Path(SIMULATION_DIR).iterdir() if d.is_dir()]
    
    print(f"Found {len(sim_dirs)} simulations.")
    
    for sim_dir in sim_dirs:
        # Check for Real (DCD) or Mock (NPY)
        traj_dcd = sim_dir / "trajectory.dcd"
        traj_npy = sim_dir / "trajectory.npy"
        
        traj = None
        if traj_dcd.exists() and HAS_MDTRAJ:
            print(f"Processing Real MD: {sim_dir.name}...")
            # For real MD, we usually need a topology (fixed.pdb or similar)
            topo_file = sim_dir / "fixed.pdb" # Assume output by OpenMM
            if not topo_file.exists():
                topo_file = "data/structures/pdb4ae1.ent" # Fallback to original
            
            t = md.load(str(traj_dcd), top=str(topo_file))
            traj = t.xyz # Shape (Frames, Atoms, 3) in nm, converted to Angstrom if needed
            traj = traj * 10.0 # nm to Angstrom
            
        elif traj_npy.exists():
            print(f"Processing Mock MD: {sim_dir.name}...")
            traj = np.load(traj_npy)
            
        if traj is None:
            continue
            
        # Calculate RMSF
        rmsf = calculate_rmsf(traj)
        
        # Convert to Tensor
        tensor = torch.from_numpy(rmsf).float().unsqueeze(1) # (N_atoms, 1)
        
        # Save per site
        site_id = sim_dir.name.split('_')[-1] # LYS157.0
        output_tensors[site_id] = tensor
        
        print(f"  > RMSF Calculated. Mean Fluctuation: {np.mean(rmsf):.4f}")
        
    # Save Aggregate
    out_path = Path("data/processed_features")
    out_path.mkdir(exist_ok=True)
    torch.save(output_tensors, out_path / "dynamic_features.pt")
    
    print(f"\nSaved all dynamic feature tensors to {out_path / 'dynamic_features.pt'}")

if __name__ == "__main__":
    main()
