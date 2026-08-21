export function renderNewTaskModal() {
  return `
    <div class="modal-header">
      <h3 style="font-size: 16px; font-weight: 700; color: #fff; display: flex; align-items: center; gap: 8px;">
        <span>✨</span>
        <span>创建新挑战 / AI 智能自适应出题</span>
      </h3>
      <button class="modal-close" id="close-new-task-modal">&times;</button>
    </div>

    <!-- Mode Selector Tabs -->
    <div class="task-mode-tabs">
      <button id="mode-tab-ai" class="task-mode-btn active">✨ AI 智能自适应生成</button>
      <button id="mode-tab-manual" class="task-mode-btn">✍️ 手动自定义配置</button>
    </div>

    <!-- AI Generator Section -->
    <div id="ai-generator-section" class="form-section">
      <div style="font-size: 12px; color: #94a3b8; margin-bottom: 6px;">
        💡 <strong>AI 导师自适应出题：</strong>输入你想攻克的工程痛点、技术方向或弱项，AI 将为你自动生成符合工业界真实评测（Authentic Assessment）的挑战与 Rubrics 标准。
      </div>
      
      <div style="display: flex; gap: 8px; margin-bottom: 8px;">
        <input type="text" id="ai-topic-input" class="form-input" placeholder="例如：LangGraph 状态机死锁防御、千万级 Token 降本缓存、多模态 RAG...">
        <button id="ai-generate-trigger-btn" class="btn-primary" style="white-space: nowrap; padding: 8px 16px;">
          🪄 一键生成
        </button>
      </div>

      <!-- Quick Preset Tags -->
      <div class="preset-tag-row">
        <span style="font-size: 11px; color: #64748b;">推荐预设:</span>
        <button class="preset-tag-btn" data-topic="LangGraph 复杂多智能体状态机与死锁恢复">🤖 LangGraph 状态机</button>
        <button class="preset-tag-btn" data-topic="千万级高并发下 LLM 语义缓存与大小模型分流降本">💰 千万级 LLM 降本</button>
        <button class="preset-tag-btn" data-topic="多模态图表解析与长文档 Cross-Encoder 混合 RAG">📄 多模态混合 RAG</button>
        <button class="preset-tag-btn" data-topic="Agent 长期情景记忆 (Episodic Memory) 与 SQLite 状态持久化">🧠 Agent 长期记忆</button>
      </div>
    </div>

    <!-- Challenge Edit / Preview Form -->
    <div class="task-form-container">
      <div class="form-row-2">
        <div class="form-group">
          <label class="form-label">挑战标题 (Title)</label>
          <input type="text" id="new-task-title" class="form-input" placeholder="例如：千万级日调用量场景下的 LLM 降本架构设计">
        </div>
        <div class="form-group">
          <label class="form-label">难度与认知层级 (Bloom Level)</label>
          <div style="display: flex; gap: 6px;">
            <select id="new-task-bloom" class="form-select" style="flex: 1;">
              <option value="UNDERSTAND">UNDERSTAND (理解)</option>
              <option value="APPLY">APPLY (应用)</option>
              <option value="ANALYZE" selected>ANALYZE (分析)</option>
              <option value="EVALUATE">EVALUATE (评估)</option>
              <option value="CREATE">CREATE (创造)</option>
            </select>
            <input type="number" id="new-task-difficulty" class="form-input" style="width: 70px;" min="10" max="100" value="75" title="难度分 (10-100)">
          </div>
        </div>
      </div>

      <div class="form-group">
        <label class="form-label">关联知识点 / 技能名称 (Competency Title)</label>
        <input type="text" id="new-task-comp-title" class="form-input" placeholder="例如：LLM 成本优化与语义缓存">
      </div>

      <div class="form-group">
        <label class="form-label">真实业务痛点与问题陈述 (Problem Statement)</label>
        <textarea id="new-task-problem" class="form-textarea" rows="3" placeholder="描述具体业务场景、工程限制条件以及需要学员交付的技术架构方案或 PRD..."></textarea>
      </div>

      <div class="form-group">
        <label class="form-label">📋 证据契约评测标准 (Rubrics Criteria)</label>
        <textarea id="new-task-rubrics" class="form-textarea" rows="2" placeholder="必须包含的硬性指标，例如：1. 缓存淘汰策略；2. 准确率对比测试；3. 延迟与降级预案。"></textarea>
      </div>
    </div>

    <div class="modal-footer" style="display: flex; justify-content: flex-end; gap: 10px; margin-top: 16px;">
      <button id="cancel-new-task-btn" class="btn-header">取消</button>
      <button id="submit-create-task-btn" class="btn-primary">
        🚀 立即发布并加入工作台
      </button>
    </div>
  `;
}
