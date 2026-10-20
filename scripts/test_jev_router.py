"""
Test suite for OpenJev Effort & Harness Router.
"""
import unittest
import sys
import os

# Ensure scripts directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jev_router import ChoiceResult, ScoreResult, NoulResult, JevDecision

class TestOpenJevPrimitives(unittest.TestCase):
    def test_choice_result(self):
        choice = ChoiceResult(
            name="primary_harness",
            selected="claude_code",
            probabilities={"claude_code": 0.72, "antigravity": 0.18, "codex": 0.10},
            confidence=0.72
        )
        self.assertEqual(choice.selected, "claude_code")
        self.assertAlmostEqual(choice.confidence, 0.72)
        self.assertEqual(len(choice.probabilities), 3)

    def test_score_result(self):
        score = ScoreResult(
            name="task_complexity",
            raw_score=0.75,
            level="complex",
            level_probabilities={"trivial": 0.05, "routine": 0.20, "complex": 0.65, "frontier_architectural": 0.10}
        )
        self.assertEqual(score.level, "complex")
        self.assertAlmostEqual(score.raw_score, 0.75)

    def test_noul_result(self):
        noul = NoulResult(
            name="high_risk_or_destructive",
            probability=0.88,
            threshold=0.5
        )
        self.assertTrue(noul.is_triggered)
        self.assertAlmostEqual(noul.probability, 0.88)

    def test_jev_decision_serialization(self):
        decision = JevDecision(
            prompt="Refactor database connection pool",
            harness=ChoiceResult("primary_harness", "antigravity", {"antigravity": 1.0}, 1.0),
            complexity=ScoreResult("task_complexity", 0.6, "complex", {"complex": 1.0}),
            reasoning=ScoreResult("reasoning_depth", 0.7, "high", {"high": 1.0}),
            destructive_risk=NoulResult("destructive_risk", 0.15, 0.5),
            large_context=NoulResult("large_context", 0.65, 0.5)
        )
        d = decision.to_dict()
        self.assertEqual(d["harness"]["selected"], "antigravity")
        self.assertEqual(d["complexity"]["level"], "complex")
        self.assertFalse(d["flags"]["destructive_risk"])
        self.assertTrue(d["flags"]["large_context"])

if __name__ == "__main__":
    unittest.main()
