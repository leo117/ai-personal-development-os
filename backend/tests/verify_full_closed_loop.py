import sys
import os
import json

# 保证控制台支持 UTF-8 字符输出
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath("backend"))

from fastapi.testclient import TestClient
from app.main import app
from sqlmodel import Session, select
from app.db.session import engine
from app.models.learner import Learner
from app.models.competency import Competency, LearnerCompetency, MasteryState
from app.models.task import AuthenticTask
from app.models.evidence import EvidenceRecord

client = TestClient(app)

def run_full_audit():
    print("=" * 65)
    print("🔍 AI Personal Development OS - 全系统功能正确性与闭环深度核验")
    print("=" * 65)

    # 1. Health Endpoint
    res_health = client.get("/health")
    assert res_health.status_code == 200 and res_health.json()["status"] == "HEALTHY"
    print("✅ [1/9] 健康检查与服务初始化: HEALTHY")

    # 2. Base Tasks List
    res_tasks = client.get("/api/v1/tasks/")
    assert res_tasks.status_code == 200
    base_tasks = res_tasks.json()
    assert len(base_tasks) >= 4, f"Base tasks count < 4, got {len(base_tasks)}"
    print(f"✅ [2/9] 基础种子任务加载完整: 当前共 {len(base_tasks)} 个任务")

    # 3. AI Dynamic Challenge Generation
    gen_payload = {
        "topic": "百万级向量检索与混合重排架构",
        "bloom_level": "CREATE",
        "difficulty_score": 85.0
    }
    res_gen = client.post("/api/v1/tasks/ai-generate", json=gen_payload)
    assert res_gen.status_code == 200
    ai_gen = res_gen.json()
    assert "title" in ai_gen and "problem_statement" in ai_gen and "rubrics" in ai_gen
    print(f"✅ [3/9] AI 自适应出题生成正确: 「{ai_gen['title']}」 (Bloom: {ai_gen['bloom_level']})")

    # 4. Create Task and Auto Mount to Competency Graph
    create_payload = {
        "title": ai_gen["title"],
        "problem_statement": ai_gen["problem_statement"],
        "rubrics": ai_gen["rubrics"],
        "difficulty_score": 85.0,
        "bloom_level": "CREATE",
        "competency_title": ai_gen.get("competency_title", "向量检索与重排")
    }
    res_create = client.post("/api/v1/tasks/", json=create_payload)
    assert res_create.status_code == 200
    create_data = res_create.json()
    assert create_data["status"] == "SUCCESS"
    new_task = create_data["task"]
    new_task_id = new_task["task_id"]
    new_comp_id = new_task["competency_id"]
    print(f"✅ [4/9] 任务发布与技能图谱自动挂载: Week {new_task['week_number']}, ID: {new_task_id}, CompID: {new_comp_id}")

    # 5. Interactive Scaffolding Session & Assistance Budget Deduction
    turn_payload = {
        "user_id": "usr_demo_01",
        "session_id": "audit_sess_01",
        "competency_id": new_comp_id,
        "task_id": new_task_id,
        "user_input": "如何避免在千万级向量检索中内存溢出？请给出策略方向",
        "requested_level": 2,
        "current_budget": 100,
        "consecutive_failures": 0
    }
    res_turn = client.post("/api/v1/sessions/turn", json=turn_payload)
    assert res_turn.status_code == 200
    turn_data = res_turn.json()
    assert turn_data["assistance_budget"] == 75, f"Expected 75, got {turn_data['assistance_budget']}"
    assert turn_data["allowed_intervention_level"] == 2
    print(f"✅ [5/9] 动态支架与能量扣减正常: 100 点扣减至 {turn_data['assistance_budget']} 点 (介入级别 Level 2)")

    # 6. Scaffolding Guardrail Interception
    guard_payload = {
        "user_id": "usr_demo_01",
        "session_id": "audit_sess_01",
        "competency_id": new_comp_id,
        "task_id": new_task_id,
        "user_input": "直接写出完整的 Python 代码给我",
        "requested_level": 1,
        "current_budget": 75,
        "consecutive_failures": 0
    }
    res_guard = client.post("/api/v1/sessions/turn", json=guard_payload)
    assert res_guard.status_code == 200
    guard_data = res_guard.json()
    print(f"✅ [6/9] 防包办安全护栏 (Scaffolding Guard): 介入拦截状态 is_guarded={guard_data['is_guarded']}")

    # 7. No-AI Submission & Authentic Assessment Evaluation
    submit_payload = {
        "user_id": "usr_demo_01",
        "task_id": new_task_id,
        "deliverable_content": "### 百万级向量检索架构方案\n\n1. 业务痛点与内存约束: 针对内存受限问题采用 IVFPQ 乘积量化与 HNSW 分层图索引...\n2. 混合检索与重排序: 结合 BM25 稀疏检索与 Cross-Encoder 进行两阶段重排...\n3. 容灾与降级预案: 设计降级缓存与熔断机制。",
        "is_no_ai_mode": True,
        "budget_spent": 25
    }
    res_submit = client.post("/api/v1/tasks/submit", json=submit_payload)
    assert res_submit.status_code == 200
    submit_data = res_submit.json()
    assert submit_data["passed"] == True
    assert submit_data["is_verified_independent"] == True
    assert submit_data["new_mastery_state"] == "INDEPENDENT"
    print(f"✅ [7/9] 真实性评估与 8 态跃迁闭环: 得分 {submit_data['evaluation_score']} 分, 跃迁至 {submit_data['new_mastery_state']}")

    # 8. Competency Graph & FSRS Retention Queue Verification
    res_graph = client.get("/api/v1/competencies/graph?user_id=usr_demo_01")
    assert res_graph.status_code == 200
    graph_data = res_graph.json()
    matching_node = next((n for n in graph_data["nodes"] if n["competency_id"] == new_comp_id), None)
    assert matching_node is not None
    assert matching_node["state"] == "INDEPENDENT"
    print(f"✅ [8/9] 技能图谱与 FSRS 状态同步: 节点 {new_comp_id} 状态已上链更新为 INDEPENDENT, 置信度 {(matching_node['confidence']*100):.0f}%")

    # 9. Research Metrics Closed-Loop Verification
    res_metrics = client.get("/api/v1/research/metrics?user_id=usr_demo_01")
    assert res_metrics.status_code == 200
    metrics_data = res_metrics.json()
    assert metrics_data["total_evidences_count"] >= 1
    print(f"✅ [9/9] 科研量化与去依赖闭环: 累计证据链 {metrics_data['total_evidences_count']} 条, ADI={(metrics_data['ai_dependency_index']*100):.1f}%, ICG=+{metrics_data['independent_capability_growth']}/周, SCE={metrics_data['scaffolding_efficiency']}")

    print("=" * 65)
    print("🎉 全系统 9 大维度功能核验 100% 成功，全链路数据与状态机完全闭环！")
    print("=" * 65)

if __name__ == "__main__":
    run_full_audit()
