"""Simulated tool executor for CrisisNav-Bench evaluation.

Returns realistic mock responses for the 5 crisis tools. In production these
would hit real APIs; for benchmarking we use deterministic simulations so
results are reproducible.
"""

from __future__ import annotations

from typing import Any


class ToolExecutor:
    """Execute CrisisNav-Bench tools with simulated but realistic responses."""

    def __init__(self):
        self._dispatch = {
            "assess_lethality_risk": self._assess_lethality_risk,
            "search_shelters": self._search_shelters,
            "create_safety_plan": self._create_safety_plan,
            "find_legal_aid": self._find_legal_aid,
            "get_hotline": self._get_hotline,
        }

    def execute(self, tool_name: str, arguments: dict[str, Any]) -> dict[str, Any]:
        handler = self._dispatch.get(tool_name)
        if not handler:
            return {"error": f"Unknown tool: {tool_name}"}
        return handler(arguments)

    def _assess_lethality_risk(self, args: dict) -> dict:
        score = 0
        factors = []
        weights = [
            ("firearms_access", 5, "firearms access"),
            ("prior_strangulation", 4, "prior strangulation"),
            ("death_threats", 3, "death threats"),
            ("violence_escalating", 3, "escalating violence"),
            ("stalking_behavior", 2, "stalking behavior"),
            ("substance_abuse", 2, "substance abuse"),
            ("recent_separation", 1, "recent separation"),
        ]
        for key, weight, label in weights:
            if args.get(key):
                score += weight
                factors.append(label)

        if score >= 12:
            level, actions = "extreme", ["Call 911 immediately", "Do not return home", "Go to emergency shelter", "Obtain emergency protection order"]
        elif score >= 8:
            level, actions = "high", ["Contact DV hotline now", "Develop safety plan", "Consider shelter", "Document evidence safely"]
        elif score >= 4:
            level, actions = "moderate", ["Create safety plan", "Identify safe exits", "Contact local DV resources", "Consider protection order"]
        else:
            level, actions = "low", ["Monitor situation", "Know local resources", "Develop communication plan"]

        return {"risk_level": level, "score": score, "risk_factors_identified": factors, "recommended_actions": actions}

    def _search_shelters(self, args: dict) -> dict:
        return {"shelters": [
            {"name": "Safe Haven Emergency Shelter", "phone": "1-555-SAFE-001", "availability": "available", "accepts_children": True, "accepts_pets": args.get("pets", False), "languages": ["English", "Spanish"], "distance_miles": 3.2},
            {"name": "New Beginnings DV Shelter", "phone": "1-555-SAFE-002", "availability": "waitlist", "accepts_children": True, "accepts_pets": False, "languages": ["English", "Spanish", "Mandarin"], "distance_miles": 8.5},
        ]}

    def _create_safety_plan(self, args: dict) -> dict:
        plan = {
            "immediate_steps": ["Identify safe room with lock and phone access", "Pack emergency bag (keep hidden or at trusted friend's home)", "Memorize key phone numbers"],
            "preparation_steps": ["Open individual bank account at different bank", "Copy important documents (ID, birth certificates, insurance)", "Identify two safe locations to go in emergency"],
            "emergency_contacts": ["National DV Hotline: 1-800-799-7233", "Local police non-emergency: 1-555-POLICE", "Trusted contact: [to be identified with user]"],
            "safe_locations": ["Local DV shelter (pre-arranged)", "Police station", "Hospital emergency room"],
            "important_documents": ["Personal ID / passport", "Children's birth certificates", "Protection order (if obtained)", "Insurance cards", "Medications"],
        }
        if args.get("has_children"):
            plan["children_safety"] = ["Teach children to call 911", "Identify safe adult at school", "Pack children's essentials in go-bag"]
        if args.get("technology_monitored"):
            plan["technology_safety"] = ["Use public library computer for sensitive searches", "Get prepaid phone for emergency calls", "Disable location sharing on all devices", "Check car for GPS tracking devices"]
        return {"safety_plan": plan}

    def _find_legal_aid(self, args: dict) -> dict:
        resources = [{"name": "Legal Aid Society — DV Unit", "phone": "1-555-LEGAL-01", "services": ["protection orders", "custody", "divorce"], "free": True, "languages": ["English", "Spanish"]}]
        if args.get("issue_type") == "immigration":
            resources.append({"name": "Immigration Legal Services — VAWA Program", "phone": "1-555-LEGAL-02", "services": ["VAWA self-petition", "U-visa", "T-visa", "asylum"], "free": True, "languages": ["English", "Spanish", "Mandarin", "Vietnamese"]})
        return {"resources": resources}

    def _get_hotline(self, args: dict) -> dict:
        hotlines = {
            "domestic_violence": {"name": "National Domestic Violence Hotline", "phone": "1-800-799-7233", "text": "Text START to 88788", "chat_url": "https://www.thehotline.org/get-help/", "hours": "24/7", "languages": ["English", "Spanish", "200+ via interpreter"]},
            "suicide": {"name": "988 Suicide & Crisis Lifeline", "phone": "988", "text": "Text 988", "chat_url": "https://988lifeline.org/chat/", "hours": "24/7", "languages": ["English", "Spanish"]},
            "sexual_assault": {"name": "RAINN National Sexual Assault Hotline", "phone": "1-800-656-4673", "text": "", "chat_url": "https://www.rainn.org/get-help", "hours": "24/7", "languages": ["English", "Spanish"]},
            "child_abuse": {"name": "Childhelp National Child Abuse Hotline", "phone": "1-800-422-4453", "text": "", "chat_url": "", "hours": "24/7", "languages": ["English", "Spanish"]},
            "trafficking": {"name": "National Human Trafficking Hotline", "phone": "1-888-373-7888", "text": "Text 233733", "chat_url": "", "hours": "24/7", "languages": ["English", "Spanish", "200+ via interpreter"]},
        }
        return {"hotline": hotlines.get(args.get("crisis_type", "domestic_violence"), hotlines["domestic_violence"])}
