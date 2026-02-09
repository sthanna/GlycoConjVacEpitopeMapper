import sys
import os
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from virtual_lab.agent import Agent

KB_PATH = "data/knowledge_base/bioinformatician/vector_index"


def _make_agent():
    return Agent(
        name="Diana",
        role="Bioinformatician",
        system_prompt="You are an expert Bioinformatician specializing in structural biology and vaccine design.",
        kb_path=KB_PATH,
    )


def test_knowledge_base_exists():
    assert os.path.exists(KB_PATH), f"Knowledge base not found at {KB_PATH}"


def test_agent_creation():
    agent = _make_agent()
    assert agent.name == "Diana"
    assert agent.role == "Bioinformatician"


def test_kb_retrieval():
    if not os.path.exists(KB_PATH):
        return

    agent = _make_agent()
    query = "How do you approach mapping conformational B-cell epitopes using 3D structural data?"
    context = agent.query_kb(query, k=2)
    assert isinstance(context, str)
