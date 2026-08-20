from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class Learner(SQLModel, table=True):
    __tablename__ = "learners"
    
    user_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    email: str = Field(index=True, unique=True)
    current_role: Optional[str] = "Product Manager"
    target_role: str = "AI Product Manager"
    weekly_hours_budget: float = 10.0
    career_stage: str = "MID"  # NOVICE, MID, SENIOR, TRANSITIONING
    motivation_type: str = "INTRINSIC"  # INTRINSIC, IDENTIFIED, EXTERNAL
    agency_score: float = 0.500
    ai_dependency_index: float = 0.500
    current_load_level: str = "OPTIMAL"  # LOW, OPTIMAL, OVERLOAD
    fatigue_index: float = 0.000
    helplessness_risk_level: str = "LOW"  # LOW, MEDIUM, HIGH
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
