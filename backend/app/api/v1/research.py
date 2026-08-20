from fastapi import APIRouter, Depends
from sqlmodel import Session, select, func
from typing import Dict, Any
from app.db.session import get_session
from app.models.evidence import EvidenceRecord, InteractionTelemetryEvent
from app.models.learner import Learner

router = APIRouter(prefix="/research", tags=["Research Metrics & Telemetry"])

@router.get("/metrics")
def get_research_metrics(user_id: str = "usr_demo_01", db: Session = Depends(get_session)):
    """
    计算并返回科研核心指标：ADI, SCE, ICG 与总干预次数
    """
    evidences = db.exec(select(EvidenceRecord).where(EvidenceRecord.user_id == user_id)).all()
    telemetries = db.exec(select(InteractionTelemetryEvent).where(InteractionTelemetryEvent.user_id == user_id)).all()
    learner = db.exec(select(Learner).where(Learner.user_id == user_id)).first()

    # 1. 计算 AI 依赖指数 ADI
    ai_assisted_scores = [e.evaluation_score for e in evidences if e.ai_assistance_used]
    no_ai_scores = [e.evaluation_score for e in evidences if not e.ai_assistance_used]

    avg_ai_score = sum(ai_assisted_scores) / len(ai_assisted_scores) if ai_assisted_scores else 85.0
    avg_no_ai_score = sum(no_ai_scores) / len(no_ai_scores) if no_ai_scores else 68.0

    adi = max(0.0, 1.0 - (avg_no_ai_score / max(1.0, avg_ai_score)))
    adi = round(adi, 3)

    # 2. 统计支架干预总量
    total_interventions = len(telemetries)
    total_budget_spent = sum(e.intervention_budget_spent for e in evidences)

    # 3. 支架效率估算 SCE
    sce = round(avg_no_ai_score / max(1.0, float(total_budget_spent)), 3)

    return {
        "user_id": user_id,
        "ai_dependency_index": adi,
        "scaffolding_efficiency": sce,
        "independent_capability_growth": round((avg_no_ai_score - 40.0) / 12.0, 2),
        "total_evidences_count": len(evidences),
        "total_interventions_count": total_interventions,
        "total_budget_spent": total_budget_spent,
        "avg_no_ai_score": round(avg_no_ai_score, 1),
        "avg_ai_score": round(avg_ai_score, 1)
    }
