from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import json
from app.db.session import get_session
from app.models.task import AuthenticTask
from app.models.competency import LearnerCompetency, MasteryState
from app.models.evidence import EvidenceRecord
from app.models.learner import Learner
from app.agents.state import AgentGraphState
from app.agents.graph import MultiAgentWorkflow
from app.engine.adaptive_elo import AdaptiveEloEngine

router = APIRouter(prefix="/tasks", tags=["Authentic Tasks & Assessment"])

class SubmissionRequest(BaseModel):
    user_id: str = "usr_demo_01"
    task_id: str
    deliverable_content: str
    is_no_ai_mode: bool = False
    budget_spent: int = 25

class SubmissionResponse(BaseModel):
    evidence_id: str
    evaluation_score: float
    passed: bool
    is_verified_independent: bool
    new_mastery_state: str
    evaluator_feedback: Dict[str, Any]

@router.get("/")
def list_tasks(db: Session = Depends(get_session)):
    tasks = db.exec(select(AuthenticTask).order_by(AuthenticTask.week_number)).all()
    result = []
    for t in tasks:
        result.append({
            "task_id": t.task_id,
            "competency_id": t.competency_id,
            "week_number": t.week_number,
            "title": t.title,
            "problem_statement": t.problem_statement,
            "difficulty_score": t.difficulty_score,
            "base_assistance_budget": t.base_assistance_budget,
            "rubrics": json.loads(t.rubrics) if t.rubrics else {}
        })
    return result

@router.post("/submit", response_model=SubmissionResponse)
def submit_task_deliverable(req: SubmissionRequest, db: Session = Depends(get_session)):
    task = db.exec(select(AuthenticTask).where(AuthenticTask.task_id == req.task_id)).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # 运行 Assessment 状态机评测
    state: AgentGraphState = {
        "user_id": req.user_id,
        "session_id": "eval_session",
        "competency_id": task.competency_id,
        "task_id": req.task_id,
        "current_capability_score": 70.0,
        "cognitive_load_state": "OPTIMAL",
        "ai_dependency_index": 0.25,
        "helplessness_risk": "LOW",
        "assistance_budget": 100 - req.budget_spent,
        "requested_level": 0,
        "allowed_intervention_level": 0,
        "failure_type": None,
        "consecutive_failures": 0,
        "user_input": "",
        "raw_agent_response": None,
        "final_guarded_response": None,
        "is_guarded": False,
        "deliverable_payload": {"content": req.deliverable_content},
        "evaluation_score": None,
        "evaluator_feedback": None,
        "is_verified_independent": False
    }

    eval_result = MultiAgentWorkflow.run_assessment(state)
    score = eval_result["evaluation_score"] or 75.0
    passed = score >= 70.0
    is_independent = eval_result["is_verified_independent"] or req.is_no_ai_mode

    # 记录证据链
    evidence = EvidenceRecord(
        user_id=req.user_id,
        competency_id=task.competency_id,
        task_id=req.task_id,
        submission_payload=json.dumps({"content": req.deliverable_content}),
        ai_assistance_used=not is_independent,
        intervention_budget_spent=req.budget_spent,
        evaluation_score=score,
        evaluator_feedback=json.dumps(eval_result["evaluator_feedback"]),
        is_verified_independent=is_independent
    )
    db.add(evidence)

    # 更新学习者掌握度状态机
    lc = db.exec(
        select(LearnerCompetency)
        .where(LearnerCompetency.user_id == req.user_id)
        .where(LearnerCompetency.competency_id == task.competency_id)
    ).first()

    new_state_str = "UNKNOWN"
    if lc:
        if passed and is_independent:
            lc.state = MasteryState.INDEPENDENT
            lc.independent_success_count += 1
            lc.confidence_score = min(1.0, lc.confidence_score + 0.25)
        elif passed:
            lc.state = MasteryState.PRACTICED
            lc.confidence_score = min(1.0, lc.confidence_score + 0.15)
        new_state_str = lc.state.value
        db.add(lc)

    db.commit()

    return SubmissionResponse(
        evidence_id=evidence.evidence_id,
        evaluation_score=score,
        passed=passed,
        is_verified_independent=is_independent,
        new_mastery_state=new_state_str,
        evaluator_feedback=eval_result["evaluator_feedback"] or {}
    )
