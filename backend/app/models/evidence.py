from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class EvidenceRecord(SQLModel, table=True):
    __tablename__ = "evidence_records"
    
    evidence_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    user_id: str = Field(index=True)
    competency_id: str = Field(index=True)
    task_id: str = Field(index=True)
    submission_payload: str # JSON string of deliverables (PRD, code, analysis)
    ai_assistance_used: bool = False
    intervention_budget_spent: int = 0
    evaluation_score: float = 0.0
    evaluator_feedback: str # JSON string of feedback
    is_verified_independent: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)

class InteractionTelemetryEvent(SQLModel, table=True):
    __tablename__ = "interaction_telemetry_events"
    
    event_id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    session_id: str = Field(index=True)
    task_id: Optional[str] = None
    competency_id: Optional[str] = None
    event_type: str # PROMPT_INPUT, HINT_REQUEST, CODE_RUN, REFLECTION
    intervention_level: int = 0
    budget_before: int = 100
    budget_after: int = 100
    failure_type: Optional[str] = None
    duration_ms: int = 0
    cognitive_load_estimate: str = "OPTIMAL"
    payload: Optional[str] = None # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)
