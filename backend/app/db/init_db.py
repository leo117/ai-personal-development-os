import json
import os
from sqlmodel import Session, select
from app.db.session import engine, init_db
from app.models.learner import Learner
from app.models.competency import Competency, LearnerCompetency, MasteryState
from app.models.task import AuthenticTask

def seed_database():
    init_db()
    
    with Session(engine) as session:
        # 1. 初始化默认学习者
        existing_learner = session.exec(select(Learner).where(Learner.email == "demo@learner.ai")).first()
        if not existing_learner:
            learner = Learner(
                user_id="usr_demo_01",
                email="demo@learner.ai",
                current_role="Senior Product Manager",
                target_role="AI Product Lead",
                weekly_hours_budget=12.0,
                career_stage="MID",
                motivation_type="INTRINSIC",
                agency_score=0.68,
                ai_dependency_index=0.25,
                current_load_level="OPTIMAL"
            )
            session.add(learner)
            session.commit()
            print("[OK] Default Learner profile seeded.")

        # 2. 读取并初始化 AI PM 课程技能树
        seed_path = os.path.join(os.path.dirname(__file__), "..", "seeds", "ai_pm_curriculum.json")
        if os.path.exists(seed_path):
            with open(seed_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                domain = data["domain"]
                
                for idx, comp_data in enumerate(data["competencies"]):
                    # 技能节点
                    comp_id = comp_data["competency_id"]
                    existing_comp = session.exec(select(Competency).where(Competency.competency_id == comp_id)).first()
                    if not existing_comp:
                        comp = Competency(
                            competency_id=comp_id,
                            domain=domain,
                            title=comp_data["title"],
                            description=comp_data["description"],
                            bloom_level=comp_data["bloom_level"],
                            difficulty_rating=comp_data["difficulty_rating"]
                        )
                        session.add(comp)

                    # 关联学习者技能掌握度
                    existing_lc = session.exec(
                        select(LearnerCompetency)
                        .where(LearnerCompetency.user_id == "usr_demo_01")
                        .where(LearnerCompetency.competency_id == comp_id)
                    ).first()
                    if not existing_lc:
                        state = MasteryState.UNDERSTOOD if idx == 0 else (MasteryState.INTRODUCED if idx == 1 else MasteryState.UNKNOWN)
                        lc = LearnerCompetency(
                            user_id="usr_demo_01",
                            competency_id=comp_id,
                            state=state,
                            confidence_score=0.65 if idx == 0 else (0.40 if idx == 1 else 0.0),
                            stability=3.5 if idx == 0 else 1.0,
                            retrievability=0.92 if idx == 0 else 0.85
                        )
                        session.add(lc)

                    # 任务
                    task_data = comp_data["task"]
                    existing_task = session.exec(select(AuthenticTask).where(AuthenticTask.competency_id == comp_id)).first()
                    if not existing_task:
                        task = AuthenticTask(
                            task_id=f"task_{comp_id.replace('.', '_')}",
                            competency_id=comp_id,
                            week_number=idx + 1,
                            title=task_data["title"],
                            problem_statement=task_data["problem_statement"],
                            context_data=json.dumps({"domain": domain, "level": comp_data["bloom_level"]}),
                            rubrics=json.dumps({"criteria": task_data["rubrics"]}),
                            difficulty_score=comp_data["difficulty_rating"],
                            base_assistance_budget=100
                        )
                        session.add(task)

                session.commit()
                print("[OK] AI PM Competency Graph and Authentic Tasks seeded.")

if __name__ == "__main__":
    seed_database()
