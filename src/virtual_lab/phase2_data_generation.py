import time
import os
from pathlib import Path
from virtual_lab.agent import Agent
from virtual_lab.constants import DEFAULT_MODEL, CONSISTENT_TEMPERATURE
from virtual_lab.synthetic_data_generator import SyntheticDataGenerator
from virtual_lab.run_meeting import run_meeting
from virtual_lab.prompts import (
    SCIENTIFIC_CRITIC,
)

# Setup paths
DATA_DIR = Path("data")
PHASE2_OUTPUT_DIR = DATA_DIR / "phase2_outputs"
TRANSCRIPT_PATH = DATA_DIR / "transcript_phase2.txt"

def main():
    print("=== Initializing Phase 2: Data Generation & Simulation ===")
    
    # 1. Initialize Agents
    # We re-initialize them to ensure fresh state or explicitly load previous context if needed.
    # For Phase 2, we assume they "know" phase 1 happened via the context we pass or just implicit role continuity.
    
    # Define Agents (Same system prompts as main_epitope_mapping, effectively)
    # Note: In a real app complexity, we'd have a factory. Here we just re-instantiate.
    
    pi = Agent("Prof. Miller", "Principal Investigator", "Lead the team...", model_name=DEFAULT_MODEL) 
    # Use simple system prompts for now, leveraging their RAG knowledge bases in practice.
    # For this simulation script, we expect them to react to data.
    
    # Reuse the same RAG initialization logic? 
    # To save time/complexity for this specific script, we will just instantiate them with their specific roles
    # as defined in their basic prompt structure, but we won't re-load the heavy VectorStore info 
    # unless strictly necessary for "research". 
    # Phase 2 is about reaction to specific outputs.
    # Let's give them robust system prompts.
    
    # Simplified instantiation for Phase 2 execution focus
    alice = Agent("Alice", "Glyco-Immunologist", "Expert in immunology...", model_name=DEFAULT_MODEL)
    bob = Agent("Bob", "Computational Chemist", "Expert in MD and structure...", model_name=DEFAULT_MODEL)
    charlie = Agent("Charlie", "ML Specialist", "Expert in machine learning...", model_name=DEFAULT_MODEL)
    diana = Agent("Diana", "Bioinformatician", "Expert in biological data...", model_name=DEFAULT_MODEL)
    
    team = [alice, bob, charlie, diana]
    
    print("Agents initialized. Starting Simulation Workflow.")
    
    # Generator
    sim_gen = SyntheticDataGenerator(PHASE2_OUTPUT_DIR)
    
    # TRANSCRIPT ACCUMULATION
    full_transcript = []

    # --- STAGE 1: Structural Setup & Validation ---
    print("\n--- [System] Status: Running AlphaFold 3 & GLYCAM Geometry Check ---")
    time.sleep(2) # Simulate work
    
    report = sim_gen.generate_structure_validation_report()
    report_str = f"System Notification: Structural Validation Report Generated:\\n{report}"
    
    print(f"Report Generated: {report['glycan_geometry_check']['status']}")
    
    # Mini-meeting / Reaction
    agenda_stage1 = (
        "Review the AlphaFold 3 vs GLYCAM validation report. "
        "Bob, analyze the RMSD. Diana, check the alignment errors. "
        "Decide if we proceed to production MD or need regrafting."
    )
    
    summary_s1 = run_meeting(
        meeting_type="team",
        agenda=agenda_stage1,
        save_dir=DATA_DIR,
        save_name="phase2_stage1_discussion",
        team_lead=pi,
        team_members=(alice, bob, charlie, diana),
        contexts=[report_str],
        num_rounds=1,
        return_summary=True
    )
    
    full_transcript.append(f"--- STAGE 1: STRUCTURE VALIDATION ---\n{summary_s1}\n")
    
    # --- STAGE 2: Metadynamics (WT-MetaD) ---
    print("\n--- [System] Status: Launching Well-Tempered Metadynamics (OpenMM) ---")
    print("Simulating 100ns run...")
    
    # Simulate partial progress log
    log_file = sim_gen.generate_md_trajectory_log(num_frames=50) # First 50ns
    
    # Read last few lines to give "live" status
    with open(log_file, 'r') as f:
        lines = f.readlines()
        recent_logs = "".join(lines[-5:])
    
    live_update = f"System Notification: MD Simulation Progress (50%). Recent Log:\\n{recent_logs}"
    
    print("50% Completed. Agents discussing stability...")
    
    agenda_stage2 = (
        "Review the mid-run MD logs. "
        "Alice, does the Rg indicate glycan collapse? "
        "Bob, is the system stable? "
        "Charlie, is the sampling density sufficient for the GNN?"
    )
    
    summary_s2 = run_meeting(
        meeting_type="team",
        agenda=agenda_stage2,
        save_dir=DATA_DIR,
        save_name="phase2_stage2_discussion",
        team_lead=pi,
        team_members=(alice, bob, charlie, diana),
        contexts=[live_update],
        num_rounds=1,
        return_summary=True
    )
    
    full_transcript.append(f"--- STAGE 2: MD DYNAMICS CHECK ---\n{summary_s2}\n")
    
    # --- STAGE 3: Final Data Packaging ---
    print("\n--- [System] Status: Simulation Completed. Packaging Data. ---")
    time.sleep(1)
    
    agenda_stage3 = (
        "The simulation phase is complete. "
        "Confirm data integrity for Phase 3 (Analysis). "
        "Adjourn Phase 2."
    )
    
    summary_s3 = run_meeting(
        meeting_type="team",
        agenda=agenda_stage3,
        save_dir=DATA_DIR,
        save_name="phase2_stage3_discussion",
        team_lead=pi,
        team_members=(alice, bob, charlie, diana),
        num_rounds=1,
        return_summary=True
    )
    
    full_transcript.append(f"--- STAGE 3: CONCLUSION ---\n{summary_s3}\n")
    
    # Save Full Transcript
    with open(TRANSCRIPT_PATH, 'w') as f:
        f.write("\n\n".join(full_transcript))
        
    print(f"\n=== Phase 2 Completed. Transcript saved to {TRANSCRIPT_PATH} ===")

if __name__ == "__main__":
    main()
