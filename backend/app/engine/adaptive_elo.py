import math

class AdaptiveEloEngine:
    """
    修正版 Elo 能力自适应估计器（引入 AI 援助惩罚因子）
    """
    @staticmethod
    def calculate_expected_score(user_ability: float, task_difficulty: float) -> float:
        """
        计算预期成功率 P(Success)
        """
        return 1.0 / (1.0 + math.pow(10.0, (task_difficulty - user_ability) / 400.0))

    @classmethod
    def update_ability(
        cls, 
        current_ability: float, 
        task_difficulty: float, 
        actual_score: float, # 0.0 ~ 1.0
        budget_spent: int, 
        initial_budget: int, 
        k_factor: float = 24.0,
        penalty_lambda: float = 0.3
    ) -> float:
        """
        更新学习者能力值 theta:
        theta_new = theta_old + K * (S - P - lambda * (BudgetSpent / B_init))
        """
        expected = cls.calculate_expected_score(current_ability, task_difficulty)
        assist_ratio = float(budget_spent) / max(1.0, float(initial_budget))
        
        delta = k_factor * (actual_score - expected - (penalty_lambda * assist_ratio))
        new_ability = current_ability + delta
        return max(0.0, round(new_ability, 2))
