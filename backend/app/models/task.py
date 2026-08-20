from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid

class AuthenticTask(SQLModel, table=True):
    __tablename__ = "authentic_tasks"
    
    task_id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    competency_id: str = Field(index=True)
    week_number: int = 1
    title: str
    problem_statement: str
    context_data: str # JSON string for background materials
    rubrics: str      # JSON string for evaluation criteria
    base_assistance_budget: int = 100
    difficulty_score: float = 50.0
    is_no_ai_assessment: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
