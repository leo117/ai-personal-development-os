from typing import Tuple, Dict

class BudgetManager:
    """
    负责任务初始援助预算计算与阶梯扣减
    """
    COST_TABLE: Dict[int, int] = {
        0: 0,   # Level 0: No Help
        1: 10,  # Level 1: Socratic Question
        2: 25,  # Level 2: Strategic Hint
        3: 50,  # Level 3: Concrete Example
        4: 80,  # Level 4: Partial Skeleton
        5: 100  # Level 5: Full Solution (标记非独立完成)
    }

    @staticmethod
    def calculate_initial_budget(confidence: float, difficulty: float) -> int:
        """
        根据当前能力置信度(0.0~1.0)和任务难度(0~100)动态生成初始预算点数
        B_init = Clamp(100 * (1 - (Confidence * 100) / (Difficulty + 10)), 20, 100)
        """
        raw_budget = 100.0 * (1.0 - (confidence * 100.0) / (difficulty + 10.0))
        return int(max(20.0, min(100.0, raw_budget)))

    @classmethod
    def evaluate_request(
        cls, 
        current_budget: int, 
        requested_level: int, 
        consecutive_failures: int
    ) -> Tuple[int, int, str]:
        """
        评估支架请求并返回 (实际允许等级, 扣减后剩余预算, 状态代码)
        """
        # 1. 预算已耗尽
        if current_budget <= 0:
            return 0, 0, "BUDGET_EXHAUSTED"

        # 2. 连续失败超过 3 次，强制触发失败归因诊断
        if consecutive_failures >= 3:
            deduction = cls.COST_TABLE[1]
            new_budget = max(0, current_budget - deduction)
            return 1, new_budget, "FAILURE_DIAGNOSIS_TRIGGERED"

        # 3. 降级匹配可用预算
        effective_level = requested_level
        while effective_level > 0 and cls.COST_TABLE[effective_level] > current_budget:
            effective_level -= 1

        if effective_level == 0:
            return 0, current_budget, "INSUFFICIENT_BUDGET_FOR_LEVEL"

        deduction = cls.COST_TABLE[effective_level]
        new_budget = current_budget - deduction
        return effective_level, new_budget, "APPROVED"
