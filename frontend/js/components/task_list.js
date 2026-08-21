/**
 * AI Personal Development OS - 右侧垂直任务列表组件
 */
export function renderTaskList(tasks = [], currentIndex = 0) {
  if (!tasks || tasks.length === 0) {
    return `
      <div style="text-align: center; color: var(--text-muted); padding: 30px 10px; font-size: 12px;">
        暂无挑战任务，点击顶部「✨ AI 智能出题」生成第一个挑战。
      </div>
    `;
  }

  return tasks.map((t, idx) => {
    const isActive = idx === currentIndex;
    
    // 难度 / Bloom 等级高亮颜色
    const bloomColorMap = {
      'UNDERSTAND': '#38bdf8',
      'APPLY': '#34d399',
      'ANALYZE': '#818cf8',
      'EVALUATE': '#fbbf24',
      'CREATE': '#f472b6'
    };
    const bloomLevel = t.bloom_level || 'ANALYZE';
    const badgeColor = bloomColorMap[bloomLevel] || '#818cf8';
    const diffScore = t.difficulty_score || 70;

    return `
      <div class="task-list-item ${isActive ? 'active' : ''}" data-index="${idx}">
        <div class="task-item-header">
          <span class="week-pill">Week ${t.week_number}</span>
          <div style="display: flex; align-items: center; gap: 6px;">
            <span class="diff-badge" style="color: ${badgeColor}; border: 1px solid ${badgeColor}40; background: ${badgeColor}18;">
              ${bloomLevel} · ${diffScore}分
            </span>
            <button class="delete-task-btn" data-task-id="${t.task_id}" data-task-title="${t.title.replace(/"/g, '&quot;')}" title="删除此挑战" onclick="event.stopPropagation();">
              🗑️
            </button>
          </div>
        </div>
        <div class="task-item-title">${t.title}</div>
        <div class="task-item-desc">${t.problem_statement ? t.problem_statement.replace(/[\r\n]+/g, ' ') : ''}</div>
        ${isActive ? `
          <div class="task-active-indicator">
            <span class="pulse-dot"></span>
            <span>当前挑战中</span>
          </div>
        ` : ''}
      </div>
    `;
  }).join("");
}
