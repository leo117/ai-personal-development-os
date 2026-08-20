export function renderBudgetBar(budget, level) {
  const percent = Math.max(0, Math.min(100, budget));
  let color = "linear-gradient(90deg, #10b981, #3b82f6)";
  if (percent <= 20) {
    color = "linear-gradient(90deg, #ef4444, #f59e0b)";
  } else if (percent <= 50) {
    color = "linear-gradient(90deg, #f59e0b, #3b82f6)";
  }

  const levelNames = {
    0: "Level 0: No Help (纯独立)",
    1: "Level 1: Socratic (反思启发)",
    2: "Level 2: Strategic (策略提示)",
    3: "Level 3: Analogy (场景类比)",
    4: "Level 4: Partial (骨架填空)",
    5: "Level 5: Full Solution (全解)"
  };

  return `
    <div class="budget-bar-header">
      <span>⚡ 支架援助能量 (Assistance Budget)</span>
      <span style="color: ${percent <= 20 ? '#ef4444' : '#10b981'}">${budget} / 100 点</span>
    </div>
    <div class="budget-progress-track">
      <div class="budget-progress-fill" style="width: ${percent}%; background: ${color};"></div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 10px;">
      <span style="font-size: 11px; color: #94a3b8;">当前介入强度:</span>
      <span class="level-badge">${levelNames[level] || "Level 1"}</span>
    </div>
  `;
}
