# GlycoConjVacEpitopeMapper
**Mapping Conformational Epitopes on Glycoconjugate Vaccines using Virtual Lab Agents**

## Overview
This repository contains the `GlycoConjVacEpitopeMapper` project, a comprehensive multi-agent system designed to optimize glycoconjugate vaccine design. It integrates **Agentic AI**, **Structural Bioinformatics** (AlphaFold 3/Boltz-1), and **Deep Learning** (ESM-2) to identify optimal B-cell epitopes on molecular scaffolds.

## Repository Structure
- `src/virtual_lab`: Core logic for `Agent` class, RAG retrieval, and meeting orchestration.
- `src/agent_schools`: Curricula and vector store builders for training agents.
- `src/virtual_lab/epitope_mapping`: Modules for structural analysis (PDB), feature extraction (ESM-2), and predictive modeling.
- `data/knowledge_base`: Local FAISS vector stores containing "graduated" agent knowledge.
- `data/structures`: Raw PDB files (e.g., CRM197).
- `data/meeting_transcript_*.txt`: Logs of multi-agent planning sessions.

## Key Features
- **Multi-Agent RAG**: Agents (Glyco-Immunologist, Chemist, ML Specialist, Bioinformatician) query localized knowledge bases during collaboration.
- **Evo-Struct Pipeline**: Combines evolutionary sequence conservation (pan-genome) with 3D structural mapping.
- **Gym-to-Lab**: Agents undergo a "School" phase (reading PubMed abstracts) before entering the "Virtual Lab" (executing code).
- **Gemini Powered**: Uses Google's Gemini (via `google-generativeai`) for stateful reasoning.

## Installation
1.  **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/GlycoConjVacEpitopeMapper.git
    cd GlycoConjVacEpitopeMapper
    ```

2.  **Set up Conda Environment**:
    ```bash
    conda env create -f environment.yml
    conda activate epitope_mapping
    ```

3.  **Install Python Dependencies**:
    ```bash
    pip install .
    # Or for editable mode
    pip install -e .
    ```

4.  **Configuration**:
    - Update `src/virtual_lab/constants.py` with your **Gemini API Key**.
    - Ensure `data/knowledge_base/` is populated (run `run_indexing.py` if needed).

## Usage
- **Run a Team Meeting**:
    ```bash
    python src/virtual_lab/main_epitope_mapping.py
    ```
- **Train the Epitope Predictor**:
    ```bash
    python src/virtual_lab/epitope_mapping/train.py
    ```

## License
MIT License
