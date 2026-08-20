import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine.fsrs_scheduler import FSRSScheduler

class TestFSRSScheduler(unittest.TestCase):
    def test_retrievability_decay(self):
        r0 = FSRSScheduler.calculate_retrievability(days_elapsed=0.0, stability=5.0)
        self.assertEqual(r0, 1.0)

        r5 = FSRSScheduler.calculate_retrievability(days_elapsed=5.0, stability=5.0)
        self.assertTrue(0.60 < r5 < 0.95)

    def test_stability_growth_on_success(self):
        init_stability = 2.0
        new_s, next_date = FSRSScheduler.update_stability_after_review(
            current_stability=init_stability,
            difficulty=4.0,
            current_r=0.75,
            review_score=85.0
        )
        self.assertGreater(new_s, init_stability)
        self.assertIsNotNone(next_date)

if __name__ == "__main__":
    unittest.main()
