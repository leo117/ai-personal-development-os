from typing import TypedDict, Optional, List, Dict, Any

class AgentGraphState(TypedDict):
    # 会话与用户标识
    user_id: str
    session_id: str
    competency_id: str
    task_id: str
    
    # 学习者模型状态
    current_capability_score: float
    cognitive_load_state: str  # 'LOW', 'OPTIMAL', 'OVERLOAD'
    ai_dependency_index: float
    helplessness_risk: str     # 'LOW', 'HIGH'
    
    # 策略与支架预算
    assistance_budget: int
    requested_level: int
    allowed_intervention_level: int
    failure_type: Optional[str]
    consecutive_failures: int
    
    # 对话流
    user_input: str
    raw_agent_response: Optional[str]
    final_guarded_response: Optional[str]
    is_guarded: bool
    
    # 真实评测与交付物
    deliverable_payload: Optional[Dict[str, Any]]
    evaluation_score: Optional[float]
    evaluator_feedback: Optional[Dict[str, Any]]
    is_verified_independent: bool
