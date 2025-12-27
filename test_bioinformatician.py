import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from virtual_lab.agent import Agent

def main():
    print("=== Testing Bioinformatician Knowledge Base ===")
    
    kb_path = "data/knowledge_base/bioinformatician/vector_index"
    
    if not os.path.exists(kb_path):
        print(f"Error: Knowledge base not found at {kb_path}")
        return

    # Initialize Agent
    agent = Agent(
        name="Diana",
        role="Bioinformatician",
        system_prompt="You are an expert Bioinformatician specializing in structural biology and vaccine design.",
        kb_path=kb_path
    )
    
    questions = [
        "How do you approach mapping conformational B-cell epitopes using 3D structural data?",
        "Explain the integration of evolutionary sequence analysis with structural modeling for vaccine target discovery."
    ]
    
    transcript = []
    
    for q in questions:
        print(f"\n--- User Question: {q} ---")
        transcript.append(f"[User]: {q}")
        
        # 1. Test Retrieval explicitly first
        print("Querying Knowledge Base...")
        context = agent.query_kb(q, k=2)
        print(f"Retrieved Context:\n{context}")
        
        # 2. Attempt Response
        print("Agent responding...")
        # mocking history
        history = [{'role': 'user', 'name': 'User', 'content': q}]
        
        response = agent.respond(history)
        print(f"Agent Response:\n{response}")
        transcript.append(f"[Diana (Bioinformatician)]: {response}\n(Context Used: {len(context)} chars)")
        
    # Save transcript
    with open("bioinformatician_test_transcript.txt", "w") as f:
        f.write("\n\n".join(transcript))
    print("\nTranscript saved to bioinformatician_test_transcript.txt")

if __name__ == "__main__":
    main()
