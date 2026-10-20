#!/usr/bin/env python3
"""
Example Prompts & Automated Showcase for OpenJev Effort & Harness Router.
Demonstrates how the router evaluates prompts across complexity, reasoning effort, and harness affinities.
"""
import sys
import os

# Add parent directory to path so we can import from scripts
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))

from jev_router import HarnessRouter, format_report

SAMPLE_PROMPTS = [
    {
        "category": "1. Trivial Mechanical Task (Typo & Linter)",
        "prompt": "fix typo and spelling in README.md header",
        "notes": "Routes to fast model tier with 0 tokens (clamped to low for always-on adaptive models) to save cost and latency."
    },
    {
        "category": "2. Routine Full-Stack Feature",
        "prompt": "implement a FastAPI authentication endpoint with JWT tokens and bcrypt password hashing",
        "notes": "Routes to balanced flagship tier (Sonnet 5.5, GPT-6.1 Sol, Gemini 3.8 Flash) with medium reasoning."
    },
    {
        "category": "3. Complex State & Concurrency Refactoring",
        "prompt": "refactor WebSocket state machine with redis pub/sub and handle async race conditions in connection pool",
        "notes": "High complexity and medium/high reasoning effort; evaluates state synchronization and concurrency."
    },
    {
        "category": "4. Frontier Distributed System Architecture",
        "prompt": "architect a Byzantine fault-tolerant Raft consensus state machine in Rust with formal invariant verification and partition recovery",
        "notes": "Frontier architectural tier; routes to maximum test-time compute (Opus 5.5, Gemini 4 Argon, GPT-6 Astra) with max tokens."
    },
    {
        "category": "5. Terminal & Shell-Centric Workflow (Claude Code Affinity)",
        "prompt": "run bash commands to grep server logs, pipe output, and inspect git commit tree branches",
        "notes": "Discriminator detects terminal bash workflows and flags Claude Code as primary harness."
    },
    {
        "category": "6. Native LSP & Debugger Tracing (Oh My Pi Affinity)",
        "prompt": "use LSP client diagnostics and DAP debugger with hashline edits to trace Rust memory leak",
        "notes": "Discriminator detects LSP, DAP, and hashline keywords and flags Oh My Pi as primary harness."
    },
    {
        "category": "7. Multi-Agent Workspace & Interactive Artifacts (Antigravity Affinity)",
        "prompt": "create an Antigravity pair-programming workspace with subagents and generative UI artifacts",
        "notes": "Discriminator detects multi-agent and artifact workspace keywords and flags Antigravity as primary harness."
    },
    {
        "category": "8. Git Micro-Commit Disciplined Pairing (Aider Affinity)",
        "prompt": "pair program in terminal with architect and editor roles and commit git micro-commits after each passing test",
        "notes": "Discriminator detects architect/editor and git commit pairing and flags Aider as primary harness."
    }
]

def main():
    if hasattr(sys.stdout, "reconfigure"):
        try:
            sys.stdout.reconfigure(encoding="utf-8")
        except Exception:
            pass

    router = HarnessRouter()
    print("=" * 80)
    print("  🚀 OPENJEV EFFORT & CODING HARNESS ROUTER — EXAMPLE SHOWCASE")
    print("=" * 80)
    print("Evaluating 8 diverse prompt scenarios across complexity, effort, and harnesses:\n")

    for idx, item in enumerate(SAMPLE_PROMPTS, 1):
        print(f"\n>>> Scenario {idx}: {item['category']}")
        print(f"    Prompt: \"{item['prompt']}\"")
        print(f"    Concept: {item['notes']}")
        
        rec = router.route(item["prompt"], profile="frontier")
        d = rec.decision
        
        print("    " + "-" * 76)
        print(f"    🎯 Complexity:    {d.complexity.level.upper()} (score: {d.complexity.raw_score:.2f})")
        print(f"    🧠 Reasoning:     {d.reasoning.level.upper()} ({rec.token_budget})")
        print(f"    ⭐ Top Harness:   {rec.primary_harness.upper()} -> {rec.primary_model}")
        print(f"    💻 Exec Command:  {rec.primary_command}")
        print("    " + "-" * 76)

    print("\n[OK] Example walkthrough complete!")

if __name__ == "__main__":
    main()
