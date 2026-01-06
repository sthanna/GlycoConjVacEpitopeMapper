---
description: Run the complete Virtual Lab (School -> Phase 1 -> Phase 2 -> Phase 3)
---

This workflow executes the entire End-to-End simulation for the Glycoconjugate Vaccine Project.

1. **Install Dependencies**
   Ensure all Python requirements are met.
   ```bash
   pip install google-generativeai langchain-community sentence-transformers faiss-cpu torch matplotlib pandas
   ```

2. **Run Agent School**
   Educate the agents and build knowledge bases.
   ```bash
   // turbo
   $env:PYTHONPATH="src"; python src/agent_schools/run_school.py
   ```

3. **Run Phase 1: Research Planning**
   Execute the main simulation to plan the vaccine design.
   ```bash
   // turbo
   $env:PYTHONPATH="src"; python src/virtual_lab/main_epitope_mapping.py
   ```

4. **Run Phase 2: Data Generation**
   Simulate AlphaFold 3 validation and Metadynamics.
   ```bash
   // turbo
   $env:PYTHONPATH="src"; python src/virtual_lab/phase2_data_generation.py
   ```

5. **Run Phase 3: Analysis & Reporting**
   Generate trajectory plots and the final report.
   ```bash
   // turbo
   $env:PYTHONPATH="src"; python src/virtual_lab/phase3_analysis.py
   ```
