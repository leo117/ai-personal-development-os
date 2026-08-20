export function renderCoachConsole(messages, currentLevel, isNoAiMode) {
  const messageItems = messages.map(m => `
    <div class="chat-message ${m.role} ${m.is_guarded ? 'guarded' : ''}">
      ${m.is_guarded ? '<div style="font-size: 10px; color: #f59e0b; font-weight: 700; margin-bottom: 4px;">🛡️ SCAFFOLDING GUARD INTERCEPTED</div>' : ''}
      <div>${escapeHtml(m.text)}</div>
    </div>
  `).join("");

  return `
    <div id="budget-bar-root" class="budget-bar-container"></div>

    <div style="margin-top: 4px;">
      <span style="font-size: 11px; color: #94a3b8; font-weight: 600;">选择请求支架强度：</span>
      <div class="scaffolding-tier-selector">
        <button class="tier-btn ${currentLevel === 1 ? 'selected' : ''}" data-level="1">Q1: 反问 (10点)</button>
        <button class="tier-btn ${currentLevel === 2 ? 'selected' : ''}" data-level="2">Q2: 提示 (25点)</button>
        <button class="tier-btn ${currentLevel === 3 ? 'selected' : ''}" data-level="3">Q3: 类比 (50点)</button>
        <button class="tier-btn ${currentLevel === 4 ? 'selected' : ''}" data-level="4">Q4: 骨架 (80点)</button>
      </div>
    </div>

    <div class="chat-history" id="chat-history-box">
      ${messageItems.length > 0 ? messageItems : '<div style="color: #64748b; font-size: 12px; text-align: center; margin-top: 80px;">AI 陪练就绪。提出你的问题或卡点，Coach 将提供受控支架引导。</div>'}
    </div>

    <div class="chat-input-row">
      <input type="text" id="coach-user-input" class="chat-input" placeholder="${isNoAiMode ? '独立测试模式下 AI 通道已锁定...' : '输入你的问题或思考假设（Enter 发送）...'}" ${isNoAiMode ? 'disabled' : ''}>
      <button id="send-turn-btn" class="btn-primary" style="padding: 8px 16px;" ${isNoAiMode ? 'disabled' : ''}>发送</button>
    </div>
  `;
}

function escapeHtml(text) {
  return text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/\n/g, "<br>");
}
