# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------

import sys

def verify_environment():
    print("=== Virtual Lab: Real MD Environment Verification ===")
    
    missing = []
    
    # Check Python Version
    print(f"Python: {sys.version.split()[0]}")
    
    # Check OpenMM
    try:
        import openmm
        print(f"OpenMM: {openmm.__version__}")
    except ImportError:
        print("OpenMM: [NOT FOUND]")
        missing.append("openmm")
        
    # Check MDTraj
    try:
        import mdtraj
        print(f"MDTraj: {mdtraj.__version__}")
    except ImportError:
        print("MDTraj: [NOT FOUND]")
        missing.append("mdtraj")
        
    # Check Torch
    try:
        import torch
        print(f"Torch: {torch.__version__}")
    except ImportError:
        print("Torch: [NOT FOUND]")
        missing.append("torch")
        
    # Check PDBFixer
    try:
        import pdbfixer
        print("PDBFixer: Installed")
    except ImportError:
        print("PDBFixer: [NOT FOUND]")
        missing.append("pdbfixer")

    print("---")
    if not missing:
        print("SUCCESS: All critical Real MD dependencies are present!")
    else:
        print(f"FAILURE: Missing dependencies: {', '.join(missing)}")
        print("Please ensure the conda environment is correctly activated and updated.")

if __name__ == "__main__":
    verify_environment()
