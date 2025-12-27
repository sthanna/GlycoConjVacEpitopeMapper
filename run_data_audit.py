import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from virtual_lab.agent import Agent
from virtual_lab.meetings import run_individual_meeting
from agent_schools.prompts import VIRTUAL_LAB_SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT

def main():
    print("=== Phase 1: Individual Meeting 1 - Data Audit ===")
    
    # 1. Initialize Agents
    critic = Agent(
        name="Dr. S", 
        role="Scientific Critic", 
        system_prompt=CRITIC_SYSTEM_PROMPT
    )

    # Bioinformatician Setup
    # Load brief curriculum context
    role = "Bioinformatician"
    name = "Diana"
    kb_path = f"data/knowledge_base/bioinformatician/vector_index"
    
    prompt = VIRTUAL_LAB_SYSTEM_PROMPT.format(
        role=role, 
        persona_description=f"You are {name}, a Bioinformatician specializing in vaccine databases (IEDB), structural data (PDB), and sequence analysis."
    )
    
    bioinformatician = Agent(
        name=name, 
        role=role, 
        system_prompt=prompt, 
        kb_path=kb_path
    )
    print(f"Initialized {name} (RAG: {'ON' if os.path.exists(kb_path) else 'OFF'})")

    # 2. Define Agenda from Strategy Doc
    agenda = """
    INDIVIDUAL MEETING: DATA AUDIT
    
    **Objective:** Perform a comprehensive audit of available data for the chosen target: **Neisseria meningitidis Serogroup A (MenA)** and **CRM197**.
    
    **Tasks:**
    1.  **IEDB Query Strategy:** Define how you will query the Immune Epitope Database for MenA. 
        -   Specific search terms (Organism ID: 487 for MenA?).
        -   How to handle the "glycan vs protein" distinction in IEDB.
    2.  **Structural Constraints:**
        -   Confirm PDB IDs for CRM197 (e.g., 4AE1, 5I82).
        -   Identify any existing glycan co-crystals or homologs (e.g., other Neisseria serogroups).
    3.  **Gap Analysis:** What is missing? Do we have enough data to train a model?
    
    **Output:** A structured "Data Audit Report" listing available datasets and defining the "Training Set" vs "Test Set" strategy.
    """

    # 3. Run Meeting
    try:
        summary, transcript = run_individual_meeting(
            agent=bioinformatician,
            critic=critic,
            task_description=agenda,  # Fixed argument name
            rounds=2
        )
        
        # 4. Save Transcript
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "meeting_transcript_data_audit.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                role = entry.get('role', 'unknown')
                name = entry.get('name', 'System')
                content = entry.get('content', '')
                f.write(f"[{role}] {name}: {content}\n\n")
        
        print("\nMeeting saved to data/meeting_transcript_data_audit.txt")
        
    except Exception as e:
        print(f"\nSimulation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    # Ensure UTF-8 output
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
