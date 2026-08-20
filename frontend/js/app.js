import { api } from './api.js';
import { renderBudgetBar } from './components/budget_bar.js';
import { renderProductionCanvas } from './components/production_canvas.js';
import { renderCoachConsole } from './components/coach_console.js';
import { renderCompetencyModal } from './components/competency_radar.js';
import { renderResearchModal } from './components/research_metrics.js';

// 全局应用状态
const state = {
  tasks: [],
  currentTaskIndex: 0,
  currentBudget: 100,
  currentLevel: 1,
  isNoAiMode: false,
  consecutiveFailures: 0,
  messages: [
    {
      role: "ai",
      text: "👋 你好！我是你的成长教练。当前任务是「智能客服场景 LLM 可行性评估与 PRD」。请先阅读左侧需求，遇到卡点可选择对应的支架强度向我提问。",
      is_guarded: false
    }
  ],
  graphData: null,
  researchMetrics: null
};

// 初始化
async function init() {
  state.tasks = await api.getTasks();
  state.graphData = await api.getCompetencyGraph();
  state.researchMetrics = await api.getResearchMetrics();

  renderAll();
  bindGlobalEvents();
}

function renderAll() {
  const currentTask = state.tasks[state.currentTaskIndex] || null;

  // 1. 渲染左侧生产画布
  const canvasRoot = document.getElementById("production-canvas-root");
  if (canvasRoot) {
    canvasRoot.innerHTML = renderProductionCanvas(currentTask, state.isNoAiMode);
  }

  // 2. 渲染任务切换标签
  renderTaskTabs();

  // 3. 渲染右侧 AI 陪练控制台
  const coachRoot = document.getElementById("coach-console-root");
  if (coachRoot) {
    coachRoot.innerHTML = renderCoachConsole(state.messages, state.currentLevel, state.isNoAiMode);
    
    // 渲染能量条子组件
    const budgetRoot = document.getElementById("budget-bar-root");
    if (budgetRoot) {
      budgetRoot.innerHTML = renderBudgetBar(state.currentBudget, state.currentLevel);
    }
  }

  // 4. 更新顶部指标
  if (state.researchMetrics) {
    const adiElem = document.getElementById("header-adi-val");
    if (adiElem) {
      adiElem.innerText = `${(state.researchMetrics.ai_dependency_index * 100).toFixed(0)}%`;
    }
    const icgElem = document.getElementById("header-icg-val");
    if (icgElem) {
      icgElem.innerText = `+${state.researchMetrics.independent_capability_growth}/周`;
    }
  }

  // 5. 重新绑定局部事件
  bindPanelEvents();
}

function renderTaskTabs() {
  const tabsContainer = document.getElementById("task-selector-tabs");
  if (!tabsContainer) return;

  tabsContainer.innerHTML = state.tasks.map((t, idx) => `
    <button class="task-tab ${idx === state.currentTaskIndex ? 'active' : ''}" data-index="${idx}">
      Week ${t.week_number}: ${t.title.substring(0, 14)}...
    </button>
  `).join("");

  tabsContainer.querySelectorAll(".task-tab").forEach(btn => {
    btn.addEventListener("click", () => {
      state.currentTaskIndex = parseInt(btn.dataset.index);
      state.currentBudget = 100; // 重置任务初始预算
      renderAll();
    });
  });
}

function bindPanelEvents() {
  // 支架等级选择
  document.querySelectorAll(".tier-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      state.currentLevel = parseInt(btn.dataset.level);
      renderAll();
    });
  });

  // 发送对话回合
  const sendBtn = document.getElementById("send-turn-btn");
  const inputElem = document.getElementById("coach-user-input");
  
  const handleSend = async () => {
    const text = inputElem?.value.trim();
    if (!text || state.isNoAiMode) return;

    // 记录用户消息
    state.messages.push({ role: "user", text: text, is_guarded: false });
    inputElem.value = "";
    renderAll();

    const currentTask = state.tasks[state.currentTaskIndex];
    try {
      const resp = await api.sendTurn({
        user_input: text,
        requested_level: state.currentLevel,
        current_budget: state.currentBudget,
        consecutive_failures: state.consecutiveFailures,
        competency_id: currentTask?.competency_id || "ai_pm.rag_architecture",
        task_id: currentTask?.task_id || "task_1"
      });

      state.currentBudget = resp.assistance_budget;
      state.currentLevel = resp.allowed_intervention_level;

      state.messages.push({
        role: "ai",
        text: resp.response_text,
        is_guarded: resp.is_guarded
      });

      // 滚动到底部
      setTimeout(() => {
        const box = document.getElementById("chat-history-box");
        if (box) box.scrollTop = box.scrollHeight;
      }, 50);

    } catch (e) {
      state.messages.push({
        role: "ai",
        text: "通信异常，请检查后端连接状态。",
        is_guarded: false
      });
    }
    renderAll();
  };

  sendBtn?.addEventListener("click", handleSend);
  inputElem?.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSend();
  });

  // 无 AI 模式切换
  const noAiBtn = document.getElementById("toggle-no-ai-btn");
  noAiBtn?.addEventListener("click", () => {
    state.isNoAiMode = !state.isNoAiMode;
    renderAll();
  });

  // 提交交付物并申请评估
  const submitBtn = document.getElementById("submit-deliverable-btn");
  submitBtn?.addEventListener("click", async () => {
    const editor = document.getElementById("deliverable-editor");
    const content = editor?.value.trim() || "";

    if (content.length < 10) {
      alert("请在生产画布中撰写完整的 PRD 或架构设计方案后再提交！");
      return;
    }

    const currentTask = state.tasks[state.currentTaskIndex];
    submitBtn.innerText = "⏳ 正在隔离沙箱中运行评估...";
    submitBtn.disabled = true;

    try {
      const result = await api.submitTask({
        task_id: currentTask.task_id,
        deliverable_content: content,
        is_no_ai_mode: state.isNoAiMode,
        budget_spent: 100 - state.currentBudget
      });

      // 弹出评估结果
      alert(`🎉 真实性评估结果：\n• 得分: ${result.evaluation_score} 分 (${result.passed ? '通过' : '未达标'})\n• 独立完成: ${result.is_verified_independent ? '是 (独立上链)' : '否 (辅助)'}\n• 掌握度跃迁: ${result.new_mastery_state}\n• 评价反馈: ${result.evaluator_feedback.summary}`);

      // 刷新科研指标与图谱
      state.researchMetrics = await api.getResearchMetrics();
      state.graphData = await api.getCompetencyGraph();
      renderAll();

    } catch (e) {
      alert("提交评估失败，请检查网络或后端服务！");
    } finally {
      submitBtn.innerText = "🚀 提交交付物并申请 Authentic 评估";
      submitBtn.disabled = false;
    }
  });
}

function bindGlobalEvents() {
  // 雷达图 Modal
  const radarBtn = document.getElementById("open-radar-btn");
  const radarModal = document.getElementById("radar-modal");
  const radarContent = document.getElementById("radar-modal-body");

  radarBtn?.addEventListener("click", async () => {
    state.graphData = await api.getCompetencyGraph();
    if (radarContent) radarContent.innerHTML = renderCompetencyModal(state.graphData);
    radarModal?.classList.add("active");

    document.getElementById("close-radar-modal")?.addEventListener("click", () => {
      radarModal?.classList.remove("active");
    });
  });

  // 科研指标 Modal
  const researchBtn = document.getElementById("open-research-btn");
  const researchModal = document.getElementById("research-modal");
  const researchContent = document.getElementById("research-modal-body");

  researchBtn?.addEventListener("click", async () => {
    state.researchMetrics = await api.getResearchMetrics();
    if (researchContent) researchContent.innerHTML = renderResearchModal(state.researchMetrics);
    researchModal?.classList.add("active");

    document.getElementById("close-research-modal")?.addEventListener("click", () => {
      researchModal?.classList.remove("active");
    });
  });
}

// 启动应用
document.addEventListener("DOMContentLoaded", init);
