import yaml
import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

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
    print("=== Phase 2: Team Meeting 2 - Tool & Pipeline Design ===")

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
        "Glyco-Immunologist": "data/knowledge_base/glyco_immunologist/vector_index",
        "Computational Chemist": "data/knowledge_base/computational_chemist/vector_index",
        "ML Specialist": "data/knowledge_base/ml_specialist/vector_index",
        "Bioinformatician": "data/knowledge_base/bioinformatician/vector_index"
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
        print(f"Initialized {role}: {name} (RAG: {'ON' if kb_path and os.path.exists(kb_path) else 'OFF'})")

    # 2. Define Meeting Context & Agenda
    # We reference the decisions from Meeting 1
    previous_decisions = """
    PREVIOUS DECISIONS (Meeting 1 & Audit):
    1. Target: Neisseria meningitidis Serogroup A (MenA).
    2. Carrier: CRM197 (PDB: 4AE1).
    3. Glycan: (alpha1->6)-linked N-acetyl-D-mannosamine-1-phosphate.
    4. Key Constraint: Must account for O-acetylation (C3/C4) and Phosphate linkage.
    5. Safety: Avoid T-cell epitope regions on CRM197 (271-290, 321-340, 411-430).
    """

    agenda = f"""
    TEAM MEETING 2: TOOL & PIPELINE DESIGN
    
    {previous_decisions}
    
    **Objective:** Select the specific tools and architect the computational pipeline.
    
    **Agenda Items:**
    1.  **Structure Modeling:** 
        -   How do we attach the MenA glycan to CRM197? (Rosetta vs. Amber/GLYCAM?)
        -   How do we simulate the flexibility of the phosphate backbone?
    2.  **Feature Extraction:**
        -   What node features capture the "phosphate cloud"?
        -   Sequence embeddings (ESM-2) vs. Structural embeddings (GNN).
    3.  **Machine Learning Architecture:**
        -   Propose the specific architecture (e.g., Graph Attention Network vs SE(3)-Transformer).
        -   Define the Input/Output tensor shapes.
    
    **Deliverable:** A consensus "Pipeline Architecture" listing the exact tools and data flow.
    """

    # 3. Run Team Meeting
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
        
        with open(output_dir / "meeting_transcript_pipeline_design.txt", "w", encoding="utf-8") as f:
            for entry in transcript:
                role = entry.get('role', 'unknown')
                name = entry.get('name', 'System')
                content = entry.get('content', '')
                f.write(f"[{role}] {name}: {content}\n\n")
        
        print("\nMeeting saved to data/meeting_transcript_pipeline_design.txt")
        
    except Exception as e:
        print(f"\nSimulation Failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
