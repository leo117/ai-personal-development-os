from typing import Dict, Any
from app.agents.state import AgentGraphState
from app.agents.nodes import AgentNodes

class MultiAgentWorkflow:
    """
    状态图执行器：负责将 User Input 通过策略决策、Tutor 生成、Scaffolding 拦截器流转
    """
    @staticmethod
    def run_turn(state: AgentGraphState) -> AgentGraphState:
        # 1. 策略引擎决策
        pedagogy_update = AgentNodes.pedagogical_engine_node(state)
        state.update(pedagogy_update)

        # 2. 领域知识/Coach 生成
        tutor_update = AgentNodes.tutor_node(state)
        state.update(tutor_update)

        # 3. 支架安全拦截器审查
        guard_update = AgentNodes.scaffolding_guard_node(state)
        state.update(guard_update)

        return state

    @staticmethod
    def run_assessment(state: AgentGraphState) -> AgentGraphState:
        # 评测流水线
        assessment_update = AgentNodes.assessment_node(state)
        state.update(assessment_update)
        return state
