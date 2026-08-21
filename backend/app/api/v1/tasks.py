from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from pydantic import BaseModel, Field as PydanticField
from typing import List, Optional, Dict, Any
import json
import uuid
import time
import re
from app.db.session import get_session
from app.models.task import AuthenticTask
from app.models.competency import Competency, LearnerCompetency, MasteryState
from app.models.evidence import EvidenceRecord
from app.models.learner import Learner
from app.agents.state import AgentGraphState
from app.agents.graph import MultiAgentWorkflow
from app.engine.adaptive_elo import AdaptiveEloEngine
from app.core.llm import LLMClient

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

class TaskCreateRequest(BaseModel):
    user_id: str = "usr_demo_01"
    title: str
    problem_statement: str
    rubrics: str
    difficulty_score: float = 65.0
    bloom_level: str = "ANALYZE"
    competency_id: Optional[str] = None
    competency_title: Optional[str] = None
    competency_description: Optional[str] = None

class AIGenerateTaskRequest(BaseModel):
    topic: str
    bloom_level: Optional[str] = "ANALYZE"
    difficulty_score: Optional[float] = 70.0

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

@router.post("/ai-generate")
def ai_generate_task(req: AIGenerateTaskRequest):
    """
    基于用户输入的学习主题/痛点，由 AI 自动生成符合真实评估规范的 Authentic Task
    """
    topic = req.topic.strip()
    system_prompt = (
        "你是一个顶尖的 AI 产品与工程能力培养架构师。请针对用户的学习主题或技能盲区，设计一个工业级真实业务挑战 (Authentic Challenge)。\n"
        "必须严格输出合法的 JSON 格式，不得输出任何其他文字或 Markdown 标记。JSON 结构如下：\n"
        "{\n"
        '  "title": "任务标题（如：XXX架构设计/PRD撰写）",\n'
        '  "competency_title": "技能知识点名称",\n'
        '  "competency_description": "该技能的关键知识点与考察范围简要说明",\n'
        '  "problem_statement": "详细真实的业务痛点背景与需要交付的目标成果（150字左右）",\n'
        '  "rubrics": "严谨的评测契约标准（如：1. 核心分块策略；2. 容灾与降级；3. 延迟与成本权衡）",\n'
        '  "bloom_level": "ANALYZE",\n'
        '  "difficulty_score": 75.0\n'
        "}"
    )

    user_prompt = f"请为主题「{topic}」设计一个高含金量的真实业务挑战，建议认知层级为 {req.bloom_level}，难度评分约为 {req.difficulty_score}。"

    generated_data = None
    if LLMClient.is_configured():
        raw_resp = LLMClient.chat_completion(system_prompt, user_prompt, temperature=0.7)
        if raw_resp:
            try:
                # 尝试提取 JSON 代码块
                json_str = raw_resp.strip()
                match = re.search(r"\{[\s\S]*\}", json_str)
                if match:
                    generated_data = json.loads(match.group(0))
            except Exception as e:
                print(f"[WARN] Failed to parse LLM response as JSON: {e}")

    # 兜底生成模板（如果 LLM 未配置或解析失败）
    if not generated_data:
        comp_title = topic if len(topic) <= 18 else topic[:18]
        generated_data = {
            "title": f"基于 {comp_title} 的企业级全链路方案设计与落地验证",
            "competency_title": f"{comp_title} 核心技术与架构权衡",
            "competency_description": f"掌握 {comp_title} 的核心技术原理、边界防护与性能优化指标",
            "problem_statement": f"针对业务中面临的「{topic}」关键瓶颈，设计端到端的落地系统方案。需深入解决高并发性能瓶颈、鲁棒性防御与工程边界约束，产出可直接投入评审的技术设计方案/PRD。",
            "rubrics": f"必须包含：1. 场景定义与边界分类；2. 针对 {comp_title} 的技术选型与权衡分析；3. 异常容错与性能成本核算。",
            "bloom_level": req.bloom_level or "ANALYZE",
            "difficulty_score": req.difficulty_score or 70.0
        }

    return generated_data

@router.post("/")
def create_task(req: TaskCreateRequest, db: Session = Depends(get_session)):
    """
    创建新任务并自动挂载至技能图谱与自增周次
    """
    # 1. 计算自增 week_number
    all_tasks = db.exec(select(AuthenticTask)).all()
    max_week = max([t.week_number for t in all_tasks], default=0)
    next_week = max_week + 1

    # 2. 处理 competency_id
    comp_id = req.competency_id
    if not comp_id:
        slug = re.sub(r'[^a-zA-Z0-9_]', '_', req.title.lower())[:20].strip('_')
        comp_id = f"custom.{slug}_{int(time.time()) % 10000}"

    # 3. 检查或新建技能节点
    existing_comp = db.exec(select(Competency).where(Competency.competency_id == comp_id)).first()
    if not existing_comp:
        new_comp = Competency(
            competency_id=comp_id,
            domain="AI_Product_Management",
            title=req.competency_title or req.title,
            description=req.competency_description or req.problem_statement[:80] + "...",
            bloom_level=req.bloom_level,
            difficulty_rating=req.difficulty_score
        )
        db.add(new_comp)

    # 4. 检查或新建学习者掌握度关联
    existing_lc = db.exec(
        select(LearnerCompetency)
        .where(LearnerCompetency.user_id == req.user_id)
        .where(LearnerCompetency.competency_id == comp_id)
    ).first()
    if not existing_lc:
        new_lc = LearnerCompetency(
            user_id=req.user_id,
            competency_id=comp_id,
            state=MasteryState.INTRODUCED,
            confidence_score=0.20,
            stability=1.0,
            retrievability=1.0
        )
        db.add(new_lc)

    # 5. 创建 AuthenticTask
    new_task = AuthenticTask(
        task_id=f"task_{uuid.uuid4().hex[:8]}",
        competency_id=comp_id,
        week_number=next_week,
        title=req.title,
        problem_statement=req.problem_statement,
        context_data=json.dumps({"domain": "AI_Product_Management", "level": req.bloom_level}),
        rubrics=json.dumps({"criteria": req.rubrics}),
        difficulty_score=req.difficulty_score,
        base_assistance_budget=100
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "status": "SUCCESS",
        "task": {
            "task_id": new_task.task_id,
            "competency_id": new_task.competency_id,
            "week_number": new_task.week_number,
            "title": new_task.title,
            "problem_statement": new_task.problem_statement,
            "difficulty_score": new_task.difficulty_score,
            "base_assistance_budget": new_task.base_assistance_budget,
            "rubrics": json.loads(new_task.rubrics) if new_task.rubrics else {}
        }
    }

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
