from typing import Optional, Dict, Any

class FailureDiagnosisEngine:
    """
    负责对用户卡点与失败进行四维归因诊断与策略建议
    """
    @staticmethod
    def diagnose(
        user_input: str,
        consecutive_failures: int,
        prerequisite_confidence: float,
        latency_seconds: float,
        average_latency: float = 30.0
    ) -> Dict[str, Any]:
        # 1. 检测认知超载 (Cognitive Overload)
        if latency_seconds > (average_latency * 2.5) and consecutive_failures >= 2:
            return {
                "failure_type": "COGNITIVE_OVERLOAD",
                "diagnosis_reason": "交互延迟显著偏高且连续受挫，可能出现认知超载与心理疲劳",
                "remediation_strategy": "SUGGEST_BREAK_OR_DECOMPOSE",
                "remediation_prompt": "检测到你在此任务停留时间较长，建议深呼吸休息 3 分钟，或由 AI 协助将当前问题拆解为更小的独立子任务。"
            }

        # 2. 检测错误概念混淆 (Misconception)
        misconception_keywords = ["就是", "应该直接等于", "我以为", "总是", "肯定不需要"]
        if any(kw in user_input for kw in misconception_keywords) and consecutive_failures >= 1:
            return {
                "failure_type": "MISCONCEPTION",
                "diagnosis_reason": "用户可能存在先入为主的概念性误解或前提假设错误",
                "remediation_strategy": "COUNTER_EXAMPLE_PROMPTING",
                "remediation_prompt": "思考一下：在极高并发或边界为空的情况下，你刚才的假设还会成立吗？试着找出一个反例。"
            }

        # 3. 检测知识断层 (Knowledge Gap)
        if prerequisite_confidence < 0.60:
            return {
                "failure_type": "KNOWLEDGE_GAP",
                "diagnosis_reason": "前置技能掌握度置信度不足 (<0.60)，导致无法顺利推进当前任务",
                "remediation_strategy": "RECOMMEND_MICRO_LESSON",
                "remediation_prompt": "当前任务需要熟练的前置知识支撑。建议先查看 3 分钟核心概念微课，完成后再返回挑战。"
            }

        # 4. 默认判定为解题策略缺失 (Strategy Gap)
        return {
            "failure_type": "STRATEGY_GAP",
            "diagnosis_reason": "概念清晰但缺乏具体问题拆解与实施策略",
            "remediation_strategy": "SUB_GOAL_LABELING",
            "remediation_prompt": "不要急于写代码或撰写方案，先列出解决本问题的 3 个关键步骤大纲（Sub-goals）。"
        }
