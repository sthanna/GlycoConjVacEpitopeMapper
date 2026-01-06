import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from virtual_lab.agent import Agent
from virtual_lab.constants import DEFAULT_MODEL
from virtual_lab.run_meeting import run_meeting

# Setup paths
DATA_DIR = Path("data")
PHASE2_OUTPUT_DIR = DATA_DIR / "phase2_outputs"
TRAJECTORY_CSV = PHASE2_OUTPUT_DIR / "trajectory_log.csv"
PLOT_PATH = PHASE2_OUTPUT_DIR / "trajectory_plot.png"
FINAL_REPORT_PATH = DATA_DIR / "final_simulation_report.md"
TRANSCRIPT_PATH = DATA_DIR / "transcript_phase3.txt"

def analyze_and_plot():
    """Reads the CSV, generating a summary and a plot."""
    print(f"Reading data from {TRAJECTORY_CSV}...")
    df = pd.read_csv(TRAJECTORY_CSV)
    
    # 1. Generate Statistics
    stats = df.describe().to_string()
    
    # 2. Generate Plot
    print("Generating trajectory plot...")
    fig, ax1 = plt.subplots(figsize=(10, 6))

    color = 'tab:red'
    ax1.set_xlabel('Time (ns)')
    ax1.set_ylabel('Potential Energy (kJ/mol)', color=color)
    ax1.plot(df['Time_ns'], df['PotentialEnergy_kJ_mol'], color=color, label='Energy')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('Rg (Angstrom)', color=color)  # we already handled the x-label with ax1
    ax2.plot(df['Time_ns'], df['Rg_MenA_Angstrom'], color=color, linestyle='--', label='Rg')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title("MenA-CRM197 Simulation Trajectory: Energy vs Stability (Rg)")
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(PLOT_PATH)
    print(f"Plot saved to {PLOT_PATH}")
    
    return stats

def main():
    print("=== Initializing Phase 3: Analysis & Reporting ===")
    
    # 1. Run Data Analysis
    try:
        data_summary = analyze_and_plot()
    except Exception as e:
        print(f"Error during analysis: {e}")
        data_summary = "Error loading data. Assume simulation failed or data corrupted."

    # 2. Initialize Agents for Final Review
    pi = Agent("Prof. Miller", "Principal Investigator", "Lead the team...", model_name=DEFAULT_MODEL)
    alice = Agent("Alice", "Glyco-Immunologist", "Expert in immunology...", model_name=DEFAULT_MODEL)
    bob = Agent("Bob", "Computational Chemist", "Expert in MD and structure...", model_name=DEFAULT_MODEL)
    charlie = Agent("Charlie", "ML Specialist", "Expert in machine learning...", model_name=DEFAULT_MODEL)
    diana = Agent("Diana", "Bioinformatician", "Expert in biological data...", model_name=DEFAULT_MODEL)
    
    team = [alice, bob, charlie, diana]
    
    # 3. Conduct Final Reporting Meeting
    print("\n--- [System] Status: Convening Final Team Meeting ---")
    
    agenda = (
        "Review the Phase 2 simulation data (Summary Stats provided). "
        "Discuss the stability of the MenA-CRM197 complex based on the Radius of Gyration (Rg). "
        "Draft the conclusions for the Final Report. "
        "Each specialist must provide one key finding."
    )
    
    # We pass the data summary as context
    context = f"Simulation Data Summary:\n{data_summary}\n\n(A plot has also been generated at {PLOT_PATH})"
    
    meeting_summary = run_meeting(
        meeting_type="team",
        agenda=agenda,
        save_dir=DATA_DIR,
        save_name="phase3_final_discussion",
        team_lead=pi,
        team_members=tuple(team),
        contexts=[context],
        num_rounds=1,
        return_summary=True
    )
    
    # 4. Generate Final Report (Using the PI to synthesize)
    print("\n--- [System] Status: Generating Final Report Document ---")
    
    report_prompt = (
        f"Based on the following team discussion, write a comprehensive 'Final Simulation Report' in Markdown format.\n"
        f"Include sections: Executive Summary, Methodology, Key Findings (Structure, Dynamics, Immunology), and Future Directions.\n\n"
        f"Discussion Transcript:\n{meeting_summary}"
    )
    
    # Single-shot report generation by PI
    final_report_content = pi.respond([{"role": "user", "content": report_prompt}])
    
    with open(FINAL_REPORT_PATH, 'w') as f:
        f.write(final_report_content)
        
    # Save Transcript
    with open(TRANSCRIPT_PATH, 'w') as f:
        f.write(meeting_summary)
        
    print(f"\n=== Phase 3 Completed. Report saved to {FINAL_REPORT_PATH} ===")

if __name__ == "__main__":
    main()
