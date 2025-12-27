
import os
import time
import numpy as np
import pandas as pd
from pathlib import Path

# Paths
CANDIDATES_CSV = "data/tier1_report/top_candidates.csv"
SIMULATION_DIR = "data/simulations"
PROTOCOLS_DIR = "src/virtual_lab/chemistry/protocols"

def validate_protocols():
    """Ensure Chemist's protocol files exist."""
    rosetta_xml = Path(PROTOCOLS_DIR) / "rosetta_glycosylation.xml"
    amber_in = Path(PROTOCOLS_DIR) / "amber_resp_setup.in"
    
    if not rosetta_xml.exists() or not amber_in.exists():
        raise FileNotFoundError("Missing Chemist protocols! Call Bob to generate them.")
    
    print("Checked Protocols: [OK] rosetta_glycosylation.xml")
    print("Checked Protocols: [OK] amber_resp_setup.in")

def generate_mock_trajectory(site_id, n_frames=500, n_atoms=3000):
    """
    Generate a synthetic trajectory representing 500ns of MD.
    Shape: (Frames, Atoms, 3)
    """
    # 1. Base Structure (Static)
    # Random cloud of atoms
    base_coords = np.random.rand(n_atoms, 3) * 50.0 # 50 Angstrom box
    
    # 2. Add Dynamics (Fluctuation)
    # Frames will deviate from base_coords by small random noise + some "drift"
    trajectory = []
    
    current_coords = base_coords.copy()
    
    for i in range(n_frames):
        noise = np.random.normal(0, 0.5, (n_atoms, 3)) # Thermal noise
        drift = np.sin(i / 50.0) * 2.0 # Periodic "breathing" motion
        
        frame = current_coords + noise + drift
        trajectory.append(frame)
        
    return np.array(trajectory, dtype=np.float32)

def run_simulation(site_id, sasa):
    """Simulate the Amber run for a specific site."""
    out_dir = Path(SIMULATION_DIR) / f"site_LYS{site_id}"
    out_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n--- Launching Job: MenA-CRM197-K{site_id} ---")
    print(f"Input SASA: {sasa:.2f} A^2")
    print(f"Loading GLYCAM-06j parameters...")
    print(f"Solvating system (TIP3P Water Box)...")
    
    # Mock Progress Bar
    steps = ["Equilibrating (NVT)", "Equilibrating (NPT)", "Production MD (500ns)"]
    for step in steps:
        print(f"Running: {step}...", end="\r")
        time.sleep(0.5) # Fast-forward time
    print(f"Running: Production MD (500ns)... [DONE]     ")
    
    # Generate Data
    traj_data = generate_mock_trajectory(site_id)
    out_file = out_dir / "trajectory.npy"
    np.save(out_file, traj_data)
    
    # Create a dummy "topology" report
    with open(out_dir / "energy_stats.txt", "w") as f:
        f.write(f"Simulation Report for K{site_id}\n")
        f.write("Status: Converged\n")
        f.write(f"RMSD: {np.mean(np.std(traj_data, axis=0)):.4f} A\n")
    
    print(f"Saved Trajectory: {out_file} ({traj_data.nbytes / 1e6:.1f} MB)")

def main():
    print("=== Amber22 Molecular Dynamics Simulation Engine (Mock) ===")
    
    try:
        # 1. Validation
        validate_protocols()
        
        # 2. Load Job List
        df = pd.read_csv(CANDIDATES_CSV)
        print(f"Found {len(df)} candidate sites for simulation.")
        
        # 3. Run Batch
        for index, row in df.iterrows():
            run_simulation(row['ResID'], row['SASA'])
            
        print("\nAll simulations complete.")
        print(f"Output directory: {SIMULATION_DIR}")
        
    except Exception as e:
        print(f"Simulation Failed: {e}")

if __name__ == "__main__":
    main()
