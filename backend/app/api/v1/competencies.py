from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any
from app.db.session import get_session
from app.models.competency import Competency, LearnerCompetency
from app.models.learner import Learner
from app.engine.fsrs_scheduler import FSRSScheduler

router = APIRouter(prefix="/competencies", tags=["Competency Graph"])

@router.get("/graph")
def get_competency_graph(user_id: str = "usr_demo_01", db: Session = Depends(get_session)):
    """
    获取用户的技能图谱状态与雷达图数据
    """
    comps = db.exec(select(Competency)).all()
    learner_comps = db.exec(select(LearnerCompetency).where(LearnerCompetency.user_id == user_id)).all()
    
    lc_map = {lc.competency_id: lc for lc in learner_comps}
    
    nodes = []
    retention_queue = []
    
    for c in comps:
        lc = lc_map.get(c.competency_id)
        state = lc.state.value if lc else "UNKNOWN"
        confidence = lc.confidence_score if lc else 0.0
        stability = lc.stability if lc else 1.0
        retrievability = lc.retrievability if lc else 1.0
        
        # 检查是否需要 FSRS 复习 (R < 0.75)
        if retrievability < FSRSScheduler.RETENTION_THRESHOLD:
            retention_queue.append({
                "competency_id": c.competency_id,
                "title": c.title,
                "retrievability": retrievability,
                "urgency": "HIGH" if retrievability < 0.60 else "MEDIUM"
            })
            
        nodes.append({
            "competency_id": c.competency_id,
            "title": c.title,
            "description": c.description,
            "bloom_level": c.bloom_level,
            "difficulty": c.difficulty_rating,
            "state": state,
            "confidence": confidence,
            "stability": stability,
            "retrievability": retrievability
        })

    return {
        "user_id": user_id,
        "nodes": nodes,
        "retention_queue": retention_queue
    }
