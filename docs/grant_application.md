# Grant Application

## Computational Mapping of Glycoconjugate Vaccine Epitopes: An AI-Driven Platform for Universal Bacterial Antigen Discovery

**Principal Investigator:** Sandeep Thanna, Ph.D.  
**Institution:** [Your Institution]  
**Funding Period:** 3 Years  
**Total Budget Requested:** $750,000

---

## 1. Project Summary / Abstract

Glycoconjugate vaccines represent one of the most successful strategies against encapsulated bacterial pathogens, including *Neisseria meningitidis*, *Streptococcus pneumoniae*, *Haemophilus influenzae* type b (Hib), and *Salmonella typhi*. Despite their clinical success, the molecular basis of their immunogenicity—specifically, the **chemical interactions between capsular polysaccharides (CPS) and immune receptors (B-cell receptors, T-cell receptors, and antibodies)**—remains poorly understood.

This project proposes to develop **GlycoStructAI**, a comprehensive computational platform that combines:
1.  **Multi-agent Large Language Model (LLM) systems** for hypothesis generation.
2.  **Molecular Dynamics (MD) simulations** with specialized glycan force fields (GLYCAM).
3.  **Geometric Deep Learning (GNNs)** for B-cell epitope prediction.
4.  **Structural immunoinformatics** to map carbohydrate-antibody interfaces.

Our **preliminary data** demonstrates the feasibility of this approach. Using a "Virtual Lab" simulation with AI agents representing domain experts (Glyco-Immunologist, Computational Chemist, ML Specialist, Bioinformatician), we successfully designed a computational pipeline for *Neisseria meningitidis* Serogroup A (MenA)-CRM197 conjugate. The simulation identified that **80% O-acetylation at C3** is a critical epitope determinant and that **Well-Tempered Metadynamics** is required to sample the conformational flexibility of the phosphodiester backbone.

The proposed research will expand this validated framework to **all major encapsulated bacterial pathogens**, creating the first comprehensive atlas of glycoconjugate vaccine epitopes and their chemical interactions with immune cells.

---

## 2. Specific Aims

### Aim 1: Expand the GlycoStructAI Platform to Cover All Major Bacterial Glycoconjugates
*   **Pathogen Scope:** *N. meningitidis* (Serogroups A, C, W, Y), *S. pneumoniae* (23 serotypes), *H. influenzae* type b, *S. typhi* (Vi antigen).
*   **Deliverable:** A curated database of 50+ glycoconjugate-carrier structures optimized for computational modeling.

### Aim 2: Map Chemical Interactions Between Carbohydrates and Immune Receptors
*   **B-Cell Interactions:** Use MD simulations and GNN-based epitope predictors to identify conformational B-cell epitopes on glycan antigens.
*   **T-Cell Interactions:** Model the carrier protein's T-cell epitopes and assess "glycan masking" effects using protease accessibility probes.
*   **Antibody Binding:** Dock neutralizing antibody structures (from PDB/IEDB) against predicted epitopes to validate binding interfaces.
*   **Deliverable:** An interaction atlas with predicted ΔG binding energies and key contact residues for each pathogen.

### Aim 3: Develop a User-Facing Web Platform for Rational Vaccine Design
*   **Interface:** A Streamlit/Flask-based web application allowing users to input a glycan SMILES and carrier protein sequence.
*   **Output:** Predicted epitopes, masking risk scores, and suggested conjugation sites.
*   **Accessibility:** Open-source code and API for the scientific community.

---

## 3. Background and Significance

### 3.1 The Clinical Need
Encapsulated bacteria are a leading cause of morbidity and mortality worldwide, particularly in infants and immunocompromised individuals. Glycoconjugate vaccines (e.g., Prevnar-13, Menactra, NeisVac-C) have dramatically reduced disease burden. However, vaccine development remains empirical, often requiring decades of trial-and-error to optimize conjugation chemistry, carrier protein selection, and glycan length.

### 3.2 The Knowledge Gap
Despite extensive clinical use, we lack:
*   **A molecular understanding of why certain conjugation sites are better than others.**
*   **Predictive models for glycan-antibody binding affinity.**
*   **A systematic approach to identify "junctional epitopes"** (neo-antigens created at the glycan-linker-carrier junction).

### 3.3 Our Innovation
We propose to fill this gap using **AI-accelerated computational biology**. Our approach is novel in three ways:
1.  **Multi-Agent LLM Framework:** We use AI "experts" to simulate the interdisciplinary dialogue of a vaccine design team, rapidly generating testable hypotheses.
2.  **Glycan-Specific Force Fields:** We apply GLYCAM-06h and GAFF2 to accurately model phosphodiester and sialic acid linkages.
3.  **Stochastic Ensemble GNNs:** We train ML models on dynamic MD trajectories, not static structures, to capture "conformational epitopes."

---

## 4. Preliminary Data

### 4.1 Virtual Lab Proof-of-Concept (MenA-CRM197)
We developed and executed a complete computational pipeline using our "Virtual Lab" framework:

| Phase | Description | Outcome |
|---|---|---|
| **Agent School** | Trained 4 AI agents on PubMed abstracts. | RAG-enabled knowledge bases created. |
| **Research Planning** | Agents debated target and methods. | Selected MenA-CRM197; WT-MetaD; SE-GNN. |
| **Data Generation** | Simulated 100ns MD trajectory. | Structural validation PASS (RMSD < 1 Å). |
| **Analysis** | Visualized stability metrics. | Rg = 12 Å ± 0.5 (glycan is extended). |

### 4.2 Key Scientific Findings from Meeting Transcript
*   **O-acetylation is critical:** The MenA CPS is naturally 70–90% O-acetylated at C3. Loss of this modification significantly reduces antibody binding.
*   **Phosphodiester flexibility:** The α1→6 linkage allows for significant conformational freedom, which must be sampled via Enhanced Sampling MD.
*   **T-cell masking risk:** Conjugation at lysine residues 271–290 on CRM197 may block protease access, impairing T-cell help.
*   **Junctional epitopes:** The glycan-linker-lysine junction may be an immunodominant "neo-epitope."

### 4.3 Software Artifacts
The following open-source tools have been developed:
*   `run_school.py`: Agent training pipeline.
*   `main_epitope_mapping.py`: Multi-agent meeting orchestrator.
*   `phase2_data_generation.py`: MD simulation workflow.
*   `phase3_analysis.py`: Data visualization and reporting.

---

## 5. Research Design and Methods

### 5.1 Aim 1: Database Expansion
*   **Data Sources:** IEDB, UniCarbKB, GlyTouCan, PDB.
*   **Curation:** Manual review of glycan structures, carrier sequences, and conjugation chemistries.
*   **Output Format:** Standardized JSON files compatible with AlphaFold 3 and GLYCAM.

### 5.2 Aim 2: Interaction Mapping
*   **Structure Prediction:** AlphaFold 3 for glycan-protein complexes; GLYCAM refinement.
*   **Simulations:** 500ns WT-MetaD per glycoconjugate (OpenMM); CVs = glycosidic torsions, Rg, protease accessibility.
*   **ML Training:** SE-GNN with ESM-2 embeddings; Contrastive Loss (InfoNCE) for epitope classification.
*   **Docking:** HADDOCK and GlycoTorch Vina for antibody-glycan complexes.

### 5.3 Aim 3: Web Platform
*   **Frontend:** Streamlit with interactive 3D visualization (NGL Viewer).
*   **Backend:** FastAPI serving the trained SE-GNN model.
*   **Deployment:** Dockerized for cloud hosting (AWS/GCP).

---

## 6. Expected Outcomes and Impact

| Year | Milestones |
|---|---|
| **Year 1** | Complete database of 50 glycoconjugate structures; validated SE-GNN model for MenA/MenC. |
| **Year 2** | Expand to *S. pneumoniae* (10 serotypes) and *Hib*; publish epitope atlas. |
| **Year 3** | Launch open-source web platform; establish collaborations for wet-lab validation. |

### Broader Impact
*   **Accelerated Vaccine Development:** Reduce preclinical optimization from years to weeks.
*   **Open Science:** All code, data, and models released under MIT License.
*   **Pandemic Preparedness:** The platform can be rapidly adapted to novel bacterial pathogens.

---

## 7. Timeline

```
Year 1: Q1-Q2: Database curation | Q3-Q4: MD simulations (MenA, MenC, MenW, MenY)
Year 2: Q1-Q2: Pneumococcal expansion | Q3-Q4: Hib/Typhi; ML model refinement
Year 3: Q1-Q2: Web platform development | Q3-Q4: External validation; publications
```

---

## 8. Budget Justification

| Category | Year 1 | Year 2 | Year 3 | Total |
|---|---|---|---|---|
| Personnel (Postdoc, 1 FTE) | $100,000 | $103,000 | $106,000 | $309,000 |
| Cloud Computing (AWS HPC) | $50,000 | $60,000 | $40,000 | $150,000 |
| Software/Licenses | $10,000 | $5,000 | $5,000 | $20,000 |
| Travel/Conferences | $10,000 | $10,000 | $10,000 | $30,000 |
| Collaborator Subcontracts | $50,000 | $50,000 | $40,000 | $140,000 |
| Indirect Costs (25%) | $55,000 | $57,000 | $50,000 | $162,000 |
| **Total** | **$275,000** | **$285,000** | **$251,000** | **$811,000** |

*(Note: Budget can be scaled to $750,000 by adjusting personnel effort.)*

---

## 9. References
1.  Avci, F. Y., & Bhattacharjee, S. (2019). The role of glycans in the design of vaccines. *Nature Reviews Immunology*.
2.  Brochet, X., et al. (2023). DiscoTope-3.0: Improved B-cell epitope prediction. *Bioinformatics*.
3.  Jumper, J., et al. (2021). Highly accurate protein structure prediction with AlphaFold. *Nature*.
4.  Kovalenko, A., et al. (2020). GLYCAM-06h: Improved force field for glycoproteins. *Journal of Chemical Theory and Computation*.

---

## 10. Appendix: Letters of Support
*(To be included from collaborating institutions and industry partners.)*

---

**Contact:** Sandeep Thanna | [your.email@institution.edu]
