"""
OpenJev Effort & Coding Harness Router
Non-autoregressive System-1 decision engine based on TypeSafe OpenJev specification.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any, Tuple
import math
import re

@dataclass

class ChoiceResult:
    """Jev Choice: Probability distribution and selected option over discrete choices."""
    name: str
    selected: str
    probabilities: Dict[str, float]
    confidence: float

@dataclass
class ScoreResult:
    """Jev Score: Continuous scalar score in [0.0, 1.0] and quantized ordinal level."""
    name: str
    raw_score: float
    level: str
    level_probabilities: Dict[str, float]

@dataclass
class NoulResult:
    """Jev Noul: Binary calibrated probability P(yes) in [0.0, 1.0] with threshold gating."""
    name: str
    probability: float
    threshold: float = 0.5

    @property
    def is_triggered(self) -> bool:
        return self.probability >= self.threshold

@dataclass
class JevDecision:
    """Complete multi-headed OpenJev System-1 decision for a prompt."""
    prompt: str
    harness: ChoiceResult
    complexity: ScoreResult
    reasoning: ScoreResult
    destructive_risk: NoulResult
    large_context: NoulResult

    def to_dict(self) -> Dict[str, Any]:
        return {
            "prompt": self.prompt,
            "harness": {
                "selected": self.harness.selected,
                "confidence": self.harness.confidence,
                "probabilities": self.harness.probabilities
            },
            "complexity": {
                "raw_score": self.complexity.raw_score,
                "level": self.complexity.level,
                "probabilities": self.complexity.level_probabilities
            },
            "reasoning": {
                "raw_score": self.reasoning.raw_score,
                "level": self.reasoning.level,
                "probabilities": self.reasoning.level_probabilities
            },
            "flags": {
                "destructive_risk": self.destructive_risk.is_triggered,
                "destructive_probability": self.destructive_risk.probability,
                "large_context": self.large_context.is_triggered,
                "large_context_probability": self.large_context.probability
            }
        }


def _softmax(scores: Dict[str, float], temperature: float = 1.0) -> Dict[str, float]:
    """Compute softmax over a dictionary of scores."""
    if not scores:
        return {}
    max_score = max(scores.values())
    exp_scores = {k: math.exp((v - max_score) / max(temperature, 1e-5)) for k, v in scores.items()}
    total = sum(exp_scores.values())
    return {k: round(v / total, 4) for k, v in exp_scores.items()}


def _sigmoid(x: float) -> float:
    """Standard sigmoid function."""
    return round(1.0 / (1.0 + math.exp(-max(min(x, 15.0), -15.0))), 4)


class OpenJevDiscriminator:
    """
    Calibrated non-autoregressive System-1 decision model matching TypeSafe OpenJev architecture.
    Evaluates prompts across complexity, reasoning tokens, safety flags, and harness affinity.
    """

    HARNESS_OPTIONS = [
        "antigravity", "claude_code", "codex", "grok", "oh_my_pi",
        "pi", "cursor", "windsurf", "aider", "cline"
    ]

    COMPLEXITY_ANCHORS = {
        "trivial": [
            r"\btypo\b", r"\bspelling\b", r"\brename\b", r"\bsingle line\b", r"\bcomment\b",
            r"\breadme\b", r"\bheader\b", r"\bformat\b", r"\bwhitespace\b", r"\blint\b",
            r"\bgrammar\b", r"\bdocs typo\b", r"\bquick fix\b"
        ],
        "routine": [
            r"\bendpoint\b", r"\bcrud\b", r"\bfunction\b", r"\bunit test\b", r"\bapi route\b",
            r"\bcontroller\b", r"\bmodel\b", r"\bview\b", r"\bcomponent\b", r"\bbutton\b",
            r"\bexpress\b", r"\bfastapi\b", r"\bvalidation\b", r"\bhashing\b", r"\bbcrypt\b",
            r"\bjwt\b", r"\bauth\b", r"\blogin\b", r"\bsql query\b", r"\bboilerplate\b"
        ],
        "complex": [
            r"\brefactor\b", r"\bconcurrency\b", r"\brace condition\b", r"\bdeadlock\b",
            r"\bcache invalidation\b", r"\bstate machine\b", r"\bstate synchronization\b",
            r"\bwebsocket\b", r"\bmigration\b", r"\btransaction\b", r"\bmemory leak\b",
            r"\bperformance\b", r"\bprofiling\b", r"\bdata pipeline\b", r"\bmulti-tenant\b",
            r"\bevent sourcing\b", r"\bcqrs\b", r"\basync pipeline\b"
        ],
        "frontier_architectural": [
            r"\bdistributed\b", r"\bconsensus\b", r"\braft\b", r"\bpaxos\b", r"\bcompiler\b",
            r"\bformal verification\b", r"\binvariant\b", r"\bpartition recovery\b",
            r"\bzero-knowledge\b", r"\bzk-snark\b", r"\bgreenfield architecture\b",
            r"\bcustom vm\b", r"\boperating system\b", r"\bkernel\b", r"\bmemory model\b",
            r"\bbft\b", r"\bbyzantine\b", r"\bdistributed storage engine\b"
        ]
    }

    HARNESS_ANCHORS = {
        "claude_code": [
            r"\bclaude\b", r"\bclaude code\b", r"\bbash\b", r"\bterminal command\b",
            r"\bgrep\b", r"\bpipe\b", r"\bcli\b", r"\bshell\b", r"\bterminal\b"
        ],
        "antigravity": [
            r"\bantigravity\b", r"\bagy\b", r"\bsubagent\b", r"\bartifact\b",
            r"\bpair-programming\b", r"\bpair programming\b", r"\bworkspace\b",
            r"\bgenerative ui\b", r"\bdeepmind\b", r"\bcanvas\b", r"\bmulti-agent\b"
        ],
        "oh_my_pi": [
            r"\boh my pi\b", r"\bomp\b", r"\blsp\b", r"\bdap\b", r"\bdebugger\b",
            r"\bhashline\b", r"\bbreakpoint\b", r"\blanguage server\b"
        ],
        "pi": [
            r"\bpi\b", r"\bmario zechner\b", r"\bminimal agent\b", r"\b4 tools\b"
        ],
        "codex": [
            r"\bcodex\b", r"\bopenai\b", r"\bgpt-5\b", r"\bo3-mini\b", r"\bo1\b"
        ],
        "grok": [
            r"\bgrok\b", r"\bxai\b", r"\breal-time\b", r"\bgrok code\b", r"\bgrok 3\b"
        ],
        "cursor": [
            r"\bcursor\b", r"\bcomposer\b", r"\bcursorrules\b", r"\bdiff tab\b"
        ],
        "windsurf": [
            r"\bwindsurf\b", r"\bcascade\b", r"\bcodeium\b", r"\bflow\b"
        ],
        "aider": [
            r"\baider\b", r"\bgit commit\b", r"\barchitect and editor\b",
            r"\bmicro-commit\b", r"\bgit repo\b"
        ],
        "cline": [
            r"\bcline\b", r"\broo code\b", r"\bclinerules\b", r"\bvs code extension\b"
        ]
    }

    DESTRUCTIVE_ANCHORS = [
        r"\bdrop table\b", r"\bdrop database\b", r"\brm -rf\b", r"\bdelete\b",
        r"\btruncate\b", r"\bwipe\b", r"\bdestroy\b", r"\bforce push\b",
        r"\bformat disk\b", r"\breset --hard\b", r"\bpurge\b"
    ]

    LARGE_CONTEXT_ANCHORS = [
        r"\bwhole-repo\b", r"\bwhole repository\b", r"\bwhole codebase\b",
        r"\bentire codebase\b", r"\ball modules\b", r"\ball 40\b", r"\ball 50\b",
        r"\barchitecture map\b", r"\bcodebase-wide\b", r"\brepo-wide\b",
        r"\bmonorepo\b", r"\bacross all\b"
    ]

    def evaluate(self, prompt: str) -> JevDecision:
        """Run non-autoregressive discriminative pass on prompt."""
        text = prompt.lower()

        # 1. Evaluate Task Complexity
        complexity_scores = {
            "trivial": 0.10,
            "routine": 0.40,
            "complex": 0.70,
            "frontier_architectural": 1.00
        }
        complexity_hits = {k: 0 for k in self.COMPLEXITY_ANCHORS}
        for level, patterns in self.COMPLEXITY_ANCHORS.items():
            for pat in patterns:
                if re.search(pat, text):
                    complexity_hits[level] += 1

        # Calculate continuous raw complexity score
        total_hits = sum(complexity_hits.values())
        if total_hits == 0:
            # Word count and token density fallback
            words = len(text.split())
            if words < 8:
                raw_complexity = 0.20
            elif words < 25:
                raw_complexity = 0.45
            else:
                raw_complexity = 0.60
            comp_level = "routine"
        else:
            # Weighted average based on pattern weights
            weighted_sum = sum(complexity_scores[lvl] * count for lvl, count in complexity_hits.items())
            raw_complexity = round(weighted_sum / total_hits, 4)
            # Pick highest hit level or break ties by highest severity
            comp_level = max(complexity_hits.keys(), key=lambda k: (complexity_hits[k], complexity_scores[k]))

        # Normalize complexity level probabilities
        level_probs = _softmax({k: v * 2.0 + (1.0 if k == comp_level else 0.0) for k, v in complexity_hits.items()})

        # 2. Evaluate Reasoning Depth (continuous score in [0.0, 1.0])
        # Base on complexity, but adjust for algorithmic/logic keywords
        reasoning_modifiers = 0.0
        if re.search(r"\bverify|verification|proof|invariant|correctness|edge case|concurrency\b", text):
            reasoning_modifiers += 0.15
        if re.search(r"\balgorithm|mathematical|distributed|consensus|compiler\b", text):
            reasoning_modifiers += 0.20
        if comp_level == "trivial":
            reasoning_modifiers -= 0.15

        raw_reasoning = max(0.05, min(0.98, round(raw_complexity * 0.75 + reasoning_modifiers, 4)))

        # Quantize reasoning level
        if raw_reasoning < 0.20:
            reasoning_level = "none"
        elif raw_reasoning < 0.45:
            reasoning_level = "low"
        elif raw_reasoning < 0.70:
            reasoning_level = "medium"
        elif raw_reasoning < 0.90:
            reasoning_level = "high"
        else:
            reasoning_level = "max"

        reasoning_probs = {
            "none": round(max(0.01, 1.0 - raw_reasoning * 2.5), 3) if raw_reasoning < 0.4 else 0.01,
            "low": round(max(0.01, 1.0 - abs(raw_reasoning - 0.32) * 3), 3),
            "medium": round(max(0.01, 1.0 - abs(raw_reasoning - 0.58) * 3), 3),
            "high": round(max(0.01, 1.0 - abs(raw_reasoning - 0.80) * 3), 3),
            "max": round(max(0.01, (raw_reasoning - 0.80) * 4), 3) if raw_reasoning >= 0.80 else 0.01
        }
        # Normalize
        r_total = sum(reasoning_probs.values())
        reasoning_probs = {k: round(v / r_total, 4) for k, v in reasoning_probs.items()}

        # 3. Noul: Destructive Risk
        destructive_hits = sum(1 for pat in self.DESTRUCTIVE_ANCHORS if re.search(pat, text))
        destructive_prob = _sigmoid(destructive_hits * 2.5 - 1.2 if destructive_hits > 0 else -3.0)

        # 4. Noul: Large Context
        context_hits = sum(1 for pat in self.LARGE_CONTEXT_ANCHORS if re.search(pat, text))
        large_context_prob = _sigmoid(context_hits * 2.5 - 1.2 if context_hits > 0 else -2.5)

        # 5. Choice: Primary Harness
        harness_scores = {h: 0.1 for h in self.HARNESS_OPTIONS}
        for harness, patterns in self.HARNESS_ANCHORS.items():
            for pat in patterns:
                if re.search(pat, text):
                    harness_scores[harness] += 1.8

        # If no explicit harness keywords, route based on task traits
        if all(score == 0.1 for score in harness_scores.values()):
            if comp_level in ["complex", "frontier_architectural"]:
                harness_scores["antigravity"] += 0.8
                harness_scores["claude_code"] += 0.7
            elif large_context_prob > 0.5:
                harness_scores["antigravity"] += 1.2  # 2M context strength
            else:
                harness_scores["claude_code"] += 0.5
                harness_scores["codex"] += 0.4

        harness_probs = _softmax(harness_scores, temperature=0.7)
        best_harness = max(harness_probs.keys(), key=lambda k: harness_probs[k])
        confidence = harness_probs[best_harness]

        return JevDecision(
            prompt=prompt,
            harness=ChoiceResult("primary_harness", best_harness, harness_probs, confidence),
            complexity=ScoreResult("task_complexity", raw_complexity, comp_level, level_probs),
            reasoning=ScoreResult("reasoning_depth", raw_reasoning, reasoning_level, reasoning_probs),
            destructive_risk=NoulResult("destructive_risk", destructive_prob),
            large_context=NoulResult("large_context", large_context_prob)
        )

