# Bioinformatics Tools for Glycoconjugate Vaccine Epitope Mapping

Research conducted on 2026-01-04 identified the following open-source tools as critical for the project:

## 1. B-Cell Epitope Prediction (Structure-Based)
*   **DiscoTope-3.0**: The leading open-source tool for predicting conformational B-cell epitopes. It uses inverse folding and AlphaFold structures. Best for mapping epitopes on the protein carrier (CRM197).
*   **ElliPro**: Integrated into IEDB, predicts discontinuous epitopes based on geometry and solvent accessibility.

## 2. Molecular Dynamics (Glycoproteins)
*   **GROMACS**: High-performance MD engine.
*   **GLYCAM**: The standard force field for simulating carbohydrates and glycoproteins. Essential for modeling the flexibility of the glycan antigen and the linker.
*   **NAMD**: Alternative scalable MD engine compatible with GLYCAM.

## 3. Protein-Glycan Docking
*   **HADDOCK**: Supports protein-carbohydrate docking. Critical for modeling antibody binding to the glycoconjugate.
*   **AutoDock Vina**: Can be adapted for glycan ligands.
*   **GlycoTorch Vina**: Specialized variant for glycans.

## 4. Glycan Modeling
*   **CHARMM-GUI Glycan Reader**: Web-based tool to build glycan structures and generate input files for GROMACS/NAMD.

## 5. Neisseria meningitidis Specifics
*   **IEDB**: The Immune Epitope Database contains specific epitope data for *N. meningitidis* serogroups (MenA, MenC, etc.) which should be used to validate predictions.
