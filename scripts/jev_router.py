"""
OpenJev Effort & Coding Harness Router
Non-autoregressive System-1 decision engine based on TypeSafe OpenJev specification.
"""
from __future__ import annotations
from dataclasses import dataclass, field, asdict
from typing import Dict, List, Optional, Any
import math

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
