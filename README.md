# OpenJev Effort & Coding Harness Router

An ultra-fast, non-autoregressive System-1 routing skill and CLI built on the **TypeSafe OpenJev Architecture**.

Dynamically evaluates any coding prompt in milliseconds to determine:
1. **Optimal Coding Harness**: Claude Code, Antigravity, Codex, Grok, Oh My Pi, Pi, Cursor, Windsurf, Aider, Cline.
2. **Model Selection**: Exact model tiers across both **Frontier/Next-Gen** (Opus 5.5, Sonnet 5.5, Argon 4, Gemini 3.8, GPT-5, Grok 4, DeepSeek R1) and **Legacy/V4** (Opus 4.5, Sonnet 3.5, GPT-4o, Gemini 1.5/2.0) profiles.
3. **Reasoning Effort & Token Budget**: Quantized thinking levels (`none`, `low`, `medium`, `high`, `max`) with exact token budgets.
4. **Direct CLI Invocations**: Copy-pasteable shell commands configured with the proper flags.

---

## ⚡ Why an OpenJev Router?

Modern software engineering agents are defined by the formula:
$$\text{Agent} = \text{Model} + \text{Harness} + \text{Reasoning Effort}$$

* Sending a simple markdown typo fix to Claude Opus 5.5 or OpenAI o1 with maximum thinking budget burns unnecessary tokens, dollars, and time.
* Conversely, asking a fast lightweight model (Haiku or Flash) with zero thinking budget to solve a distributed Raft consensus state machine leads to broken concurrency bugs and hallucinated code.
* Different harnesses have dedicated superpowers: **Antigravity** excels at multi-agent workspaces, visual UI artifacts, and 2M+ context; **Claude Code** excels at fast terminal bash pipes; **Oh My Pi (`omp`)** excels at native LSP diagnostics, DAP debugging, and hashline edits; **Aider** excels at git micro-commit discipline.

OpenJev evaluates prompts **non-autoregressively** (sub-50ms) using discriminative `Choice`, `Score`, and `Noul` decision heads without token streaming delays.

---

## 🚀 Quickstart

### 1. Command-Line Usage

```bash
# General evaluation: outputs decision summary, primary recommendation, and cross-harness matrix
python scripts/jev_router.py "design distributed Raft consensus in Rust with formal invariant verification"

# Filter to a specific coding harness
python scripts/jev_router.py "implement jwt auth in express" --harness claude_code

# Switch to Legacy / V4 model generation profile
python scripts/jev_router.py "refactor database schema" --profile legacy

# Programmatic JSON output (for agent piping / automation)
python scripts/jev_router.py "fix typo in readme.md header" --json

# Direct executable command string only
python scripts/jev_router.py "audit smart contract security" --quiet
```

### 2. Python API

```python
from scripts.jev_router import HarnessRouter

router = HarnessRouter()
rec = router.route("architect a microservices event pipeline", profile="frontier")

print(f"Primary Harness: {rec.primary_harness}")
print(f"Primary Model:   {rec.primary_model}")
print(f"Effort:          {rec.effort} ({rec.token_budget})")
print(f"Run Command:     {rec.primary_command}")
```

---

## 📊 Harness & Model Matrix

| Harness | Command | Fast / Low Effort | Balanced / Med Effort | Frontier / High Effort | Legacy / V4 Equivalent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | `claude` | `claude-haiku-5.5` | `claude-sonnet-5.5` | `claude-opus-5.5` | `claude-3-5-sonnet`, `claude-opus-4.5` |
| **Antigravity** | `agy` | `gemini-3.8-flash` | `gemini-3.8-pro` | `argon-4` / `opus-5.5` | `gemini-1.5-pro`, `gemini-2.0-flash` |
| **OpenAI Codex** | `codex` | `o3-mini` | `gpt-5` | `o1` / `codex-next` | `gpt-4o`, `o1-preview` |
| **Grok Code** | `grok` | `grok-3-mini` | `grok-3` | `grok-4` | `grok-2` |
| **Oh My Pi (OMP)** | `omp` | `qwen-2.5-coder-32b` | `deepseek-v3` | `deepseek-r1` | `claude-3-5-sonnet` |
| **Pi** | `pi` | `qwen-2.5-coder-7b` | `deepseek-v3` | `deepseek-r1` | `claude-3-5-haiku` |
| **Cursor** | `cursor` | `claude-3-5-haiku` | `claude-sonnet-5.5` | `claude-opus-5.5` | `cursor-small`, `gpt-4o` |
| **Windsurf** | `windsurf` | `cascade-fast` | `cascade-base` | `cascade-deep` | `swe-bench-lite` |
| **Aider** | `aider` | `haiku-5.5` | `sonnet-5.5` | `opus-5.5` | `gpt-4o` |
| **Cline** | `cline` | `gemini-3.8-flash` | `claude-sonnet-5.5` | `claude-opus-5.5` | `claude-3-5-sonnet` |

---

## 🎯 Effort Levels & Token Budgets

- **`none` ($0$ tokens)**: Mechanical tasks, typos, linters, single line edits.
- **`low` ($1,024 - 2,048$ tokens)**: Syntax checking, quick test fixes, basic function implementation.
- **`medium` ($4,096 - 8,192$ tokens)**: Standard feature implementation, refactors, multi-step functions.
- **`high` ($16,384 - 32,768$ tokens)**: Complex state machines, multi-file architectural changes, concurrency bugs.
- **`max` ($64,000+$ tokens)**: Distributed consensus algorithms, formal verification, cryptographic proofs, compiler optimizations.

---

## 📦 Multi-Agent Installation

The router is distributed as a universal skill compatible with all major coding agents:

```bash
# Run one-click installer across all environments
python scripts/install_skills.py
```

This installs the skill specification and standalone engine into:
* **Antigravity**: `~/.gemini/config/skills/effort-harness-router/` (and repo `.agents/skills/effort-harness-router/`)
* **OpenAI Codex**: `~/.codex/skills/effort-harness-router/`
* **Claude Code**: `~/.claude/skills/effort-harness-router/`
* **Oh My Pi**: `~/.omp/skills/effort-harness-router/`
* **Pi**: `~/.pi/skills/effort-harness-router/`

---

## 🧪 Testing

Run the full unit test suite:

```bash
python scripts/test_jev_router.py
```
