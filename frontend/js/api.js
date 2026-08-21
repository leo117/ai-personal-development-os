const API_BASE = "/api/v1";

export const api = {
  // 获取任务列表
  async getTasks() {
    try {
      const res = await fetch(`${API_BASE}/tasks/`);
      return await res.json();
    } catch (e) {
      console.error("Failed to fetch tasks", e);
      return [];
    }
  },

  // 获取技能图谱与 FSRS 复习队列
  async getCompetencyGraph(userId = "usr_demo_01") {
    try {
      const res = await fetch(`${API_BASE}/competencies/graph?user_id=${userId}`);
      return await res.json();
    } catch (e) {
      console.error("Failed to fetch graph", e);
      return { nodes: [], retention_queue: [] };
    }
  },

  // 提交交互对话回合
  async sendTurn(payload) {
    const res = await fetch(`${API_BASE}/sessions/turn`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  // 提交任务交付物
  async submitTask(payload) {
    const res = await fetch(`${API_BASE}/tasks/submit`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return await res.json();
  },

  // 获取科研指标
  async getResearchMetrics(userId = "usr_demo_01") {
    try {
      const res = await fetch(`${API_BASE}/research/metrics?user_id=${userId}`);
      return await res.json();
    } catch (e) {
      console.error("Failed to fetch research metrics", e);
      return null;
    }
  },

  // AI 智能出题生成任务草案
  async generateAiTask(topic, bloomLevel = "ANALYZE", difficultyScore = 70.0) {
    const res = await fetch(`${API_BASE}/tasks/ai-generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        topic: topic,
        bloom_level: bloomLevel,
        difficulty_score: difficultyScore
      })
    });
    return await res.json();
  },

  // 创建并持久化新任务
  async createTask(payload) {
    const res = await fetch(`${API_BASE}/tasks/`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    return await res.json();
  }
};
