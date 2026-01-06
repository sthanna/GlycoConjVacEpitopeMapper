# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
import yaml
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

# Import Agent
from virtual_lab.agent import Agent
from virtual_lab.meetings import run_team_meeting
from agent_schools.prompts import VIRTUAL_LAB_SYSTEM_PROMPT, PI_SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT

def load_curriculum(role_name: str) -> str:
    """Load the curriculum yaml for a given role to inject into their persona."""
    filename = f"{role_name.lower().replace('-', '_').replace(' ', '_')}_curriculum.yaml"
    path = Path("src/agent_schools") / filename
    try:
        with open(path, "r") as f:
            data = yaml.safe_load(f)
        # Summarize topics for the prompt
        topics = data.get("foundational", {}).get("topics", []) + \
                 data.get("intermediate", {}).get("topics", []) + \
                 data.get("advanced", {}).get("topics", [])
        return f"Certified Expert in: {', '.join(topics)}"
    except FileNotFoundError:
        return "Expert in the field."

def main():
    print("=== Initializing Virtual Lab for Epitope Mapping (Gemini Powered) ===")

    # 1. Initialize Agents
    pi = Agent(
        name="Prof. Miller", 
        role="Principal Investigator", 
        system_prompt=PI_SYSTEM_PROMPT
    )
    
    critic = Agent(
        name="Dr. S", 
        role="Scientific Critic", 
        system_prompt=CRITIC_SYSTEM_PROMPT
    )

    specialists = []
    roles = ["Glyco-Immunologist", "Computational Chemist", "ML Specialist", "Bioinformatician"]
    names = ["Alice", "Bob", "Charlie", "Diana"]

    ROLE_TO_KB = {
        "Glyco-Immunologist": "data/knowledge_base/indexes/glyco_immunologist",
        "Computational Chemist": "data/knowledge_base/indexes/computational_chemist",
        "ML Specialist": "data/knowledge_base/indexes/ml_specialist",
        "Bioinformatician": "data/knowledge_base/indexes/bioinformatician"
    }

    for name, role in zip(names, roles):
        curriculum_summary = load_curriculum(role)
        prompt = VIRTUAL_LAB_SYSTEM_PROMPT.format(
            role=role, 
            persona_description=f"You are {name}. {curriculum_summary}"
        )
        kb_path = ROLE_TO_KB.get(role)
        agent = Agent(name=name, role=role, system_prompt=prompt, kb_path=kb_path)
        specialists.append(agent)
        print(f"Initialized {role}: {name} (RAG: {'ON' if kb_path else 'OFF'})")

    # 2. Define Meeting Context
    try:
        with open("project_specification.md", "r") as f:
            spec = f.read()
    except FileNotFoundError:
        spec = "Project Specification not found. Using default goals."

    agenda = f"""
    PHASE 1 RESEARCH PLANNING: SCOPE AND TARGETS
    Review the Project Specification below. We must define the functional scope for the Virtual Lab.
    
    ---
    {spec}
    ---
    
    Objectives:
    1. Select the specific Glycoconjugate Vaccine target (e.g., MenA, MenC, Pneumococcal).
    2. Determine if we focus on single or multiple serotypes initially.
    3. Define the validation metrics (e.g., IEDB recovery rate, structural stability scores).

    Questions:
    1. What is the clinical/scientific motivation for the chosen target?
    2. What prior epitope data exists in IEDB for this target?
    3. What structural data is available (PDB IDs)?
    """

    # 3. Run Planning Meeting
    print("\n=== Compiling Team Meeting ===")
    
    try:
        summary, transcript = run_team_meeting(
            agents=specialists,
            critic=critic,
            pi=pi,
            agenda=agenda,
            rounds=2
        )

        # 4. Save Transcript
        output_dir = Path("data")
        output_dir.mkdir(exist_ok=True)
        
        with open(output_dir / "meeting_transcript_001.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                role = entry.get('role', 'unknown')
                name = entry.get('name', 'System')
                content = entry.get('content', '')
                f.write(f"[{role}] {name}: {content}\n\n")
        
        print("\nMeeting saved to data/meeting_transcript_001.txt")
        
    except Exception as e:
        print(f"\nSimulation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
