import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app.main import app

class TestAPIEndpoints(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def test_health_endpoint(self):
        response = self.client.get("/health")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["status"], "HEALTHY")

    def test_list_tasks(self):
        response = self.client.get("/api/v1/tasks/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertGreater(len(data), 0)
        self.assertEqual(data[0]["week_number"], 1)

    def test_competency_graph(self):
        response = self.client.get("/api/v1/competencies/graph?user_id=usr_demo_01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("nodes", data)
        self.assertIn("retention_queue", data)

    def test_interactive_turn_session(self):
        payload = {
            "user_id": "usr_demo_01",
            "session_id": "sess_test_01",
            "competency_id": "ai_pm.rag_architecture",
            "task_id": "task_ai_pm_rag_architecture",
            "user_input": "我想了解多路召回如何实现？",
            "requested_level": 2,
            "current_budget": 100,
            "consecutive_failures": 0
        }
        response = self.client.post("/api/v1/sessions/turn", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["allowed_intervention_level"], 2)
        self.assertEqual(data["assistance_budget"], 75)
        self.assertIn("策略提示", data["response_text"])

    def test_task_submission_and_assessment(self):
        payload = {
            "user_id": "usr_demo_01",
            "task_id": "task_ai_pm_fundamentals",
            "deliverable_content": "### 智能客服场景可行性评估 PRD\n\n1. 场景分析与适用性边界定义...\n2. 预期成本与多模型路由设计...",
            "is_no_ai_mode": True,
            "budget_spent": 10
        }
        response = self.client.post("/api/v1/tasks/submit", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data["passed"])
        self.assertTrue(data["is_verified_independent"])
        self.assertEqual(data["new_mastery_state"], "INDEPENDENT")

    def test_research_metrics(self):
        response = self.client.get("/api/v1/research/metrics?user_id=usr_demo_01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ai_dependency_index", data)
        self.assertIn("scaffolding_efficiency", data)
        self.assertIn("independent_capability_growth", data)

if __name__ == "__main__":
    unittest.main()
