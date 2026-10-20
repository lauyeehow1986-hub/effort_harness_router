"""
Install OpenJev Effort & Harness Router across all coding agent skill directories:
- Antigravity: ~/.gemini/config/skills/effort-harness-router/
- OpenAI Codex: ~/.codex/skills/effort-harness-router/
- Claude Code: ~/.claude/skills/effort-harness-router/
- Oh My Pi: ~/.omp/skills/effort-harness-router/
- Pi: ~/.pi/skills/effort-harness-router/
"""
import os
import shutil
from pathlib import Path

def install():
    home = Path.home()
    destinations = [
        home / ".gemini" / "config" / "skills" / "effort-harness-router",
        home / ".codex" / "skills" / "effort-harness-router",
        home / ".claude" / "skills" / "effort-harness-router",
        home / ".omp" / "skills" / "effort-harness-router",
        home / ".pi" / "skills" / "effort-harness-router",
    ]

    root = Path(__file__).resolve().parent.parent
    source_skill = root / ".agents" / "skills" / "effort-harness-router" / "SKILL.md"
    source_engine = root / "scripts" / "jev_router.py"

    if not source_skill.exists():
        raise FileNotFoundError(f"Missing {source_skill}")
    if not source_engine.exists():
        raise FileNotFoundError(f"Missing {source_engine}")

    print("Deploying OpenJev Effort & Harness Router to coding agent environments:")
    for dest in destinations:
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_skill, dest / "SKILL.md")
        shutil.copy2(source_engine, dest / "jev_router.py")
        print(f"  [+] Installed to {dest}")

    print("\n[OK] Skill successfully registered across all 5 agent harness environments!")

if __name__ == "__main__":
    install()
