from typing import List, Dict, Tuple
from .agent import Agent

def run_team_meeting(
    agents: List[Agent], 
    critic: Agent, 
    pi: Agent, 
    agenda: str, 
    rounds: int = 3
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Orchestrate a multi-agent team meeting.
    """
    history: List[Dict[str, str]] = [{"role": "system", "content": f"Meeting Agenda: {agenda}"}]
    
    print(f"--- Starting Team Meeting: {agenda[:50]}... ---")

    import time
    
    # PI starts
    pi_msg = pi.respond(history)
    history.append({"role": "model", "name": pi.name, "content": pi_msg})
    print(f"{pi.name} (PI): {pi_msg}")
    time.sleep(10)

    for r in range(rounds):
        print(f"--- Round {r+1} ---")
        # Specialists respond
        for agent in agents:
            # For each specialist, we give them the history so far
            msg = agent.respond(history)
            history.append({"role": "model", "name": agent.name, "content": msg})
            print(f"{agent.name} ({agent.role}): {msg}")
            time.sleep(10)
        
        # Critic intervenes
        critic_msg = critic.respond(history)
        history.append({"role": "model", "name": critic.name, "content": critic_msg})
        print(f"{critic.name} (Critic): {critic_msg}")
        time.sleep(10)

    # Final Synthesis
    wrap_up_prompt = [{"role": "user", "name": "System", "content": "Synthesize the discussion, make final decisions, and list next steps."}]
    final_summary = pi.respond(history + wrap_up_prompt)
    print(f"--- Meeting Adjourned ---\nFinal Summary: {final_summary}")
    
    return final_summary, history

def run_individual_meeting(
    agent: Agent, 
    critic: Agent, 
    task_description: str, 
    rounds: int = 3
) -> Tuple[str, List[Dict[str, str]]]:
    """
    Orchestrate a focused 1-on-1 session.
    """
    history: List[Dict[str, str]] = [{"role": "system", "content": f"Task: {task_description}"}]
    
    print(f"--- Starting Individual Task: {task_description[:50]}... ---")

    for r in range(rounds):
        # Agent works
        work_output = agent.respond(history)
        history.append({"role": "model", "name": agent.name, "content": work_output})
        print(f"{agent.name}: {work_output}")
        
        if r < rounds - 1:
            # Critic gives feedback
            feedback = critic.respond(history)
            history.append({"role": "model", "name": critic.name, "content": feedback})
            print(f"{critic.name}: {feedback}")

    # Final Polish
    final_prompt = [{"role": "user", "content": "Provide your final, refined output for this task."}]
    final_output = agent.respond(history + final_prompt)
    
    return final_output, history
