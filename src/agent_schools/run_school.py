# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
import yaml
import sys
import os
from pathlib import Path
from typing import List

# Add src to path
sys.path.append(os.path.join(os.getcwd(), 'src'))

from agent_schools.retrieval import PaperRetriever

def load_curriculum(filename: str) -> dict:
    path = Path("src/agent_schools") / filename
    try:
        with open(path, "r") as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Curriculum not found: {filename}")
        return {}

def extract_topics(curriculum: dict) -> List[str]:
    topics = []
    # Levels of mastery
    for level in ["foundational", "intermediate", "advanced"]:
        if level in curriculum:
             topics.extend(curriculum[level].get("topics", []))
    return list(set(topics)) # De-duplicate

def main():
    print("=== Agent School: Morning Bell Ringing ===")
    
    # 1. Setup Retriever
    kb_path = Path("data/knowledge_base")
    retriever = PaperRetriever(out_dir=str(kb_path))
    
    # 2. Define Curricula Map
    roles = {
        "glyco_immunologist": "glyco_immunologist_curriculum.yaml",
        "computational_chemist": "computational_chemist_curriculum.yaml",
        "ml_specialist": "ml_specialist_curriculum.yaml",
        "bioinformatician": "bioinformatician_curriculum.yaml"
    }

    # Execution Loop
    for role, filename in roles.items():
        print(f"\n--- Class in Session: {role.replace('_', ' ').title()} ---")
        
        # Load Topics
        curr = load_curriculum(filename)
        if not curr:
            continue
            
        topics = extract_topics(curr)
        print(f"Curriculum Topics: {len(topics)} found.")
        
        # Focusing on Strategy-defined specific queries if present (added to YAML)
        # We'll prioritize the ones detailed in the strategy doc if they appear in our list
        priority_keywords = ["epitope", "AlphaFold", "ESM", "GLYCAM"]
        selected_topics = [t for t in topics if any(k in t for k in priority_keywords)]
        if not selected_topics:
            selected_topics = topics[:2] # Fallback
            
        # Limit to 3 to respect quotas
        selected_topics = selected_topics[:3]
        print(f"Focusing on: {selected_topics}")
        
        # Setup role-specific output folder
        role_dir = kb_path / role
        role_dir.mkdir(parents=True, exist_ok=True)
        retriever.out_dir = role_dir 
        
        # Run Retrieval
        retriever.run_full_pipeline(selected_topics)
        
        # Internal Representation / Summarization (Strategy Sec 5.3)
        from virtual_lab.agent import Agent
        student = Agent(name=role, role=role, system_prompt=f"You are a {role}. Study these abstracts and summarize key insights relevant to epitope mapping.")
        
        # Read the just-downloaded abstracts
        combined_text = ""
        for topic in selected_topics:
            fpath = role_dir / f"{topic.replace(' ', '_')}_abstracts.txt"
            if fpath.exists():
                with open(fpath, "r", encoding="utf-8") as f:
                    combined_text += f"--- Topic: {topic} ---\n{f.read()[:2000]}\n\n" # Truncate to avoid context limit
        
        summary = ""
        if combined_text:
            print("Generating Knowledge Update (Mini-Review)...")
            summary = student.respond([{"role": "user", "content": f"Based on the following abstracts, write a mini-review summarizing the key methods and findings:\n\n{combined_text}"}])
            
            summary_file = role_dir / "knowledge_update_001.md"
            with open(summary_file, "w", encoding="utf-8") as f:
                f.write(summary)
            print(f"Saved summary to {summary_file}")

        # --- Phase 3: Knowledge Integration (RAG) ---
        print(f"Building Vector Knowledge Base for {role}...")
        from agent_schools.vector_store import build_agent_knowledge_base
        index_path = kb_path / "indexes" / role
        index_path.mkdir(parents=True, exist_ok=True)
        build_agent_knowledge_base(str(role_dir), str(index_path))

        # --- Phase 4: Testing & Certification ---
        print(f"Executing Certification for {role}...")
        certification_prompt = (
            "You are the Scientific Critic and Teacher. Assess the student agent based on their summary. "
            "Score them from 0-100 based on biological accuracy, tool awareness, and reasoning. "
            "If score >= 80, mark as CERTIFIED."
        )
        critic = Agent(name="Scientific Critic", role="Critic", system_prompt=certification_prompt)
        
        # We use the previous summary as the exam submission
        assessment = critic.respond([{"role": "user", "content": f"Student ({role}) Submission:\n\n{summary}"}])
        
        cert_file = role_dir / "certification_report.md"
        with open(cert_file, "w", encoding="utf-8") as f:
            f.write(assessment)
        print(f"Certification report saved to {cert_file}")
            
    print("\n=== All Agents Completed Agent School Graduation! ===")

if __name__ == "__main__":
    main()
