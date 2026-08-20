import math
from datetime import datetime, timezone, timedelta
from typing import Tuple, Dict, Any

class FSRSScheduler:
    """
    高阶能力真实情境 FSRS 记忆衰减与复习调度器
    R(t) = (1 + F * t / S)^(-w)
    """
    F: float = 0.19
    W: float = 0.50
    RETENTION_THRESHOLD: float = 0.75  # 可提取性低于 75% 触发复习

    @classmethod
    def calculate_retrievability(cls, days_elapsed: float, stability: float) -> float:
        """
        计算经过 t 天后的能力可提取性 R(t)
        """
        if stability <= 0.0:
            return 0.0
        if days_elapsed <= 0.0:
            return 1.0
        
        factor = 1.0 + (cls.F * days_elapsed / stability)
        return float(math.pow(factor, -cls.W))

    @classmethod
    def update_stability_after_review(
        cls, 
        current_stability: float, 
        difficulty: float, 
        current_r: float, 
        review_score: float # 0.0 ~ 100.0
    ) -> Tuple[float, datetime]:
        """
        根据复习得分更新记忆稳定性 S，并计算下一次复习时间
        """
        is_success = review_score >= 70.0
        
        if is_success:
            scale = 1.0 + math.exp(1.2) * (11.0 - difficulty) * math.pow(current_stability, -0.2) * (math.exp((1.0 - current_r) * 0.8) - 1.0)
            new_stability = max(current_stability * 1.5, current_stability * scale)
        else:
            new_stability = max(1.0, current_stability * 0.5)

        interval_days = new_stability * ((math.pow(cls.RETENTION_THRESHOLD, -1.0 / cls.W) - 1.0) / cls.F)
        interval_days = max(1.0, interval_days)
        
        next_review_at = datetime.now(timezone.utc) + timedelta(days=interval_days)
        return round(new_stability, 2), next_review_at
