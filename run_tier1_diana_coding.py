import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from virtual_lab.agent import Agent
from virtual_lab.meetings import run_individual_meeting
from agent_schools.prompts import VIRTUAL_LAB_SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT

def main():
    print("=== Phase 3: Coding Session - Diana (Bioinformatician) ===")
    
    # 1. Initialize Agents
    critic = Agent(
        name="Dr. S", 
        role="Scientific Critic", 
        system_prompt=CRITIC_SYSTEM_PROMPT
    )

    role = "Bioinformatician"
    name = "Diana"
    kb_path = f"data/knowledge_base/bioinformatician/vector_index"
    
    prompt = VIRTUAL_LAB_SYSTEM_PROMPT.format(
        role=role, 
        persona_description=f"You are {name}, an expert Python developer and Bioinformatician. You specialize in BioPython, structural analysis, and algorithm design."
    )
    
    bioinformatician = Agent(
        name=name, 
        role=role, 
        system_prompt=prompt, 
        kb_path=kb_path
    )
    print(f"Initialized {name} (RAG: {'ON' if os.path.exists(kb_path) else 'OFF'})")

    # 2. Define Coding Task
    task = """
    CODING TASK: Implement Tier 1 Screening Script for CRM197
    
    **Objective:** Write a complete, runnable Python script (`src/virtual_lab/bioinformatics/crm197_screening.py`) that filters potential conjugation sites on CRM197 (PDB: 4AE1).
    
    **Specifications:**
    1.  **Input:** PDB file `data/structures/pdb4ae1.ent`.
    2.  **Protected Presentation Zones (PPZs):** defined as residues [271-290, 321-340, 411-430].
    3.  **Logic:**
        -   Parse the PDB structure using `Bio.PDB`.
        -   Identify all surface Lysine residues (Residue name 'LYS').
        -   Calculate the minimum distance from each Lysine's centroid (NZ atom preferred) to any atom in the PPZs.
        -   Filter out any Lysine where `min_distance < 15.0` Angstroms.
        -   Calculate Solvent Accessible Surface Area (SASA) using `Bio.PDB.SASA` (Shrake-Rupley) for the remaining Lysines.
        -   Rank the passing Lysines by SASA (High to Low).
    4.  **Output:** Print a table of "Top Candidate Sites" with their Residue ID, PPZ Distance, and SASA.
    
    **Constraint:** Return ONLY the Python code block.
    """

    # 3. Run Session
    try:
        final_code, transcript = run_individual_meeting(
            agent=bioinformatician,
            critic=critic,
            task_description=task,
            rounds=1 # Quick coding round
        )
        
        # 4. Save Transcript (for record)
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        with open(output_dir / "coding_session_diana.txt", "w", encoding="utf-8") as f:
             for entry in transcript:
                role = entry.get('role', 'unknown')
                content = entry.get('content', '')
                f.write(f"[{role}]: {content}\n\n")

        print("\nCoding session complete.")
        
    except Exception as e:
        print(f"\nSimulation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
