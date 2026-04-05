"""Agent conditions for CrisisNav-Bench comparative evaluation.

Four conditions per ResearchClaw H2 experiment design:
  vanilla  — baseline system prompt, no tools
  policy   — structured policy checklist in system prompt, no tools
  tool     — tool access (5 crisis tools), minimal system prompt
  combined — policy checklist + tool access
"""

from agents.conditions import AGENT_CONDITIONS, get_system_prompt, get_tools_schema

__all__ = ["AGENT_CONDITIONS", "get_system_prompt", "get_tools_schema"]
