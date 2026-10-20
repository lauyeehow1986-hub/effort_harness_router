"""
Test suite for OpenJev Effort & Harness Router.
"""
import unittest
import sys
import os

# Ensure scripts directory is in path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from jev_router import ChoiceResult, ScoreResult, NoulResult, JevDecision, OpenJevDiscriminator

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

class TestOpenJevDiscriminator(unittest.TestCase):
    def setUp(self):
        self.discriminator = OpenJevDiscriminator()

    def test_trivial_prompt_classification(self):
        decision = self.discriminator.evaluate("fix typo in README.md header")
        self.assertLess(decision.complexity.raw_score, 0.35)
        self.assertIn(decision.complexity.level, ["trivial", "routine"])
        self.assertIn(decision.reasoning.level, ["none", "low"])
        self.assertLess(decision.reasoning.raw_score, 0.35)

    def test_routine_prompt_classification(self):
        decision = self.discriminator.evaluate("implement JWT authentication endpoint in Express with bcrypt password hashing")
        self.assertGreaterEqual(decision.complexity.raw_score, 0.30)
        self.assertLessEqual(decision.complexity.raw_score, 0.75)
        self.assertIn(decision.complexity.level, ["routine", "complex"])
        self.assertIn(decision.reasoning.level, ["low", "medium"])

    def test_frontier_prompt_classification(self):
        decision = self.discriminator.evaluate("design and implement a fault-tolerant distributed Raft consensus state machine in Rust with formal invariant verification and network partition recovery")
        self.assertGreaterEqual(decision.complexity.raw_score, 0.70)
        self.assertEqual(decision.complexity.level, "frontier_architectural")
        self.assertIn(decision.reasoning.level, ["high", "max"])
        self.assertGreaterEqual(decision.reasoning.raw_score, 0.70)

    def test_destructive_risk_noul(self):
        decision = self.discriminator.evaluate("recursively drop all staging database tables and rm -rf old build directories")
        self.assertTrue(decision.destructive_risk.is_triggered)
        self.assertGreaterEqual(decision.destructive_risk.probability, 0.50)

    def test_large_context_noul(self):
        decision = self.discriminator.evaluate("analyze whole-repository dependencies across all 40 microservices and generate a comprehensive architecture map")
        self.assertTrue(decision.large_context.is_triggered)
        self.assertGreaterEqual(decision.large_context.probability, 0.50)

    def test_harness_affinities(self):
        # Claude Code affinity (bash/terminal CLI pipes)
        d_claude = self.discriminator.evaluate("run bash commands in terminal to grep logs and pipe git status")
        self.assertEqual(d_claude.harness.selected, "claude_code")

        # Oh My Pi affinity (LSP / DAP / hashline)
        d_omp = self.discriminator.evaluate("use LSP client diagnostics and DAP debugger with hashline edits to trace Rust memory leak")
        self.assertEqual(d_omp.harness.selected, "oh_my_pi")

        # Antigravity affinity (artifacts / subagents / pair programming workspace)
        d_agy = self.discriminator.evaluate("create a pair-programming subagent in Antigravity workspace with generative UI artifacts")
        self.assertEqual(d_agy.harness.selected, "antigravity")

        # Aider affinity (git commits pair programming)
        d_aider = self.discriminator.evaluate("git commit changes and pair program in terminal with architect and editor roles")
        self.assertEqual(d_aider.harness.selected, "aider")

if __name__ == "__main__":

    unittest.main()
