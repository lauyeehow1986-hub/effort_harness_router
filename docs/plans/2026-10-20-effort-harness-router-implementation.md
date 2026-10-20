# OpenJev Effort & Coding Harness Router Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build a production-ready, open-source OpenJev System-1 routing skill and CLI that non-autoregressively routes prompts to the optimal coding harness, model generation, and reasoning effort.

**Architecture:** A standalone, zero-dependency Python engine implementing the TypeSafe OpenJev System-1 contract (`Choice`, `Score`, `Noul`) with calibrated non-autoregressive decision heads, an effort quantizer, a dual-generation cross-harness model catalog, and multi-agent skill distributions across Antigravity, Codex, Claude Code, Oh My Pi, and Pi.

**Tech Stack:** Python 3.10+, Standard Library (no heavy PyTorch or GPU dependencies required for local sub-50ms inference), Git, Markdown/YAML Antigravity & Codex skill specifications.

---

### Task 1: OpenJev System-1 Primitives & Schema

**Files:**
- Create: `scripts/jev_router.py`
- Test: `scripts/test_jev_router.py`

**Step 1: Write the failing test**
Create `scripts/test_jev_router.py` testing the core Jev primitives (`ChoiceResult`, `ScoreResult`, `NoulResult`, `JevDecision`).

**Step 2: Run test to verify it fails**
Run: `python scripts/test_jev_router.py`
Expected: FAIL with `ModuleNotFoundError` or `ImportError`.

**Step 3: Write minimal implementation**
Implement dataclasses and validation for `Choice`, `Score`, `Noul`, and `JevDecision` in `scripts/jev_router.py`.

**Step 4: Run test to verify it passes**
Run: `python scripts/test_jev_router.py`
Expected: PASS.

**Step 5: Commit**
```bash
git add scripts/jev_router.py scripts/test_jev_router.py
git commit -m "feat(jev): implement OpenJev System-1 primitive types and schemas"
```

---

### Task 2: Calibrated Non-Autoregressive Semantic Discriminator

**Files:**
- Modify: `scripts/jev_router.py`
- Modify: `scripts/test_jev_router.py`

**Step 1: Write the failing test**
Add tests in `scripts/test_jev_router.py` verifying that:
- Trivial prompts ("fix typo in readme") yield low `task_complexity` score (<0.3) and low `reasoning_depth` score (<0.2).
- Routine coding prompts ("add express jwt auth endpoint") yield moderate complexity (0.4-0.6) and medium reasoning (0.4-0.65).
- Deep algorithmic prompts ("build distributed raft consensus with formal verification") yield frontier complexity (>0.8) and high/max reasoning (>0.75).
- Potentially destructive operations trigger elevated `Noul("destructive_risk")`.

**Step 2: Run test to verify it fails**
Run: `python scripts/test_jev_router.py`
Expected: FAIL.

**Step 3: Write minimal implementation**
Implement the OpenJev discriminator in `scripts/jev_router.py` using calibrated semantic indicator vectors, lexical density, structural complexity heuristics, and probability calibration.

**Step 4: Run test to verify it passes**
Run: `python scripts/test_jev_router.py`
Expected: PASS.

**Step 5: Commit**
```bash
git add scripts/jev_router.py scripts/test_jev_router.py
git commit -m "feat(jev): implement calibrated semantic discriminator and decision heads"
```

---

### Task 3: Dual-Generation Multi-Harness Catalog & Effort Quantizer

**Files:**
- Modify: `scripts/jev_router.py`
- Modify: `scripts/test_jev_router.py`

**Step 1: Write the failing test**
Add tests in `scripts/test_jev_router.py` verifying:
- Quantization of continuous reasoning score to `none`, `low`, `medium`, `high`, `max` with token estimates.
- Model mapping for all 10 harnesses across Frontier and Legacy profiles:
  - Claude Code: `haiku-5.5` vs `sonnet-5.5` vs `opus-5.5` (Legacy: `sonnet-3.5`, `opus-4.5`)
  - Antigravity: `gemini-3.8-flash` vs `gemini-3.8-pro` vs `argon-4` / `opus-5.5` (Legacy: `gemini-1.5-pro`)
  - Codex: `o3-mini` vs `gpt-5` vs `o1`/`codex-next` (Legacy: `gpt-4o`, `o1-preview`)
  - Grok: `grok-3-mini` vs `grok-3` vs `grok-4`
  - Oh My Pi: `qwen-2.5-coder-32b` vs `deepseek-v3`/`sonnet-5.5` vs `deepseek-r1`/`opus-5.5`
  - Pi, Cursor, Windsurf, Aider, Cline.
- Command synthesis producing exact executable flags (e.g., `claude --model claude-opus-5.5 --effort high`).

**Step 2: Run test to verify it fails**
Run: `python scripts/test_jev_router.py`
Expected: FAIL.

**Step 3: Write minimal implementation**
Implement the `ModelCatalog`, `HarnessProfile`, `quantize_effort`, and `recommend_harness_matrix` in `scripts/jev_router.py`.

**Step 4: Run test to verify it passes**
Run: `python scripts/test_jev_router.py`
Expected: PASS.

**Step 5: Commit**
```bash
git add scripts/jev_router.py scripts/test_jev_router.py
git commit -m "feat(router): implement multi-harness catalog and dual-generation recommendation engine"
```

---

### Task 4: CLI Interface & Formatted Output Engine

**Files:**
- Modify: `scripts/jev_router.py`
- Modify: `scripts/test_jev_router.py`

**Step 1: Write the failing test**
Add tests testing:
- Terminal invocation via subprocess: `python scripts/jev_router.py "refactor database schema"`
- Flag `--profile legacy` producing legacy model equivalents.
- Flag `--json` outputting machine-readable JSON for agent piping.
- Flag `--harness claude_code` filtering to a single harness.

**Step 2: Run test to verify it fails**
Run: `python scripts/test_jev_router.py`
Expected: FAIL.

**Step 3: Write minimal implementation**
Implement `argparse` CLI, rich terminal table formatting (using ASCII/Unicode tables), and JSON serialization.

**Step 4: Run test to verify it passes**
Run: `python scripts/test_jev_router.py`
Expected: PASS.

**Step 5: Commit**
```bash
git add scripts/jev_router.py scripts/test_jev_router.py
git commit -m "feat(cli): add CLI interface with formatted markdown tables and JSON piping"
```

---

### Task 5: Antigravity & Cross-Agent Skill Definitions

**Files:**
- Create: `.agents/skills/effort-harness-router/SKILL.md`
- Create: `.agents/skills/effort-harness-router/jev_router.py`

**Step 1: Write the skill document**
Write `.agents/skills/effort-harness-router/SKILL.md` following the Antigravity Customization standard:
- YAML frontmatter (`name: effort-harness-router`, `description: ...`)
- Clear routing triggers and step-by-step guidance on interpreting Jev decisions.
- Copy portable `scripts/jev_router.py` into `.agents/skills/effort-harness-router/` for standalone execution.

**Step 2: Verify skill syntax and execution**
Run: `python .agents/skills/effort-harness-router/jev_router.py "create a react dashboard" --json`
Expected: Valid JSON decision output.

**Step 3: Commit**
```bash
git add .agents/skills/effort-harness-router/
git commit -m "feat(skill): add Antigravity skill specification and bundled engine"
```

---

### Task 6: Multi-Agent Global Distribution & Installation

**Files:**
- Create/Copy: `C:\Users\lauye\.gemini\config\skills\effort-harness-router/SKILL.md`
- Create/Copy: `C:\Users\lauye\.codex\skills\effort-harness-router/SKILL.md`
- Create/Copy: `C:\Users\lauye\.claude\skills\effort-harness-router/SKILL.md`
- Create/Copy: `C:\Users\lauye\.omp\skills\effort-harness-router/SKILL.md`
- Create/Copy: `C:\Users\lauye\.pi\skills\effort-harness-router/SKILL.md`

**Step 1: Write installation script / routine**
Deploy the skill and runner to the respective user configuration folders.

**Step 2: Verify files exist and are readable in all directories**
Run PowerShell verification script checking path existence.

**Step 3: Commit**
```bash
git commit -m "chore(distribution): distribute skill to Antigravity, Codex, Claude Code, Oh My Pi, and Pi"
```

---

### Task 7: Comprehensive End-to-End Verification & Documentation

**Files:**
- Create: `README.md`
- Run full test suite: `python scripts/test_jev_router.py`

**Step 1: Verify test suite passes with 100% coverage across edge cases**
Run: `python scripts/test_jev_router.py`
Expected: All tests pass.

**Step 2: Create comprehensive `README.md`**
Document motivation, Jev architecture, CLI usage, supported harnesses, model tiers, and integration instructions.

**Step 3: Commit**
```bash
git add README.md
git commit -m "docs: add comprehensive README and verification guide"
```
