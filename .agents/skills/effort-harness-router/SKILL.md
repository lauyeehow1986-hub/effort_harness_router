---
name: effort-harness-router
description: >-
  Routes coding prompts to the optimal coding harness (Claude Code, Antigravity, Codex,
  Grok, Oh My Pi, Pi, Cursor, Windsurf, Aider, Cline), model tier (Frontier vs Legacy),
  and reasoning effort level based on TypeSafe OpenJev System-1 decision modeling.
---

# OpenJev Effort & Coding Harness Router

## Overview

Modern software engineering with AI follows the fundamental agent stack formula:
$$\text{Coding Agent} = \text{Model} + \text{Harness} + \text{Reasoning Effort}$$

This skill provides an ultra-fast, non-autoregressive decision engine powered by the **OpenJev System-1 Architecture**. It evaluates any programming task or user prompt and deterministically outputs:
1. **Primary Harness Recommendation**: The optimal agent harness (`antigravity`, `claude_code`, `codex`, `grok`, `oh_my_pi`, `pi`, `cursor`, `windsurf`, `aider`, `cline`).
2. **Model Selection**: Exact model tier for the chosen harness (e.g., Opus 5.5 vs Sonnet 5.5 vs Haiku 5.5 in Claude Code; Argon 4 vs Opus 5.5 vs Gemini 3.8 Flash in Antigravity).
3. **Reasoning Effort & Token Budget**: Calibrated thinking budget (`none`, `low`, `medium`, `high`, `max`).
4. **Cross-Harness Compatibility Matrix**: Ready-to-use CLI commands and configurations across all 10 major coding harnesses.
5. **Dual-Generation Support**: Switch between Next-Gen/Frontier models and Legacy/V4 equivalents (e.g., Opus 4.5, Sonnet 3.5, GPT-4o).

---

## When to Use This Skill

Activate this skill whenever:
- You need to decide which model, agent harness, or thinking budget to use for a user request.
- The user asks whether to run Claude Code, Antigravity, Codex, Grok, Oh My Pi, or another tool for their task.
- You need to choose between lightweight/fast models (Haiku 5.5 / Gemini Flash / o3-mini) vs. frontier reasoning models (Opus 5.5 / Argon 4 / o1).
- You want to economize token spending and latency without sacrificing task accuracy.

---

## How to Execute the Router

### 1. Terminal / Shell Invocation
Run the bundled OpenJev router script directly:

```bash
# General evaluation (prints full decision summary, primary choice, and matrix)
python scripts/jev_router.py "your coding prompt or task description"

# Filter to a specific coding harness
python scripts/jev_router.py "implement raft consensus" --harness claude_code

# Switch to Legacy / V4 model generation profile
python scripts/jev_router.py "refactor user auth" --profile legacy

# Machine-readable JSON output (ideal for programmatic subagent pipelines)
python scripts/jev_router.py "fix spelling error in README.md" --json

# Quick CLI command output only
python scripts/jev_router.py "audit security vulnerabilities" --quiet
```

---

## Decision Taxonomy & Thresholds

The OpenJev router uses calibrated non-autoregressive decision heads:

### 1. Task Complexity (`Score`)
- **`trivial` (Score $\le 0.25$)**: Typos, documentation formatting, single-line edits, simple command execution.
- **`routine` (Score $0.26 - 0.65$)**: Standard API endpoints, CRUD operations, boilerplate unit tests, isolated bugs.
- **`complex` (Score $0.66 - 0.85$)**: Multi-file refactoring, state machine synchronization, cache invalidation, async race conditions.
- **`frontier_architectural` (Score $\ge 0.86$)**: Greenfield system architecture, distributed consensus (Raft/Paxos), formal verification, compiler passes, high-ambiguity research tasks.

### 2. Reasoning Effort & Token Budget (`Score`)
- **`none` ($0.00 \le \text{score} < 0.20$)**: $0$ reasoning tokens. Instant response for mechanical tasks.
- **`low` ($0.20 \le \text{score} < 0.45$)**: $1,024 - 2,048$ tokens. Quick sanity checks and syntax verification.
- **`medium` ($0.45 \le \text{score} < 0.70$)**: $4,096 - 8,192$ tokens. Standard feature engineering and test writing.
- **`high` ($0.70 \le \text{score} < 0.90$)**: $16,384 - 32,768$ tokens. Complex architecture, concurrency, and security audits.
- **`max` ($\text{score} \ge 0.90$)**: $64,000+$ tokens. Deep mathematical proofs, distributed invariants, compiler design.

### 3. Binary Safety & Context Flags (`Noul`)
- **`destructive_risk`**: Calibrated probability $P(\text{destructive})$. Flags high-risk actions like table truncation, hard resets, or recursive file deletion.
- **`large_context`**: Calibrated probability $P(\text{large\_context})$. Triggers recommendation for Antigravity (Gemini 3.8 2M+ context) or whole-codebase indexing.

---

## Harness Specialization Guide

| Harness | Primary Strengths | Recommended When... |
| :--- | :--- | :--- |
| **Antigravity** (`agy`) | Multi-agent workspaces, subagent delegation, interactive UI artifacts, Gemini 2M+ context. | Greenfield projects, complex multi-step planning, visual/interactive tasks, large repo exploration. |
| **Claude Code** (`claude`) | Fast terminal-native bash execution, rapid directory inspection, deep git branch awareness. | Terminal-centric work, rapid CLI debugging, quick iterative bash loops. |
| **Codex** (`codex`) | OpenAI GPT-6 reasoning and agentic architecture (Astra/Sol/Luna), direct IDE integration, cloud sandboxes. | Algorithmic logic, formal math problems, competitive programming, deep computer use. |

| **Oh My Pi** (`omp`) | 31+ Rust-backed IDE tools, native LSP client, DAP debugger, Hashline edits, multi-role models. | Language server diagnostics, deep breakpoint debugging, high-accuracy edits without text drift. |
| **Pi** (`pi`) | Minimalist zero-bloat harness with 4 core tools (`read`, `write`, `edit`, `bash`). | Lightweight terminal scripting, local open-weight models (Qwen, DeepSeek). |
| **Grok Code** (`grok`) | Real-time web/social synthesis, fast xAI reasoning models. | Tasks requiring up-to-the-minute web information or fast reasoning. |
| **Aider** (`aider`) | Git micro-commits, dual Architect + Editor pairing. | Incremental git commit discipline, strict step-by-step pair programming. |
| **Cursor / Windsurf** | AI IDE editor workflows, multi-file diffing tabs, Cascade agent flows. | Day-to-day interactive GUI editing within the IDE. |
| **Cline** | VS Code MCP ecosystem, human-in-the-loop tool approvals. | Extensible MCP tool chains within standard VS Code. |

---

## Dual-Generation Model Catalog

### Frontier / Next-Gen Profile (`--profile frontier`)
- **Claude Code**: `claude-haiku-5.5` (Fast) $\to$ `claude-sonnet-5.5` (Balanced) $\to$ `claude-opus-5.5` (Frontier)
- **Antigravity**: `gemini-3.8-flash` (Fast) $\to$ `gemini-3.8-pro` (Balanced) $\to$ `argon-4` / `opus-5.5` (Frontier)
- **Codex**: `gpt-6-luna` (Fast) $\to$ `gpt-6.1-sol` (Balanced) $\to$ `gpt-6-astra` (Frontier)
- **Grok**: `grok-3-mini` (Fast) $\to$ `grok-3` (Balanced) $\to$ `grok-4` (Frontier)
- **Oh My Pi**: `qwen-2.5-coder-32b` (Fast) $\to$ `deepseek-v3` (Balanced) $\to$ `deepseek-r1` (Frontier)

### Legacy / V4 Profile (`--profile legacy`)
- **Claude Code**: `claude-3-5-haiku` $\to$ `claude-3-5-sonnet` $\to$ `claude-opus-4.5`
- **Antigravity**: `gemini-1.5-flash` $\to$ `gemini-1.5-pro` $\to$ `gemini-2.0-flash`
- **Codex**: `o3-mini` $\to$ `gpt-4o` $\to$ `o1` (with `gpt-4.5-preview` / `gpt-4o-mini`)
- **Grok**: `grok-2-mini` $\to$ `grok-2`
- **Oh My Pi**: `deepseek-coder-v2` $\to$ `claude-3-5-sonnet`

