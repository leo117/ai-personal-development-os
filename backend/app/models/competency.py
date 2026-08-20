from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
import uuid

class MasteryState(str, Enum):
    UNKNOWN = "UNKNOWN"
    INTRODUCED = "INTRODUCED"
    UNDERSTOOD = "UNDERSTOOD"
    PRACTICED = "PRACTICED"
    FUNCTIONAL = "FUNCTIONAL"
    INDEPENDENT = "INDEPENDENT"
    TRANSFERABLE = "TRANSFERABLE"
    MASTERED = "MASTERED"

class Competency(SQLModel, table=True):
    __tablename__ = "competencies"
    
    competency_id: str = Field(primary_key=True) # e.g. 'ai_pm.rag_architecture'
    domain: str = Field(index=True)
    title: str
    description: str
    bloom_level: str # REMEMBER, UNDERSTAND, APPLY, ANALYZE, EVALUATE, CREATE
    difficulty_rating: float = 50.0
    stability_factor: float = 1.0
    created_at: datetime = Field(default_factory=datetime.utcnow)

class LearnerCompetency(SQLModel, table=True):
    __tablename__ = "learner_competencies"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    competency_id: str = Field(index=True)
    state: MasteryState = Field(default=MasteryState.UNKNOWN)
    confidence_score: float = 0.0
    independent_success_count: int = 0
    
    # FSRS 模型字段
    stability: float = 1.0        # 熟练度稳定性 (天)
    difficulty_fsrs: float = 5.0  # 个人主观难度 (1.0 ~ 10.0)
    retrievability: float = 1.0   # 当前可提取性/熟练度
    last_practiced_at: Optional[datetime] = None
    next_retention_test_at: Optional[datetime] = None
    updated_at: datetime = Field(default_factory=datetime.utcnow)
