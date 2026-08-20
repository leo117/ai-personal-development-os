import re
from typing import Tuple

class ScaffoldingGuard:
    """
    负责对 Tutor Agent 输出进行后验审查与安全脱敏，确保不向用户泄露完整代码与直接答案
    """
    CODE_BLOCK_PATTERN = re.compile(r"```(?:python|javascript|typescript|sql|bash)?[\s\S]*?```", re.IGNORECASE)
    DIRECT_ANSWER_CUES = ["答案是", "可以直接复制", "完整的实现如下", "here is the full code", "代码如下："]

    @classmethod
    def filter_response(
        cls, 
        raw_text: str, 
        allowed_level: int, 
        budget: int,
        is_rescue_mode: bool = False
    ) -> Tuple[str, bool]:
        """
        过滤并审查 AI 输出
        返回: (处理后的响应文本, 是否触发了拦截/折叠)
        """
        # 1. Level 5 允许完整解答
        if allowed_level >= 5:
            return raw_text, False

        # 2. 动机救援模式下允许适度放宽
        if is_rescue_mode and allowed_level >= 3:
            return raw_text, False

        # 3. 预算耗尽熔断保护
        if budget <= 0:
            return (
                "⚠️ **支架能量已用尽**：AI 当前暂停提供进一步提示。请整理已有思路，在左侧生产画布中独立完成方案编写并提交评估。", 
                True
            )

        # 4. 等级 1~2 严禁泄露完整可运行代码块
        if allowed_level in [1, 2]:
            if cls.CODE_BLOCK_PATTERN.search(raw_text):
                sanitized = cls.CODE_BLOCK_PATTERN.sub(
                    "*(完整代码已由支架安全机制折叠。请根据上述思路尝试自行构建代码骨架)*", 
                    raw_text
                )
                return sanitized, True

        # 5. 审查直接答案口令
        for cue in cls.DIRECT_ANSWER_CUES:
            if cue in raw_text and allowed_level <= 2:
                sanitized = raw_text.replace(cue, "关键思路启发如下：")
                return sanitized, True

        return raw_text, False
