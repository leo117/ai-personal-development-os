# AI Personal Development OS (AI 个人成长与能力发展系统)

> **核心哲学**：AI 不是替你完成目标，而是帮助你成为能够完成目标的人。  
> **北极星指标**：独立能力增长 (Independent Capability Growth) 与去 AI 依赖 (Anti-AI-Dependency)。

---

## 目录
1. [⚡ 运行环境与一键启动 (Quick Start)](#1-运行环境与一键启动)
2. [🤖 AI 模型与 API 接口配置 (LLM Config)](#2-ai-模型与-api-接口配置)
3. [🖥️ Web 双工作区核心功能操作指南](#3-web-双工作区核心功能操作指南)
4. [🔌 API 接口与开发者调用方法](#4-api-接口与开发者调用方法)
5. [🧪 自动化测试与质量校验](#5-自动化测试与质量校验)
6. [🎯 领域图谱与任务定制方法](#6-领域图谱与任务定制方法)
7. [📚 文档体系与工程规范索引](#7-文档体系与工程规范索引)
8. [🏛️ 系统核心架构概览](#8-系统核心架构概览)

---

## 1. 运行环境与一键启动

本项目已内置独立的 **Python 虚拟环境 (`.venv`)**，所有生产与测试依赖均已安装就绪。

### 🚀 启动方式 (任选其一)

- **方式一：Windows 批处理脚本 (推荐)**  
  直接双击运行根目录下的 `start.bat` 或在终端执行：
  ```cmd
  start.bat
  ```

- **方式二：PowerShell 脚本**  
  在 PowerShell 终端执行：
  ```powershell
  .\start.ps1
  ```

- **方式三：虚拟环境命令行**  
  ```powershell
  # 激活虚拟环境 (可选)
  .\.venv\Scripts\Activate.ps1
  
  # 启动服务
  python run_server.py
  ```

### 🌐 服务访问入口
- **🖥️ 生产级双工作区前端**：[http://localhost:8000/](http://localhost:8000/)
- **📖 OpenAPI / Swagger 交互式文档**：[http://localhost:8000/docs](http://localhost:8000/docs)
- **📑 ReDoc 规范文档**：[http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 2. AI 模型与 API 接口配置

系统采用标准 `.env` 环境变量配置大模型，**兼容所有 OpenAI 协议接口**。

### ⚙️ 配置文件位置：根目录 [`.env`](./.env)

打开根目录下的 `.env` 文件，填入对应服务商参数即可：

#### ① 配置 DeepSeek (官方 API)
```ini
LLM_API_KEY=sk-your-deepseek-api-key
LLM_API_BASE=https://api.deepseek.com/v1
LLM_MODEL_NAME=deepseek-chat
```

#### ② 配置 OpenAI (官方 API)
```ini
LLM_API_KEY=sk-your-openai-api-key
LLM_API_BASE=https://api.openai.com/v1
LLM_MODEL_NAME=gpt-4o
```

#### ③ 配置 硅基流动 (SiliconFlow / 国内高可用代理)
```ini
LLM_API_KEY=sk-your-siliconflow-api-key
LLM_API_BASE=https://api.siliconflow.cn/v1
LLM_MODEL_NAME=deepseek-ai/DeepSeek-V3
```

#### ④ 配置 本地 Ollama (完全离线与本地部署)
```ini
LLM_API_KEY=ollama
LLM_API_BASE=http://localhost:11434/v1
LLM_MODEL_NAME=qwen2.5:7b
```

> **💡 智能兜底机制**：若 `LLM_API_KEY` 留空，系统不会报错，而是自动启用内置的教育策略模板引擎生成受控响应。

---

## 3. Web 双工作区核心功能操作指南

打开浏览器访问 [http://localhost:8000/](http://localhost:8000/) 即可进入现代双工作区：

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 顶栏：北极星指标 ICG (+3.2/周) | AI 依赖指数 ADI (25%) | [🕸️ 技能图谱与FSRS] | [📊 科研看板]  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 任务标签栏：[Week 1: 客服场景LLM]  [Week 2: RAG架构设计]  [Week 3: 自动化Eval]  [Week 4: 多Agent] │
├──────────────────────────────────────────┬─────────────────────────────────────────────┤
│ 🛠️ 左侧：真实生产画布 (Production Canvas)  │ 🧠 右侧：AI 动态支架陪练控制台 (Coach Console)│
│                                          │                                             │
│ 1. 任务背景与 Evidence Contract 评测标准 │ 1. ⚡ Assistance Budget 能量条 (100点动态扣减)│
│ 2. Markdown 方案/PRD/代码编辑器          │ 2. 支架强度选择：Q1反问 / Q2提示 / Q3类比 / Q4骨架│
│ 3. [🔒 进入无 AI 独立评估模式] 按钮      │ 3. 苏格拉底式启发对话流 (含 Guardrail 拦截标签)│
│ 4. [🚀 提交交付物并申请 Authentic 评估]  │ 4. 问题输入框与快速提问                     │
└──────────────────────────────────────────┴─────────────────────────────────────────────┘
```

### 1. 真实方案撰写与交付 (左侧画布)
- **切换任务**：点击顶部的 Week 1 ~ Week 4 标签，自动载入对应的真实业务背景与评分规准（Rubrics）。
- **撰写方案**：在中间的 Markdown 编辑器中撰写 PRD、架构设计或代码方案。
- **提交评估**：点击 **“🚀 提交交付物并申请 Authentic 评估”**，系统将自动调用 Assessment Agent 进行多维度客观打分（技术严密性、权衡分析、掌握度跃迁）。

### 2. 动态支架陪练与能量管理 (右侧控制台)
- **能量条机制**：每个任务初始赋予 **100 点支架能量**。
- **阶梯提问**：
  - `Q1: 反问启发 (10点)`：AI 提出关键矛盾与反思点，引导自我探索。
  - `Q2: 策略提示 (25点)`：AI 给出解题策略方向（如分阶段检索与重排）。
  - `Q3: 场景类比 (50点)`：AI 给出跨领域的直观类比案例。
  - `Q4: 骨架填空 (80点)`：AI 给出带 `TODO` 槽位的代码/文档框架。
- **拦截保护 (Scaffolding Guard)**：若 AI 试图直接给出完整答案或代码，拦截器会自动折叠代码块并提示先自行尝试。
- **能量耗尽熔断**：当能量降为 0 时，AI 强制进入冷凝状态，鼓励独立完成。

### 3. 无 AI 独立测试模式 (No-AI Assessment)
- 点击左下角 **“🔒 进入无 AI 独立评估模式”**，系统会切断右侧 AI 对话通道。
- 在此模式下提交的高质量成果将作为 **“独立能力确证（Independent Evidence）”** 记录，大幅降低您的 AI 依赖度指数。

### 4. 技能图谱与 FSRS 记忆复习 (顶部弹窗)
- 点击顶栏 **“🕸️ 技能图谱与 FSRS”**：
  - 查看各项技能的 8 态掌握度（`UNDERSTOOD`, `PRACTICED`, `INDEPENDENT` 等）。
  - 查看稳定性 $S$（天）与当前可提取性 $R$。
  - 当可提取性 $R < 75\%$ 时，红框预警提示触发 **FSRS 延迟微挑战**。

### 5. 科研指标看板 (顶部弹窗)
- 点击顶栏 **“📊 科研与去依赖看板”**：
  - 查看 **AI 依赖指数 (ADI)**：反映独立解决与 AI 辅助表现的差距（越低越优）。
  - 查看 **独立能力增长率 (ICG)** 与 **支架转化效率 (SCE)**。

---

## 4. API 接口与开发者调用方法

### 核心 REST API 示例

#### ① 交互对话回合 (`POST /api/v1/sessions/turn`)
```bash
curl -X POST "http://localhost:8000/api/v1/sessions/turn" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "usr_demo_01",
       "session_id": "sess_01",
       "competency_id": "ai_pm.rag_architecture",
       "task_id": "task_ai_pm_rag_architecture",
       "user_input": "多路召回后如何去除重复项并保证低延迟？",
       "requested_level": 2,
       "current_budget": 100,
       "consecutive_failures": 0
     }'
```

#### ② 提交真实交付物 (`POST /api/v1/tasks/submit`)
```bash
curl -X POST "http://localhost:8000/api/v1/tasks/submit" \
     -H "Content-Type: application/json" \
     -d '{
       "user_id": "usr_demo_01",
       "task_id": "task_ai_pm_rag_architecture",
       "deliverable_content": "## 1. 检索架构方案...\n## 2. 权衡分析...",
       "is_no_ai_mode": true,
       "budget_spent": 25
     }'
```

#### ③ 获取技能图谱与 FSRS 队列 (`GET /api/v1/competencies/graph`)
```bash
curl "http://localhost:8000/api/v1/competencies/graph?user_id=usr_demo_01"
```

#### ④ 获取科研去依赖指标 (`GET /api/v1/research/metrics`)
```bash
curl "http://localhost:8000/api/v1/research/metrics?user_id=usr_demo_01"
```

---

## 5. 自动化测试与质量校验

系统自带覆盖引擎、算法、拦截器、状态机与接口的 **16 项全量自动化测试**：

```powershell
# 使用虚拟环境的 pytest 执行测试 (推荐)
.\.venv\Scripts\pytest.exe backend/tests/ -v

# 或使用标准 unittest 执行测试
.\.venv\Scripts\python.exe -m unittest discover -s backend/tests -p "test_*.py"
```

---

## 6. 领域图谱与任务定制方法

如果您想拓展其他职业（例如 **AI 算法工程师**、**AI 全栈开发** 或 **AI 运营**）：

1. 打开 [`backend/app/seeds/ai_pm_curriculum.json`](./backend/app/seeds/ai_pm_curriculum.json)。
2. 按照以下格式新增或修改技能节点与实战任务：
   ```json
   {
     "competency_id": "ai_dev.agent_tools",
     "title": "自定义工具与 MCP 协议集成",
     "description": "掌握 Model Context Protocol (MCP) 与 Function Calling 架构",
     "bloom_level": "CREATE",
     "difficulty_rating": 80.0,
     "task": {
       "title": "为 Agent 构建高可用天气与搜索 MCP Server",
       "problem_statement": "编写并发布符合 MCP 规范的标准服务器...",
       "rubrics": "必须包含：1. 错误熔断；2. 类型安全 Schema；3. 单元测试。"
     }
   }
   ```
3. 重新执行数据库种子填充：
   ```powershell
   .\.venv\Scripts\python.exe -c "import sys; sys.path.insert(0, 'backend'); from app.db.init_db import seed_database; seed_database()"
   ```

---

## 7. 文档体系与工程规范索引

| 文档名称 | 格式 | 说明与定位 |
| :--- | :---: | :--- |
| [AIPersonalDevelopmentOS.md](./AIPersonalDevelopmentOS.md) | Markdown | **产品与科研蓝图 v1.0**：定义核心哲学、Scaffolding 支架理论、8 态能力模型与 6 大科研问题 (RQ)。 |
| [AI_Personal_Development_OS_Complete_Engineering_Spec.md](./AI_Personal_Development_OS_Complete_Engineering_Spec.md) | Markdown | **完整技术设计与工程实现规范 v3.0**：生产级 PostgreSQL DDL、FSRS 遗忘调度、动机救援、LangGraph 状态机、Docker 沙箱评测与 AI PM 12 周参考实现。 |
| [AI_Personal_Development_OS_Complete_Engineering_Spec.pdf](./AI_Personal_Development_OS_Complete_Engineering_Spec.pdf) | PDF | **高清排版工程规格说明书**：适合团队评审、技术交底与架构归档。 |
| [AI_Personal_Development_OS_System_Design_and_Implementation_Spec.md](./AI_Personal_Development_OS_System_Design_and_Implementation_Spec.md) | Markdown | **体系完备性综合评估报告与终审结论 v2.0**：全维度 10 大指标审计与就绪判定。 |
| [AI_Personal_Development_OS_System_Design_and_Implementation_Spec.pdf](./AI_Personal_Development_OS_System_Design_and_Implementation_Spec.pdf) | PDF | **高清排版综合评估报告**：归档与评审版本。 |

---

## 8. 系统核心架构概览

```
                        ┌────────────────────────────────────────────────────────────┐
                        │                 AI Personal Development OS                 │
                        └─────────────────────────────┬──────────────────────────────┘
                                                      │
         ┌─────────────────────┬──────────────────────┼─────────────────────┬─────────────────────┐
         ▼                     ▼                      ▼                     ▼                     ▼
  1. 学习者模型 (Learner)  2. 策略引擎 (Policy)  3. 多智能体编排 (LangGraph) 4. 真实评估 (Assessment) 5. 世界模型 (World Model)
  - 动态画像与安全档案    - Assistance Budget   - 7 大 Agent 角色       - Docker 隔离执行沙箱   - ArXiv/GitHub 信号抓取
  - 8 态技能状态机       - 失败归因决策树      - Scaffolding Guard    - Evidence 证据链契约   - 图谱 Diff 补丁建议
  - FSRS 真实任务衰减    - 修正 Elo 动态难度   - 拦截代码阻断机制     - No-AI 闭卷评估与 ADI  - 用户手动审批合并
```

---

## 📄 许可证

本项目遵循 [GPL-3.0 许可证](./LICENSE)。
