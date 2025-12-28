# --------------------------------------------------------------------------------
# Author: Sandeep Thanna
# Copyright: 2025, Sandeep Thanna
# Maintainer: Sandeep Thanna
# --------------------------------------------------------------------------------
"""Runs a meeting with Gemini agents."""

import time
from pathlib import Path
from typing import Literal, List, Optional
from tqdm import trange, tqdm
from virtual_lab.agent import Agent
from virtual_lab.constants import CONSISTENT_TEMPERATURE, PUBMED_TOOL_DESCRIPTION
from virtual_lab.prompts import (
    individual_meeting_agent_prompt,
    individual_meeting_critic_prompt,
    individual_meeting_start_prompt,
    SCIENTIFIC_CRITIC,
    team_meeting_start_prompt,
    team_meeting_team_lead_initial_prompt,
    team_meeting_team_lead_intermediate_prompt,
    team_meeting_team_lead_final_prompt,
    team_meeting_team_member_prompt,
)
from virtual_lab.utils import (
    count_discussion_tokens,
    get_summary,
    save_meeting,
)

def run_meeting(
    meeting_type: Literal["team", "individual"],
    agenda: str,
    save_dir: Path,
    save_name: str = "discussion",
    team_lead: Agent | None = None,
    team_members: tuple[Agent, ...] | None = None,
    team_member: Agent | None = None,
    agenda_questions: tuple[str, ...] = (),
    agenda_rules: tuple[str, ...] = (),
    summaries: tuple[str, ...] = (),
    contexts: tuple[str, ...] = (),
    num_rounds: int = 0,
    temperature: float = CONSISTENT_TEMPERATURE,
    pubmed_search: bool = False,
    return_summary: bool = False,
) -> str:
    """Runs a meeting with LLM agents (Gemini)."""
    
    # 1. Validation (Matched logic from original)
    if meeting_type == "team":
        if team_lead is None or team_members is None or len(team_members) == 0:
            raise ValueError("Team meeting requires team lead and team members")
    elif meeting_type == "individual":
        if team_member is None:
            raise ValueError("Individual meeting requires individual team member")

    # 2. Setup Team
    if meeting_type == "team":
        team = [team_lead] + list(team_members)
    else:
        team = [team_member] + [SCIENTIFIC_CRITIC]

    # 3. Initialize History
    # We maintain a flat list of dicts for the "discussion"
    discussion: List[dict] = []
    
    start_prompt = ""
    if meeting_type == "team":
        start_prompt = team_meeting_start_prompt(
            team_lead=team_lead,
            team_members=team_members,
            agenda=agenda,
            agenda_questions=agenda_questions,
            agenda_rules=agenda_rules,
            summaries=summaries,
            contexts=contexts,
            num_rounds=num_rounds,
        )
    else:
        # For individual meetings, start prompt often goes to the agent in the loop
        pass

    # Record the system kick-off if team
    if start_prompt:
        discussion.append({"agent": "System", "message": start_prompt})

    # 4. Meeting Loop
    for round_index in trange(num_rounds + 1, desc="Rounds"):
        round_num = round_index + 1
        
        for agent in tqdm(team, desc="Team"):
            # Construct Prompt Logic
            prompt = ""
            if meeting_type == "team":
                if agent == team_lead:
                    if round_index == 0:
                        prompt = team_meeting_team_lead_initial_prompt(team_lead)
                    elif round_index == num_rounds:
                        prompt = team_meeting_team_lead_final_prompt(
                            team_lead, agenda, agenda_questions, agenda_rules
                        )
                    else:
                        prompt = team_meeting_team_lead_intermediate_prompt(
                            team_lead, round_num-1, num_rounds
                        )
                else:
                    prompt = team_meeting_team_member_prompt(agent, round_num, num_rounds)
            
            else:
                # Individual
                if agent == SCIENTIFIC_CRITIC:
                     prompt = individual_meeting_critic_prompt(SCIENTIFIC_CRITIC, team_member)
                else:
                    if round_index == 0:
                        prompt = individual_meeting_start_prompt(
                            team_member, agenda, agenda_questions, agenda_rules, summaries, contexts
                        )
                    else:
                        prompt = individual_meeting_agent_prompt(SCIENTIFIC_CRITIC, team_member)

            # Map discussion to history format expected by Agent.respond
            # agent.respond expects [{"role":..., "content":...}, ...]
            history_for_agent = []
            for turn in discussion:
                # Map 'agent' name to 'role'/'name'
                history_for_agent.append({
                    "role": "user" if turn["agent"] != agent.name else "model",
                    "name": turn["agent"],
                    "content": turn["message"]
                })
            
            # Add the specific prompt for this turn
            history_for_agent.append({"role": "user", "content": prompt})

            # CALL GEMINI AGENT
            response_text = agent.respond(history_for_agent)
            
            # Append to discussion
            discussion.append({"agent": agent.name, "message": response_text})
            
            # Stop early in final round if team lead has spoken
            if meeting_type == "team" and round_index == num_rounds and agent == team_lead:
                break

    # 5. Save & Return
    save_meeting(save_dir, save_name, discussion)
    
    if return_summary:
        return get_summary(discussion)
    return ""
