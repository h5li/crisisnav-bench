#!/usr/bin/env python3
"""
CrisisNav-Bench Evaluation Runner

Runs test cases against a target AI system and produces scored results.

Usage:
    python scripts/run_eval.py --model claude-3.5-sonnet --test-suite all
    python scripts/run_eval.py --model gpt-4o --test-suite safety
    python scripts/run_eval.py --model claude-3.5-sonnet --system-prompt prompts/system.md
"""

import argparse
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from eval.dimensions import ALL_DIMENSIONS, EvalResult
from eval.safety_checker import check_safety


def load_test_cases(suite: str = "all") -> list[dict]:
    """Load test cases from JSON files."""
    test_dir = Path(__file__).parent.parent / "test_cases"
    cases = []
    
    if suite == "all":
        pattern = "**/*.json"
    else:
        pattern = f"{suite}/**/*.json"
    
    for path in sorted(test_dir.glob(pattern)):
        with open(path) as f:
            data = json.load(f)
            if isinstance(data, list):
                cases.extend(data)
            else:
                cases.append(data)
    
    return cases


def run_test_case(case: dict, model: str, system_prompt: str | None = None) -> EvalResult:
    """
    Run a single test case against the target model.
    
    This is a placeholder — implement with your preferred API client.
    """
    result = EvalResult(test_case_id=case["id"])
    
    # TODO: Implement actual API call to target model
    # response = call_model(model, system_prompt, case["conversation"])
    
    # For now, return placeholder
    print(f"  Running: {case['id']} ({case.get('difficulty', '?')})")
    
    return result


def main():
    parser = argparse.ArgumentParser(description="CrisisNav-Bench Evaluation Runner")
    parser.add_argument("--model", required=True, help="Model to evaluate")
    parser.add_argument("--test-suite", default="all", help="Test suite to run (all, safety, insurance, etc.)")
    parser.add_argument("--system-prompt", help="Path to system prompt file")
    parser.add_argument("--output", help="Output path for results JSON")
    args = parser.parse_args()
    
    # Load test cases
    cases = load_test_cases(args.test_suite)
    print(f"Loaded {len(cases)} test cases for suite: {args.test_suite}")
    
    # Load system prompt
    system_prompt = None
    if args.system_prompt:
        with open(args.system_prompt) as f:
            system_prompt = f.read()
    
    # Run evaluation
    results = []
    for case in cases:
        result = run_test_case(case, args.model, system_prompt)
        results.append(result)
    
    # Output results
    output = {
        "metadata": {
            "model": args.model,
            "test_suite": args.test_suite,
            "total_cases": len(cases),
            "timestamp": datetime.utcnow().isoformat(),
        },
        "results": [
            {
                "test_case_id": r.test_case_id,
                "scores": r.scores,
                "passed": r.passed,
                "overall_pass": r.overall_pass,
                "weighted_score": r.weighted_score,
            }
            for r in results
        ],
    }
    
    output_path = args.output or f"results/{args.model.replace('/', '_')}_{args.test_suite}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    os.makedirs(os.path.dirname(output_path) or "results", exist_ok=True)
    
    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)
    
    print(f"\nResults written to: {output_path}")


if __name__ == "__main__":
    main()
