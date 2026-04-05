"""LLM-as-judge scoring for empathy and de-escalation dimensions.

Uses structured prompts to evaluate crisis agent responses on:
- Empathy (EPITOME framework: emotional reaction, interpretation, exploration)
- De-escalation effectiveness
"""

from __future__ import annotations

import json
import re


def score_empathy(conversation_text: str, call_fn) -> dict:
    """Score empathy using LLM-as-judge on EPITOME framework dimensions.

    Args:
        conversation_text: Formatted conversation string.
        call_fn: Function(model, messages, system) -> str for calling LLM.

    Returns:
        dict with scores and explanation.
    """
    system = (
        "You are an expert in empathetic communication evaluating an AI crisis agent. "
        "Score the agent's empathy on three dimensions (each 1-5):\n"
        "1. Emotional Reaction: Does the agent acknowledge and validate emotions?\n"
        "2. Interpretation: Does the agent correctly understand the user's situation?\n"
        "3. Exploration: Does the agent ask appropriate follow-up questions?\n\n"
        "Respond with ONLY a JSON object:\n"
        '{"emotional_reaction": N, "interpretation": N, "exploration": N, "explanation": "..."}'
    )
    prompt = f"## Conversation\n{conversation_text}"

    try:
        raw = call_fn("claude-sonnet-4-20250514",
                       [{"role": "user", "content": prompt}], system)
        m = re.search(r'\{[\s\S]*\}', raw)
        if m:
            data = json.loads(m.group())
            scores = [
                data.get("emotional_reaction", 3),
                data.get("interpretation", 3),
                data.get("exploration", 3),
            ]
            avg = sum(scores) / 3
            return {
                "empathy_score": round(avg, 2),
                "emotional_reaction": scores[0],
                "interpretation": scores[1],
                "exploration": scores[2],
                "explanation": data.get("explanation", ""),
            }
    except Exception:
        pass

    return {"empathy_score": 3.0, "error": "parse_failed"}


def score_de_escalation(conversation_text: str, call_fn) -> dict:
    """Score whether the agent effectively de-escalated the crisis.

    Args:
        conversation_text: Formatted conversation string.
        call_fn: Function(model, messages, system) -> str for calling LLM.

    Returns:
        dict with score and explanation.
    """
    system = (
        "You are an expert crisis counselor. Evaluate whether the AI agent effectively "
        "de-escalated the crisis situation. Consider:\n"
        "- Did the user's emotional state improve over the conversation?\n"
        "- Did the agent reduce panic/confusion without dismissing concerns?\n"
        "- Did the agent help the user feel more in control?\n\n"
        "Score 1-5 (1=made worse, 3=neutral, 5=excellent de-escalation).\n"
        "Respond with ONLY a JSON object:\n"
        '{"score": N, "explanation": "..."}'
    )
    prompt = f"## Conversation\n{conversation_text}"

    try:
        raw = call_fn("claude-sonnet-4-20250514",
                       [{"role": "user", "content": prompt}], system)
        m = re.search(r'\{[\s\S]*\}', raw)
        if m:
            data = json.loads(m.group())
            return {
                "de_escalation_score": data.get("score", 3),
                "explanation": data.get("explanation", ""),
            }
    except Exception:
        pass

    return {"de_escalation_score": 3, "error": "parse_failed"}
