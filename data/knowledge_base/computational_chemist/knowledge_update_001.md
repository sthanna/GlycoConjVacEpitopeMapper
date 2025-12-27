# Knowledge Update: Advanced Glycoprotein Modeling & AlphaFold 3 Integration
**Date**: 2025-12-26
**Agent**: Computational Chemist

## Executive Summary
This update synthesizes recent breakthroughs in structural biology, specifically the synergy between AlphaFold 3 (AF3) and experimental techniques like cryo-EM and HDX-MS for modeling complex glycoproteins and their interactions.

## Key Themes
1. **AlphaFold 3 & Multimer Modeling**:
   AF3 has revolutionized the prediction of protein-protein and protein-ligand interactions. It is now being used to model complex trimolecular assemblies (e.g., FV-Short/TFPIα/protein S) and to predict the structural impact of missense variants (e.g., L1CAM salt-bridge disruption) with high precision.

2. **Integrative Structural Biology**:
   The combination of predictive models with experimental data is the new standard.
   - **HDX-MS + AF3**: Used to map the conformational landscape of intrinsically disordered regions in proteins like Histidine-rich glycoprotein (HRG).
   - **Cryo-EM + AF3**: High-resolution maps allow for unambiguous assignment of flexible loops and disordered N-termini (e.g., HSV-2 gC-C3b complex).

3. **Glycan & Lipid Modeling Challenges**:
   - **GlycoShape & Re-Glyco**: New open-access tools enable the restoration of glycosylation to AF3 models in seconds, covering the human glycome.
   - **Lipid Affinity**: AF3 accurately predicts β-barrel folds (e.g., Fibrillins) and identifies specific lipid-binding cavities, crucial for understanding membrane-associated glycoproteins.

4. **Dynamic Simulations & Allostery**:
   Advanced MD simulations (GROMACS/Schrödinger) are vital for validating AF3-predicted "hydrolock" mechanisms and allosteric communications in viral spikes (e.g., SARS-CoV-2 XBB lineages).

## Implications for Epitope Mapping Project
- We must use **AlphaFold 3** for the MenA-CRM197 covalent linkage model.
- **GlycoShape** should be used to add the MenA trimer to the CRM197 carrier.
- We should monitor **salt-bridge stability** and **hydrophobic patches** as key indicators of epitope accessibility.

---
*End of Update*