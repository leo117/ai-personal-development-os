export function renderCompetencyModal(graphData) {
  const nodes = graphData.nodes || [];
  const retentionQueue = graphData.retention_queue || [];

  const stateColors = {
    UNKNOWN: "#64748b",
    INTRODUCED: "#3b82f6",
    UNDERSTOOD: "#8b5cf6",
    PRACTICED: "#f59e0b",
    FUNCTIONAL: "#10b981",
    INDEPENDENT: "#06b6d4",
    TRANSFERABLE: "#ec4899",
    MASTERED: "#eab308"
  };

  const nodeCards = nodes.map(n => `
    <div style="background: rgba(15,23,42,0.6); border: 1px solid rgba(148,163,184,0.15); padding: 12px; border-radius: 8px;">
      <div style="display: flex; justify-content: space-between; align-items: center;">
        <strong style="font-size: 13px; color: #fff;">${n.title}</strong>
        <span style="font-size: 10px; font-weight: 700; color: ${stateColors[n.state] || '#64748b'}; background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px;">
          ${n.state}
        </span>
      </div>
      <div style="font-size: 11px; color: #94a3b8; margin: 4px 0;">${n.description}</div>
      <div style="display: flex; gap: 12px; font-size: 11px; color: #cbd5e1; margin-top: 6px;">
        <span>置信度: ${(n.confidence * 100).toFixed(0)}%</span>
        <span>稳定性 S: ${n.stability}天</span>
        <span>可提取性 R: ${(n.retrievability * 100).toFixed(0)}%</span>
      </div>
    </div>
  `).join("");

  const retentionCards = retentionQueue.map(r => `
    <div style="background: rgba(239,68,68,0.1); border-left: 3px solid #ef4444; padding: 8px 12px; border-radius: 4px; font-size: 12px; margin-bottom: 6px;">
      ⚠️ <strong>${r.title}</strong> 可提取性跌破 75% (${(r.retrievability * 100).toFixed(0)}%)，建议触发 FSRS 延迟真实挑战！
    </div>
  `).join("");

  return `
    <div class="modal-header">
      <h3 style="font-size: 16px; font-weight: 700; color: #fff;">🕸️ 个人技能图谱与 FSRS 复习调度</h3>
      <button class="modal-close" id="close-radar-modal">&times;</button>
    </div>
    ${retentionQueue.length > 0 ? `<div style="margin-bottom: 14px;">${retentionCards}</div>` : ''}
    <div style="display: flex; flex-direction: column; gap: 10px; max-height: 420px; overflow-y: auto;">
      ${nodeCards}
    </div>
  `;
}
