import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine.budget_manager import BudgetManager

class TestBudgetManager(unittest.TestCase):
    def test_initial_budget_calculation(self):
        budget_low = BudgetManager.calculate_initial_budget(confidence=0.8, difficulty=30.0)
        self.assertLessEqual(budget_low, 40)

        budget_high = BudgetManager.calculate_initial_budget(confidence=0.0, difficulty=90.0)
        self.assertEqual(budget_high, 100)

    def test_budget_deduction_and_downgrade(self):
        level, new_budget, status = BudgetManager.evaluate_request(
            current_budget=60,
            requested_level=4,
            consecutive_failures=0
        )
        self.assertEqual(level, 3)
        self.assertEqual(new_budget, 10)
        self.assertEqual(status, "APPROVED")

    def test_consecutive_failures_forces_level_1(self):
        level, new_budget, status = BudgetManager.evaluate_request(
            current_budget=100,
            requested_level=4,
            consecutive_failures=3
        )
        self.assertEqual(level, 1)
        self.assertEqual(status, "FAILURE_DIAGNOSIS_TRIGGERED")

if __name__ == "__main__":
    unittest.main()
