export function renderResearchModal(metrics) {
  if (!metrics) return `<div>正在计算科研指标...</div>`;

  const adiPercent = (metrics.ai_dependency_index * 100).toFixed(1);
  const isHealthyAdi = metrics.ai_dependency_index <= 0.35;

  return `
    <div class="modal-header">
      <h3 style="font-size: 16px; font-weight: 700; color: #fff;">📊 科研量化指标与去 AI 依赖分析</h3>
      <button class="modal-close" id="close-research-modal">&times;</button>
    </div>

    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-bottom: 16px;">
      <div style="background: rgba(15,23,42,0.6); padding: 14px; border-radius: 8px; border: 1px solid rgba(148,163,184,0.15);">
        <div style="font-size: 11px; color: #94a3b8;">AI 依赖度指数 (ADI)</div>
        <div style="font-size: 22px; font-weight: 800; color: ${isHealthyAdi ? '#10b981' : '#f59e0b'}; margin: 4px 0;">
          ${adiPercent}%
        </div>
        <div style="font-size: 11px; color: #64748b;">
          ${isHealthyAdi ? '✓ 具备优异独立解题能力' : '⚠️ 存在一定 AI 依赖，建议增加无 AI 练习'}
        </div>
      </div>

      <div style="background: rgba(15,23,42,0.6); padding: 14px; border-radius: 8px; border: 1px solid rgba(148,163,184,0.15);">
        <div style="font-size: 11px; color: #94a3b8;">独立能力增长率 (ICG)</div>
        <div style="font-size: 22px; font-weight: 800; color: #3b82f6; margin: 4px 0;">
          +${metrics.independent_capability_growth} / 周
        </div>
        <div style="font-size: 11px; color: #64748b;">
          无 AI 均分: ${metrics.avg_no_ai_score} | AI 辅助均分: ${metrics.avg_ai_score}
        </div>
      </div>
    </div>

    <div style="background: rgba(15,23,42,0.4); padding: 12px; border-radius: 8px; font-size: 12px; color: #cbd5e1; line-height: 1.6;">
      <strong>📈 科研洞见 (RQ4 & RQ2 分析)：</strong><br>
      • 累计产生证据链记录: <strong>${metrics.total_evidences_count} 条</strong><br>
      • 触发支架干预与失败诊断: <strong>${metrics.total_interventions_count} 次</strong><br>
      • 支架转化效率 (SCE): <strong>${metrics.scaffolding_efficiency}</strong> (每点能量带来的独立能力增益)
    </div>
  `;
}
