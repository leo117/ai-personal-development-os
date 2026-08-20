import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.agents.state import AgentGraphState
from app.agents.graph import MultiAgentWorkflow

class TestAgentWorkflow(unittest.TestCase):
    def test_multi_agent_workflow_turn_execution(self):
        state: AgentGraphState = {
            "user_id": "usr_test",
            "session_id": "sess_test",
            "competency_id": "ai_pm.rag_architecture",
            "task_id": "task_1",
            "current_capability_score": 60.0,
            "cognitive_load_state": "OPTIMAL",
            "ai_dependency_index": 0.3,
            "helplessness_risk": "LOW",
            "assistance_budget": 80,
            "requested_level": 2,
            "allowed_intervention_level": 2,
            "failure_type": None,
            "consecutive_failures": 0,
            "user_input": "如何优化检索准确率？",
            "raw_agent_response": None,
            "final_guarded_response": None,
            "is_guarded": False,
            "deliverable_payload": None,
            "evaluation_score": None,
            "evaluator_feedback": None,
            "is_verified_independent": False
        }

        result = MultiAgentWorkflow.run_turn(state)

        self.assertEqual(result["allowed_intervention_level"], 2)
        self.assertLess(result["assistance_budget"], 80)
        self.assertIsNotNone(result["final_guarded_response"])
        self.assertTrue(len(result["final_guarded_response"]) > 0)

    def test_multi_agent_assessment_execution(self):
        state: AgentGraphState = {
            "user_id": "usr_test",
            "session_id": "sess_test",
            "competency_id": "ai_pm.rag_architecture",
            "task_id": "task_1",
            "current_capability_score": 60.0,
            "cognitive_load_state": "OPTIMAL",
            "ai_dependency_index": 0.3,
            "helplessness_risk": "LOW",
            "assistance_budget": 100,
            "requested_level": 0,
            "allowed_intervention_level": 0,
            "failure_type": None,
            "consecutive_failures": 0,
            "user_input": "",
            "raw_agent_response": None,
            "final_guarded_response": None,
            "is_guarded": False,
            "deliverable_payload": {"content": "一份长达500字的高质量RAG架构设计文档，包含多路召回与重排方案..."},
            "evaluation_score": None,
            "evaluator_feedback": None,
            "is_verified_independent": False
        }

        result = MultiAgentWorkflow.run_assessment(state)

        self.assertGreaterEqual(result["evaluation_score"], 70.0)
        self.assertIn("technical_rigor", result["evaluator_feedback"])

if __name__ == "__main__":
    unittest.main()
