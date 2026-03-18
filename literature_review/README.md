# Systematic Literature Review: GlycoConjugate Vaccine Epitope Identification

*Generated 2026-03-18 using the `systematic-review-automation` skill*

## Overview

A systematic review of the scientific literature on epitope identification methods for glycoconjugate vaccines, conducted to inform the computational pipeline design in this repository.

## PICO Framework

| Component | Definition |
|---|---|
| **P** – Population | Glycoconjugate vaccines (polysaccharide-protein conjugates, bioconjugates, CPS-based vaccines) |
| **I** – Intervention | Epitope identification / mapping methods (B-cell, T-cell, structural, computational) |
| **C** – Comparison | Not applicable (discovery/methods review) |
| **O** – Outcome | Protective epitopes, immunogenicity, OPA, seroconversion, antibody avidity |

## Search Summary

| Parameter | Value |
|---|---|
| Databases | PubMed, OpenAlex, Semantic Scholar, bioRxiv/medRxiv |
| Date | 2026-03-18 |
| Raw records | 575 |
| After deduplication | 567 |
| Title/Abstract excluded | 328 |
| Full texts assessed | 239 |
| **Studies included** | **50** |

## Directory Structure

```
literature_review/
├── README.md                  — this file
├── figures/
│   └── prisma_flow.png        — PRISMA 2020 flow diagram
└── results/
    ├── review_report.md       — full narrative review with themes & gaps
    ├── evidence_table.csv     — 60 papers with metadata & relevance scores
    ├── screened.json          — all screening decisions with rationale
    ├── deduplicated.json      — post-dedup records
    ├── raw_results.json       — raw harvest from all databases
    └── search_log.json        — reproducible search provenance log
```

## Key Findings

### 1. Carbohydrate B-cell Epitopes
Primary methods: STD-NMR, glycan microarrays, cryo-EM of Fab–oligosaccharide complexes. Conformational presentation of polysaccharide antigens is critical — repeat unit number and O-acetylation status directly modulate epitope accessibility.

### 2. T-cell Help via Carrier Proteins
CRM197, tetanus toxoid (TT), and diphtheria toxoid (DT) provide MHC-II-restricted T-helper epitopes. In-cell depolymerization of polysaccharide antigens determines glycan fragment presentation — key mechanistic insight for vaccine design.

### 3. Computational Epitope Prediction (Emerging)
AlphaFold3 and ESM-2 are beginning to be applied to glycoprotein structure prediction, though polysaccharide flexibility remains a challenge. Molecular dynamics simulations provide conformational sampling of PS antigens. This is the primary gap this repository addresses.

### 4. Fully Synthetic Vaccines (2024–2026)
Chemical synthesis of defined oligosaccharides enables precise epitope definition. Recent examples: *Pseudomonas aeruginosa*, *S. aureus*, *Acinetobacter baumannii* synthetic glycoconjugate vaccines with defined minimal epitopes.

### 5. Functional Correlates
- OPA (opsonophagocytic activity) — gold standard for protective antibody assessment
- Bactericidal assays — complement-dependent killing
- Avidity index — antibody maturation quality post-vaccination

## Research Gaps (Informing This Repo)

1. **No consensus on minimal protective saccharide length** across pathogens
2. **Cryo-EM structural data for PS-antibody complexes** remains sparse vs. protein antigens
3. **No dedicated AI/ML tools for carbohydrate epitope prediction** — AlphaFold doesn't natively model polysaccharides
4. **Cross-reactive epitopes understudied** — potential for broader-spectrum vaccine design
5. **Neonatal/pediatric immune responses** differ from adults; limited epitope data

## Top Cited Papers

| # | Title | Year | Citations |
|---|---|---|---|
| 1 | Glycoconjugate vaccines: Principles and mechanisms | 2018 | 248 |
| 2 | Discovery of Semi- and Fully-Synthetic Carbohydrate Vaccines Against Bacterial Infections | 2021 | 189 |
| 3 | Vaccines based on the cell surface carbohydrates of pathogenic bacteria | 2005 | 180 |
| 4 | Protein Carriers for Glycoconjugate Vaccines: History, Selection Criteria, Characterization | 2018 | 108 |
| 5 | Carbohydrates as T-cell antigens with implications in health and disease | 2016 | 84 |
| 6 | Role of O-Acetylation in the Immunogenicity of Bacterial Polysaccharide Vaccines | 2018 | 78 |
| 7 | Recent advances on smart glycoconjugate vaccines in infections and cancer | 2021 | 64 |

## Methodology

Automated using the [`systematic-review-automation`](https://github.com/sthanna/claude-scientific-skills) AgentSkill:
- Multi-database harvest via PubMed E-utilities + OpenAlex REST API
- Fuzzy deduplication (rapidfuzz, threshold 0.92 title similarity + DOI/PMID exact match)
- PICO-based relevance scoring (weighted keyword matching across population, intervention, outcome domains)
- PRISMA 2020 flow diagram auto-generated from search logs
