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

    def test_ai_generate_task(self):
        payload = {
            "topic": "多模态 Agent 检索与状态机设计",
            "bloom_level": "CREATE",
            "difficulty_score": 85.0
        }
        response = self.client.post("/api/v1/tasks/ai-generate", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("title", data)
        self.assertIn("problem_statement", data)
        self.assertIn("rubrics", data)
        self.assertIn("competency_title", data)

    def test_create_custom_task(self):
        payload = {
            "user_id": "usr_demo_01",
            "title": "高并发缓存分流降本实战架构",
            "problem_statement": "针对千万级高并发场景设计语义缓存与小模型路由方案",
            "rubrics": "必须包含：1. 缓存淘汰策略；2. 准确率评估；3. 延迟与降级。",
            "difficulty_score": 75.0,
            "bloom_level": "ANALYZE",
            "competency_title": "LLM 语义缓存与分流降本"
        }
        response = self.client.post("/api/v1/tasks/", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "SUCCESS")
        self.assertIn("task", data)
        self.assertGreaterEqual(data["task"]["week_number"], 5)

    def test_research_metrics(self):
        response = self.client.get("/api/v1/research/metrics?user_id=usr_demo_01")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ai_dependency_index", data)
        self.assertIn("scaffolding_efficiency", data)
        self.assertIn("independent_capability_growth", data)

if __name__ == "__main__":
    unittest.main()
