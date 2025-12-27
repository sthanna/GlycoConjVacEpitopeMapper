import sys
import os
from pathlib import Path

# Add src to path
sys.path.append(os.path.abspath("src"))

from virtual_lab.agent import Agent

def main():
    print("=== Testing ML Specialist Knowledge Base ===")
    
    # Path verified in previous step
    kb_path = "data/knowledge_base/ml_specialist/vector_index"
    
    if not os.path.exists(kb_path):
        print(f"Error: Knowledge base not found at {kb_path}")
        return

    # Initialize Agent "Charlie"
    agent = Agent(
        name="Charlie",
        role="ML Specialist",
        system_prompt="You are an expert ML Specialist in Geometric Deep Learning and Protein Language Models.",
        kb_path=kb_path
    )
    
    questions = [
        "How do equivariant neural networks improve 3D epitope prediction compared to standard CNNs?",
        "Discuss the advantages of using pre-trained protein language models (like ESM-2) for zero-shot prediction of immunogenicity."
    ]
    
    transcript = []
    
    for q in questions:
        print(f"\n--- User Question: {q} ---")
        transcript.append(f"[User]: {q}")
        
        # 1. Test Retrieval explicitly
        print("Querying Knowledge Base...")
        context = agent.query_kb(q, k=3)
        print(f"Retrieved Context:\n{context[:500]}... [truncated]") 
        
        # 2. Attempt Response
        print("Agent responding...")
        history = [{'role': 'user', 'name': 'User', 'content': q}]
        
        response = agent.respond(history)
        print(f"Agent Response:\n{response}")
        transcript.append(f"[Charlie (ML Specialist)]: {response}\n(Context Used: {len(context)} chars)")
        
    # Save transcript
    with open("ml_specialist_test_transcript.txt", "w", encoding="utf-8") as f:
        f.write("\n\n".join(transcript))
    print("\nTranscript saved to ml_specialist_test_transcript.txt")

if __name__ == "__main__":
    if sys.stdout.encoding != 'utf-8':
        sys.stdout.reconfigure(encoding='utf-8')
    main()
