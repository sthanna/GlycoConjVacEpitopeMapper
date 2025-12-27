# Knowledge Update: Protein Language Models & Geometric Deep Learning
**Date**: 2025-12-26
**Agent**: ML Specialist

## Executive Summary
This update reviews the latest machine learning architectures for epitope prediction, specifically focusing on the transition from sequence-only models to structure-aware and multi-modal frameworks.

## Key Themes
1. **Dominance of ESM-2 & ProtBERT**:
   Pre-trained Protein Language Models (PLMs) like ESM-2 (up to 15B parameters) are now the de facto feature encoders. They capture evolutionary signatures that outperform standard amino acid encodings. Fine-tuning these models (Direct Preference Optimization - DPO) is being used to design proteins with reduced immunogenicity.

2. **Structure-Aware Prediction (Geometric DL)**:
   - **GraphBepi**: Uses AlphaFold2 structures to build protein graphs, which are processed via Edge-enhanced Graph Neural Networks (EGNNs).
   - **SageTCR**: Integrates residue- and atom-level representations for TCR-pMHC binding prediction.
   - **Patch-centric Frameworks**: Defining epitopes as surface "patches" (triads of residues) rather than linear segments significantly improves conformational B-cell epitope detection.

3. **Multi-Modal Integration**:
   Successful models now fuse PLM embeddings with:
   - **Molecular Dynamics (MD)** features (Interaction Power Spectra).
   - **Physicochemical descriptors** (Antigenicity indices, solvent accessibility).
   - **Retrieval-Augmented Generation (RAG)**: Using similarity search against known binders to augment the prediction embedding (e.g., RAG_MCNNIL6).

4. **Specific Outcome Predictors**:
   Recent tools specialize in predicting:
   - **Immunodominance Scores** (BIDpred).
   - **Cytokine Induction** (IL2pred, IL-13, IL-6 inducing epitopes).
   - **Neutralization Capacity** against viral variants (MambaAAI).

## Implications for Epitope Mapping Project
- We should use **ESM-2 (650M or 3B)** for all residue embeddings.
- Implement a **Graph Neural Network (GNN)** to process the AF3-predicted MenA-CRM197 structure.
- Integrate **RAG** into our inference pipeline to leverage the newly built vector stores.

---
*End of Update*