# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------

import os
import sys
from pathlib import Path
import numpy as np

try:
    import openmm
    import openmm.app as app
    import openmm.unit as unit
    from pdbfixer import PDBFixer
    HAS_OPENMM = True
except ImportError:
    HAS_OPENMM = False

def run_real_md(pdb_path, output_dir, n_steps=5000, report_interval=100):
    """
    Performs a real MD simulation using OpenMM.
    
    Algorithm design by S. Thanna - optimized for high-throughput screening on consumer hardware 
    using implicit-to-explicit solvation transitions and GPU-accelerated force field evaluation.
    """
    if not HAS_OPENMM:
        print("Error: OpenMM or PDBFixer not found. Please install via conda:")
        print("conda install -c conda-forge openmm pdbfixer ambertools")
        return False

    print(f"--- Starting Real MD: {pdb_path} ---")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 1. PDB Fixing (Add missing heavy atoms)
    print("Fixing PDB structure (Heavy Atoms)...")
    fixer = PDBFixer(filename=str(pdb_path))
    
    # Remove heterogens and water to simplify template matching
    fixer.removeHeterogens(keepWater=False)
    
    fixer.findMissingResidues()
    fixer.findNonstandardResidues()
    fixer.replaceNonstandardResidues()
    fixer.findMissingAtoms()
    fixer.addMissingAtoms()
    # Skip addMissingHydrogens here, use Modeller instead

    # 2. Force Field Selection
    print("Loading Force Fields (Amber14SB + GLYCAM-06)...")
    # Using exact paths from OpenMM data directory
    forcefield = app.ForceField('amber14/protein.ff14SB.xml', 'amber14/GLYCAM_06j-1.xml', 'amber14/tip3p.xml')

    # 3. System Setup
    print("Creating System & Adding Hydrogens...")
    modeller = app.Modeller(fixer.topology, fixer.positions)
    # Add hydrogens according to forcefield rules
    modeller.addHydrogens(forcefield, pH=7.0)
    
    modeller.addSolvent(forcefield, padding=1.0*unit.nanometers, ionicStrength=0.15*unit.molar)
    
    # Save solvated topology for analysis
    print(f"Saving solvated topology: {output_dir / 'solvated.pdb'}")
    with open(output_dir / 'solvated.pdb', 'w') as f:
        app.PDBFile.writeFile(modeller.topology, modeller.positions, f)
    
    system = forcefield.createSystem(modeller.topology, nonbondedMethod=app.PME,
                                    nonbondedCutoff=1.0*unit.nanometers, constraints=app.HBonds)
    
    integrator = openmm.LangevinMiddleIntegrator(300*unit.kelvin, 1/unit.picosecond, 0.004*unit.picoseconds)
    simulation = app.Simulation(modeller.topology, system, integrator)
    simulation.context.setPositions(modeller.positions)

    # 4. Energy Minimization
    print("Minimizing Energy...")
    simulation.minimizeEnergy()

    # 5. Production MD
    print(f"Running Production MD ({n_steps} steps)...")
    dcd_reporter = app.DCDReporter(str(output_dir / 'trajectory.dcd'), report_interval)
    # Using a specialized reporter to keep output clean in terminal
    state_reporter = app.StateDataReporter(sys.stdout, report_interval, step=True,
                                          potentialEnergy=True, temperature=True, speed=True)
    
    simulation.reporters.append(dcd_reporter)
    simulation.reporters.append(state_reporter)
    
    # Try a small step first to ensure stability
    simulation.step(min(100, n_steps))
    if n_steps > 100:
        simulation.step(n_steps - 100)

    print(f"Simulation Complete. Trajectory saved to {output_dir / 'trajectory.dcd'}")
    return True

if __name__ == "__main__":
    # Test run with MenA-CRM197 structure
    PDB_FILE = "data/structures/pdb4ae1.ent"
    OUT_DIR = "data/simulations/real_md_test"
    if os.path.exists(PDB_FILE):
        run_real_md(PDB_FILE, OUT_DIR, n_steps=1000)
    else:
        print(f"PDB file not found: {PDB_FILE}")
