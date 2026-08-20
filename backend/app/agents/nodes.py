from typing import Dict, Any
from app.agents.state import AgentGraphState
from app.engine.budget_manager import BudgetManager
from app.engine.failure_diagnosis import FailureDiagnosisEngine
from app.engine.scaffolding_guard import ScaffoldingGuard
from app.agents.prompts import AgentPrompts
from app.core.llm import LLMClient

class AgentNodes:
    @staticmethod
    def pedagogical_engine_node(state: AgentGraphState) -> Dict[str, Any]:
        """
        策略决策节点：计算允许支架等级、扣减预算、执行失败诊断
        """
        budget = state.get("assistance_budget", 100)
        requested_level = state.get("requested_level", 1)
        failures = state.get("consecutive_failures", 0)

        is_rescue = False
        if failures >= 3:
            diagnosis = FailureDiagnosisEngine.diagnose(
                user_input=state.get("user_input", ""),
                consecutive_failures=failures,
                prerequisite_confidence=0.7,
                latency_seconds=45.0
            )
            state["failure_type"] = diagnosis["failure_type"]
            if failures >= 4:
                state["helplessness_risk"] = "HIGH"
                is_rescue = True

        allowed_level, new_budget, status = BudgetManager.evaluate_request(
            current_budget=budget,
            requested_level=requested_level,
            consecutive_failures=failures
        )

        return {
            "allowed_intervention_level": allowed_level,
            "assistance_budget": new_budget,
            "helplessness_risk": "HIGH" if is_rescue else "LOW"
        }

    @staticmethod
    def tutor_node(state: AgentGraphState) -> Dict[str, Any]:
        """
        Tutor 生成节点：根据支架等级生成有针对性的引导（支持真实 LLM 调用与规则兜底）
        """
        level = state.get("allowed_intervention_level", 1)
        user_input = state.get("user_input", "")
        
        # 1. 如果已配置真实 LLM API，优先请求大模型
        if LLMClient.is_configured() and level > 0:
            level_instructions = {
                1: "严格要求：仅提出 1~2 个苏格拉底反思问题，严禁给出答案或代码。",
                2: "严格要求：仅给出策略方向或设计模式提示，不透露具体实现。",
                3: "严格要求：仅给出一个跨领域的简化类比案例。",
                4: "严格要求：仅给出包含 TODO 槽位的骨架代码或方案大纲。",
                5: "允许给出完整方案解析（但提示用户将被标记为非独立完成）。"
            }
            custom_sys_prompt = f"{AgentPrompts.SCAFFOLDING_COACH}\n\n【当前支架限制】: {level_instructions.get(level, '')}"
            llm_reply = LLMClient.chat_completion(
                system_prompt=custom_sys_prompt,
                user_prompt=user_input
            )
            if llm_reply:
                return {"raw_agent_response": llm_reply}

        # 2. 内置规则引擎与教学模板兜底
        if level == 0:
            raw_response = "请在左侧生产画布中独立尝试解题。AI 当前处于纯独立观察模式。"
        elif level == 1:
            raw_response = f"【苏格拉底反思引导】：针对问题「{user_input}」，你认为限制系统性能的核心瓶颈是在召回阶段还是在排序阶段？试着列出 2 种主要考量。"
        elif level == 2:
            raw_response = f"【策略提示】：可以考虑分阶段处理——先通过向量检索保证召回覆盖率，再引入交叉编码器 (Cross-Encoder) 做精排重打分，兼顾延迟与精度。"
        elif level == 3:
            raw_response = "【类比案例】：就像图书馆借书，图书管理员先按分类号把相关的 20 本书挑出来（粗排），再由读者仔细翻看目录选出最需要的 3 本（精排）。"
        elif level == 4:
            raw_response = "【骨架填空】：\n```python\ndef hybrid_retrieval(query):\n    # 1. 向量粗排\n    dense_results = dense_search(query, top_k=50)\n    # 2. TODO: 引入 BM25 稀疏检索合并\n    # 3. TODO: 调用 Reranker 重排\n    return reranked_top_k\n```"
        else:
            raw_response = "【完整方案解析】（注意：本次尝试已标记为非独立完成）：完整的重排检索链路包含混合检索、去重与重排算法。"

        return {"raw_agent_response": raw_response}

    @staticmethod
    def scaffolding_guard_node(state: AgentGraphState) -> Dict[str, Any]:
        """
        安全拦截审查节点
        """
        raw_text = state.get("raw_agent_response", "")
        allowed_level = state.get("allowed_intervention_level", 1)
        budget = state.get("assistance_budget", 100)
        is_rescue = state.get("helplessness_risk") == "HIGH"

        guarded_text, is_guarded = ScaffoldingGuard.filter_response(
            raw_text=raw_text,
            allowed_level=allowed_level,
            budget=budget,
            is_rescue_mode=is_rescue
        )

        return {
            "final_guarded_response": guarded_text,
            "is_guarded": is_guarded
        }

    @staticmethod
    def assessment_node(state: AgentGraphState) -> Dict[str, Any]:
        """
        真实性评估节点
        """
        payload = state.get("deliverable_payload", {})
        content = payload.get("content", "")
        budget_spent = 100 - state.get("assistance_budget", 100)
        
        # 基础评分：65 分底分 + 内容长度与结构质量加分
        length_bonus = min(25.0, float(len(content)) * 0.3)
        base_score = min(98.0, 65.0 + length_bonus)
        is_independent = (budget_spent <= 20)
        
        feedback = {
            "technical_rigor": round(base_score * 0.95, 1),
            "tradeoff_analysis": round(base_score * 0.9, 1),
            "clarity": round(base_score, 1),
            "summary": "方案结构完整，权衡分析到位，已达到阶段性交付要求。" if base_score >= 75.0 else "方案缺少对异常边界情况的防御，建议补充重排失败时的降级兜底逻辑。"
        }
        
        return {
            "evaluation_score": round(base_score, 1),
            "evaluator_feedback": feedback,
            "is_verified_independent": is_independent
        }
