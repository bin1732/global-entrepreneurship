<!-- sopMeta: { lastVerified: "2026-08-11", verifyCycleDays: 90, nextVerifyAt: "2026-11-09" } -->
# Context Engineering 一人公司实战指南

> 2026年，Context Engineering取代Prompt Engineering成为一人公司的核心能力

---

## 一、为什么Context Engineering对一人公司至关重要

传统创业需要组建团队来分担认知负荷。一人公司没有团队——但可以用**结构化上下文**让AI成为你的团队。

| 对比 | Prompt Engineering | Context Engineering |
|------|-------------------|-------------------|
| 核心动作 | 写一条好提示词 | 设计整个信息环境 |
| 范围 | 单次对话 | 跨会话、跨Agent、跨工具 |
| 持久性 | 一次性 | 持久化到文件系统 |
| 协作 | 单人单AI | 多Agent编排 |
| 记忆 | 无 | RAG+结构化记忆 |

---

## 二、CLAUDE.md 设计指南

CLAUDE.md是Claude Code的"长期记忆"，写入项目根目录即可生效。

### 一人公司CLAUDE.md模板

```markdown
# [你的公司名] — AI工作上下文

## 业务身份
- 公司名：XX
- 创始人：XX
- 行业：XX
- 目标市场：XX
- 核心产品：XX
- 当前阶段：[探索期/MVP期/增长期/规模化期]

## 业务目标
- 月收入目标：XX元
- 当前月收入：XX元
- 目标用户数：XX
- 当前用户数：XX

## 15层进度
| 层 | 状态 | 关键产出 |
|----|------|----------|
| 1 用户画像 | ✅/🔄/⬜ | |
| 2 市场扫描 | | |
| ... | | |
| 15 长期蓝图 | | |

## 关键决策记录
- [日期] 决策：XX → 原因：XX
- [日期] Pivot：XX → 原因：XX

## 约束与偏好
- 语言：[中文/英语/...]
- 预算上限：XX元/月
- 时间投入：XX小时/天
- 风险偏好：[保守/中等/激进]

## AI Agent分工
- 市场分析：market-analyst
- 财务建模：financial-planner
- 合规检查：compliance-advisor
- 内容获客：content-strategist
```

---

## 三、AGENTS.md 设计指南

AGENTS.md定义多Agent编排架构，放在项目根目录。

### 设计原则
1. 每个Agent有明确职责边界，避免重叠
2. Agent间通过文件系统共享上下文（非实时消息）
3. 主Skill文件是编排中枢，Agent是执行单元
4. 使用`.claude/agents/`目录存放各Agent的详细prompt

### 一人公司典型Agent架构

```
创始人（你）
  ├── Vibe CEO 仪表盘（决策层）
  │     ├── 市场数据 → market-analyst
  │     ├── 财务数据 → financial-planner
  │     └── 风险预警 → compliance-advisor
  ├── 执行层
  │     ├── 产品开发 → Claude Code / Codex
  │     ├── 内容生产 → content-strategist
  │     └── 客户服务 → 自定义Agent
  └── 知识层
        ├── RAG知识库 → 行业数据/竞品情报
        └── 结构化记忆 → state.mjs持久化
```

---

## 四、MCP Server 推荐

Model Context Protocol (MCP) Server让AI能访问外部工具和数据。

### 一人公司必备MCP Server

| MCP Server | 用途 | 适用场景 |
|------------|------|----------|
| **filesystem** | 文件读写 | 所有场景 |
| **web-search** | 网络搜索 | 市场扫描/竞品分析 |
| **postgres/sqlite** | 数据库操作 | 用户数据/财务数据 |
| **github** | 代码管理 | SaaS/工具类产品 |
| **notion** | 知识管理 | 项目管理/文档 |
| **slack** | 团队沟通 | 社群运营 |

### 按业务类型推荐

**SaaS/工具类**
- filesystem + github + postgres + web-search

**内容/媒体类**
- filesystem + web-search + notion + slack

**电商/贸易类**
- filesystem + web-search + sqlite + notion

**咨询/服务类**
- filesystem + web-search + notion + postgres

---

## 五、RAG知识管理

### 一人公司RAG架构

```
知识来源
  ├── 行业报告（PDF/Web）
  ├── 竞品数据（定期抓取）
  ├── 用户反馈（客服记录）
  ├── 法规政策（OPC/合规）
  └── 内部文档（决策记录/复盘）
       │
       ▼
  向量化存储（本地/云）
       │
       ▼
  AI检索 → 补充到当前对话上下文
```

### 知识分类体系

| 类别 | 示例 | 更新频率 | 优先级 |
|------|------|----------|--------|
| 市场情报 | 竞品动态/行业趋势 | 每周 | 高 |
| 合规政策 | 法规变化/OPC政策 | 每月 | 高 |
| 用户洞察 | 反馈/需求/痛点 | 持续 | 高 |
| 财务数据 | 收入/成本/预测 | 每月 | 中 |
| 操作文档 | 流程/模板/工具 | 按需 | 中 |
| 灵感素材 | 创意/案例/趋势 | 持续 | 低 |

---

## 六、结构化记忆模式

### 跨会话记忆设计

```yaml
# 项目状态文件 (.project-state.yaml)
version: "1.0"
last_updated: "2026-08-02"

business:
  name: "XX"
  stage: "MVP期"
  monthly_revenue: 0
  target_revenue: 10000

layers_completed:
  - 1  # 用户画像
  - 2  # 市场扫描
  - 3  # 方向推荐

pending_actions:
  - "完成MVP功能开发"
  - "启动种子用户获取"

decisions:
  - date: "2026-07-30"
    decision: "选择订阅制SaaS模式"
    reason: "可扩展性最高"
```

### state.mjs 集成

使用 `scripts/state.mjs` 管理：
- `node scripts/state.mjs init` — 初始化项目状态
- `node scripts/state.mjs commit` — 保存当前会话状态
- `node scripts/state.mjs status` — 查看项目进度

---

## 七、Context Engineering最佳实践

1. **CLAUDE.md先写业务身份**——AI需要知道"为谁做什么"
2. **每完成一层就commit状态**——跨会话连续性
3. **Agent之间通过文件通信**——比对话更可靠
4. **RAG聚焦高优先级知识**——不是所有信息都值得向量化
5. **定期清理过时上下文**——避免认知噪音
6. **用结构化格式（YAML/JSON）**——比自然语言更可靠
7. **MCP Server按需启用**——不是越多越好
