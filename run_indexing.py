import sys
import os
from pathlib import Path

# Add src to sys.path
sys.path.append(os.path.abspath("src"))

from agent_schools.vector_store import build_agent_knowledge_base

AGENTS = ["glyco_immunologist", "computational_chemist", "ml_specialist", "bioinformatician"]
BASE_DATA_DIR = "data/knowledge_base"

def main():
    for agent in AGENTS:
        print(f"\n--- Indexing {agent} ---")
        agent_dir = os.path.join(BASE_DATA_DIR, agent)
        index_path = os.path.join(agent_dir, "vector_index")
        
        # Ensure directories exist
        os.makedirs(agent_dir, exist_ok=True)
        
        # Build index
        # This will process *.txt and *.pdf in the agent directory
        build_agent_knowledge_base(agent_dir, index_path)

if __name__ == "__main__":
    main()
