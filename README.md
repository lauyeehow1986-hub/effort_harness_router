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

## 💡 Example Prompts & How to Use the Skill

You can use the router in two ways:
1. **As a conversational routing skill inside your AI pair-programmer** (Antigravity, Claude Code, Codex, Oh My Pi, Pi).
2. **As a direct terminal CLI / script** before launching an agent session.

### 💬 Mode 1: Asking Your Agent (Conversational In-Chat Prompts)

When the skill is loaded in Antigravity (`agy`), Claude Code (`claude`), Codex (`codex`), or Oh My Pi (`omp`), simply ask natural routing questions. Here are real-world prompt examples:

#### Scenario A: Architecting a Distributed System
> **User Prompt:**
> *"I need to implement a distributed Raft consensus state machine in Rust with network partition recovery and formal invariant verification. Which harness and model should I use, and what thinking effort?"*
> 
> **Agent Decision & Response:**
> ```text
> [OpenJev Decision Summary]
> Complexity:    FRONTIER_ARCHITECTURAL (score: 0.95)
> Reasoning:     MAX (64,000+ tokens)
> Top Harness:   ANTIGRAVITY -> gemini-4-argon (agy --model gemini-4-argon --effort max)
> Cross-Harness Options:
>   - Claude Code: claude --model claude-opus-5.5 --effort max
>   - Codex:       codex --model gpt-6-astra --reasoning-effort max
>   - Oh My Pi:    omp --role default=deepseek-r1 --role plan=deepseek-r1
> ```

#### Scenario B: Quick Syntax or Documentation Fix
> **User Prompt:**
> *"Route this task: 'Fix 3 typos in CONTRIBUTING.md and format markdown tables'. I want to minimize cost and latency."*
> 
> **Agent Decision & Response:**
> ```text
> [OpenJev Decision Summary]
> Complexity:    TRIVIAL (score: 0.10)
> Reasoning:     NONE (0 tokens -> clamped to 'low' for always-on adaptive models)
> Top Harness:   CLAUDE_CODE -> claude-haiku-5.5 (claude --model claude-haiku-5.5 --effort low)
> Cross-Harness Options:
>   - Antigravity: agy --model gemini-3.8-flash --effort low
>   - Codex:       codex --model gpt-6-luna --reasoning-effort low
> ```

#### Scenario C: Debugging with Breakpoints and LSP Diagnostics
> **User Prompt:**
> *"I'm debugging a multi-threaded memory leak in a C++ server using GDB/DAP breakpoints and clangd LSP diagnostics. What's the optimal setup?"*
> 
> **Agent Decision & Response:**
> ```text
> [OpenJev Decision Summary]
> Complexity:    COMPLEX (score: 0.70)
> Reasoning:     MEDIUM (4,096 - 8,192 tokens)
> Top Harness:   OH_MY_PI -> deepseek-v4.1-flash (omp --role default=deepseek-v4.1-flash --role plan=deepseek-v4.1-flash)
> Superpower:    Leverages Oh My Pi's native DAP debugger, LSP client, and Hashline edits.
> ```

#### Scenario D: Legacy / Budget API Routing
> **User Prompt:**
> *"I only have access to legacy 2024/2025 API models (like Sonnet 3.5, GPT-4o). Route this task under the legacy profile: 'Implement a Stripe billing webhook endpoint with idempotent database writes'."*
> 
> **Agent Decision & Response:**
> ```text
> [OpenJev Decision Summary] (Legacy Profile)
> Complexity:    ROUTINE (score: 0.45)
> Reasoning:     LOW (1,024 - 2,048 tokens)
> Top Harness:   CLAUDE_CODE -> claude-3-5-haiku (or claude-3-5-sonnet)
> Cross-Harness Options:
>   - Antigravity: agy --model gemini-1.5-flash
>   - Codex:       codex --model gpt-4o-mini
> ```

---

### 💻 Mode 2: Terminal CLI Prompts & Piped Workflows

#### 1. Evaluate Directly from the Command Line
```bash
# Complex state machine
python scripts/jev_router.py "refactor WebSocket connection pool with redis pubsub and async lock contention"

# Single harness filter (outputs recommendation specific to Claude Code)
python scripts/jev_router.py "build user authentication microservice" --harness claude_code

# Run the automated multi-scenario demonstration showcase
python examples/demo_prompts.py
```

#### 2. Pipe Git Diffs or Issue Descriptions Directly into OpenJev
```bash
# Evaluate git uncommitted changes to decide model effort for reviewing the PR
git diff | python scripts/jev_router.py --harness claude_code

# Pipe GitHub issue description via gh CLI to decide model tier
gh issue view 42 --json body -q .body | python scripts/jev_router.py --json
```

#### 3. Programmatic Subagent Dispatching in Automation Scripts
```python
import subprocess
import json

def get_routing(prompt: str) -> dict:
    result = subprocess.run(
        ["python", "scripts/jev_router.py", prompt, "--json"],
        capture_output=True, text=True, check=True
    )
    return json.loads(result.stdout)

decision = get_routing("optimize PostgreSQL spatial query indexing")
print(f"Selected: {decision['primary_recommendation']['harness']} with {decision['primary_recommendation']['model']}")
print(f"Effort:   {decision['effort']} ({decision['token_budget']})")
```


---

## 📊 Harness & Model Matrix

| Harness | Command | Fast / Low Effort | Balanced / Med Effort | Frontier / High Effort | Legacy / V4 Equivalent |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Claude Code** | `claude` | `claude-haiku-5.5` | `claude-sonnet-5.5` | `claude-opus-5.5` | `claude-3-5-sonnet`, `claude-opus-4.5` |
| **Antigravity** | `agy` | `gemini-3.8-flash` | `gemini-3.8-flash` (high) | `gemini-4-argon` / `opus-5.5` | `gemini-1.5-pro`, `gemini-2.0-flash` |
| **OpenAI Codex** | `codex` | `gpt-6-luna` | `gpt-6.1-sol` | `gpt-6-astra` | `o3-mini`, `gpt-4o`, `o1` |
| **Grok Code** | `grok` | `grok-4-fast` | `grok-4` | `grok-4.7` | `grok-2`, `grok-3` |
| **Oh My Pi (OMP)** | `omp` | `qwen3-coder-next` | `deepseek-v4.1-flash` | `deepseek-r1` | `qwen-2.5-coder-32b`, `deepseek-v3` |
| **Pi** | `pi` | `qwen3-coder-7b` | `deepseek-v4.1-flash` | `deepseek-r1` | `qwen-2.5-coder-7b`, `claude-3-5-haiku` |

| **Cursor** | `cursor` | `claude-haiku-5.5` | `claude-sonnet-5.5` | `claude-opus-5.5` | `cursor-small`, `gpt-4o` |
| **Windsurf** | `windsurf` | `cascade-fast` | `cascade-base` | `cascade-deep` | `swe-bench-lite` |
| **Aider** | `aider` | `haiku-5.5` | `sonnet-5.5` | `opus-5.5` | `gpt-4o` |
| **Cline** | `cline` | `gemini-3.8-flash` | `claude-sonnet-5.5` | `claude-opus-5.5` | `claude-3-5-sonnet` |

---

## 🎯 Effort Levels & Token Budgets

- **`none` ($0$ tokens)**: Mechanical tasks, typos, linters, single line edits. *(Note: Models with always-on adaptive thinking like Claude 5.5 and Gemini 3.8/Argon automatically clamp CLI execution to `--effort low` to prevent API rejection)*.
- **`low` ($1,024 - 2,048$ tokens)**: Syntax checking, quick test fixes, basic function implementation.
- **`medium` ($4,096 - 8,192$ tokens)**: Standard feature implementation, refactors, multi-step functions.
- **`high` ($16,384 - 32,768$ tokens)**: Complex state machines, multi-file architectural changes, concurrency bugs.
- **`xhigh` ($48,000 - 64,000$ tokens)**: Extended chain-of-thought for GPT-5.5 and Claude 5.5 frontier tasks.
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
