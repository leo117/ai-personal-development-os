import unittest
import sys
import os

# 确保 backend 路径在 sys.path 中
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.engine.scaffolding_guard import ScaffoldingGuard

class TestScaffoldingGuard(unittest.TestCase):
    def test_scaffolding_guard_level_1_code_filtering(self):
        raw_response = "这里是给你的思路。```python\ndef solve():\n    return 42\n```希望对你有帮助。"
        
        sanitized, is_guarded = ScaffoldingGuard.filter_response(
            raw_text=raw_response,
            allowed_level=1,
            budget=80
        )
        
        self.assertTrue(is_guarded)
        self.assertNotIn("def solve()", sanitized)
        self.assertIn("支架安全机制折叠", sanitized)

    def test_scaffolding_guard_level_5_allows_full_code(self):
        raw_response = "```python\ndef solve():\n    return 42\n```"
        
        sanitized, is_guarded = ScaffoldingGuard.filter_response(
            raw_text=raw_response,
            allowed_level=5,
            budget=100
        )
        
        self.assertFalse(is_guarded)
        self.assertIn("def solve()", sanitized)

    def test_scaffolding_guard_budget_exhaustion_block(self):
        raw_response = "好的，我给你一个提示。"
        
        sanitized, is_guarded = ScaffoldingGuard.filter_response(
            raw_text=raw_response,
            allowed_level=2,
            budget=0
        )
        
        self.assertTrue(is_guarded)
        self.assertIn("支架能量已用尽", sanitized)

if __name__ == "__main__":
    unittest.main()
