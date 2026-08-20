export function renderProductionCanvas(task, isNoAiMode) {
  if (!task) {
    return `<div style="color: #94a3b8; text-align: center; padding: 40px;">正在加载任务...</div>`;
  }

  return `
    <div class="task-card">
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
        <span style="font-size: 11px; font-weight: 700; color: #3b82f6;">WEEK ${task.week_number} AUTHENTIC CHALLENGE</span>
        <span style="font-size: 11px; background: rgba(59,130,246,0.15); color: #60a5fa; padding: 2px 6px; border-radius: 4px;">难度: ${task.difficulty_score}</span>
      </div>
      <div class="task-card-title">${task.title}</div>
      <div class="task-card-statement">${task.problem_statement}</div>
      <div class="task-rubrics">
        <strong>📋 证据契约评测标准 (Rubrics)：</strong><br>
        ${task.rubrics?.criteria || "要求方案具备技术可行性、边界防护与明确权衡分析。"}
      </div>
    </div>

    <div class="editor-area">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <span style="font-size: 12px; font-weight: 600; color: #cbd5e1;">📄 生产交付物撰写区 (PRD / Architecture Markdown)</span>
        <span style="font-size: 11px; color: ${isNoAiMode ? '#10b981' : '#94a3b8'};">
          ${isNoAiMode ? '🔒 闭卷独立测试中 (AI 通道已切断)' : '💡 支架陪练模式'}
        </span>
      </div>
      <textarea id="deliverable-editor" class="editor-textarea" placeholder="# 1. 业务目标与边界定义&#10;&#10;## 2. 核心架构与多路召回设计&#10;&#10;## 3. 权衡分析 (Trade-offs)..."></textarea>
    </div>

    <div class="canvas-footer">
      <button id="toggle-no-ai-btn" class="btn-no-ai">
        ${isNoAiMode ? '🔓 退出独立模式' : '🔒 进入无 AI 独立评估模式'}
      </button>
      <button id="submit-deliverable-btn" class="btn-primary">
        🚀 提交交付物并申请 Authentic 评估
      </button>
    </div>
  `;
}
