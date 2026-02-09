import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.agent import Agent

KB_PATH = "data/knowledge_base/ml_specialist/vector_index"


def _make_agent():
    return Agent(
        name="Charlie",
        role="ML Specialist",
        system_prompt="You are an expert ML Specialist in Geometric Deep Learning and Protein Language Models.",
        kb_path=KB_PATH,
    )


def test_knowledge_base_exists():
    assert os.path.exists(KB_PATH), f"Knowledge base not found at {KB_PATH}"


def test_agent_creation():
    agent = _make_agent()
    assert agent.name == "Charlie"
    assert agent.role == "ML Specialist"


def test_kb_retrieval():
    if not os.path.exists(KB_PATH):
        return

    agent = _make_agent()
    query = "How do equivariant neural networks improve 3D epitope prediction?"
    context = agent.query_kb(query, k=3)
    assert isinstance(context, str)
