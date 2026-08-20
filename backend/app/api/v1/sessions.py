from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import Optional, Dict, Any
from app.db.session import get_session
from app.models.learner import Learner
from app.models.evidence import InteractionTelemetryEvent
from app.agents.state import AgentGraphState
from app.agents.graph import MultiAgentWorkflow

router = APIRouter(prefix="/sessions", tags=["Interactive Sessions"])

class TurnRequest(BaseModel):
    user_id: str = "usr_demo_01"
    session_id: str = "sess_demo_default"
    competency_id: str = "ai_pm.rag_architecture"
    task_id: str = "task_ai_pm_rag_architecture"
    user_input: str
    requested_level: int = 1
    current_budget: int = 100
    consecutive_failures: int = 0

class TurnResponse(BaseModel):
    allowed_intervention_level: int
    assistance_budget: int
    response_text: str
    is_guarded: bool
    helplessness_risk: str

@router.post("/turn", response_model=TurnResponse)
def handle_interactive_turn(req: TurnRequest, db: Session = Depends(get_session)):
    # 构建 Agent 状态
    state: AgentGraphState = {
        "user_id": req.user_id,
        "session_id": req.session_id,
        "competency_id": req.competency_id,
        "task_id": req.task_id,
        "current_capability_score": 70.0,
        "cognitive_load_state": "OPTIMAL",
        "ai_dependency_index": 0.25,
        "helplessness_risk": "LOW",
        "assistance_budget": req.current_budget,
        "requested_level": req.requested_level,
        "allowed_intervention_level": 1,
        "failure_type": None,
        "consecutive_failures": req.consecutive_failures,
        "user_input": req.user_input,
        "raw_agent_response": None,
        "final_guarded_response": None,
        "is_guarded": False,
        "deliverable_payload": None,
        "evaluation_score": None,
        "evaluator_feedback": None,
        "is_verified_independent": False
    }

    # 执行 Multi-Agent 工作流
    result_state = MultiAgentWorkflow.run_turn(state)

    # 记录原子遥测日志
    telemetry = InteractionTelemetryEvent(
        user_id=req.user_id,
        session_id=req.session_id,
        task_id=req.task_id,
        competency_id=req.competency_id,
        event_type="PROMPT_INTERVENTION",
        intervention_level=result_state["allowed_intervention_level"],
        budget_before=req.current_budget,
        budget_after=result_state["assistance_budget"],
        duration_ms=1200,
        payload=req.user_input
    )
    db.add(telemetry)
    db.commit()

    return TurnResponse(
        allowed_intervention_level=result_state["allowed_intervention_level"],
        assistance_budget=result_state["assistance_budget"],
        response_text=result_state["final_guarded_response"] or "",
        is_guarded=result_state["is_guarded"],
        helplessness_risk=result_state["helplessness_risk"]
    )
