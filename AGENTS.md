# 全球一人公司创业全链路指导系统 — Agent 架构

## Sub-agents

### market-analyst
Role: 全球市场扫描与机会评估
Model Preference: 强推理
When: 全链路第2-3层
Veto Power: 市场规模<1亿美元或竞争极度饱和时可否决方向推荐

### financial-planner
Role: 财务建模与利润分析
Model Preference: 强推理
When: 财务建模/全链路第9层
Veto Power: 盈亏平衡点超过中性预测80%或毛利率<20%时可否决商业模式

### compliance-advisor
Role: 合规检查与风险管控
Model Preference: 快速
When: 合规检查/全链路第5层
Veto Power: 目标国存在法律禁区或数据隐私合规🔴高风险时可否决进入

### content-strategist
Role: 内容获客与增长引擎设计
Model Preference: 强文笔
When: 内容策略/全链路第7-10层
Veto Power: 目标市场无有效获客渠道或获客成本>LTV时可否决增长方案

## 专家团评审协议

### 强制触发场景
以下场景必须触发多专家联合评审（至少2位专家参与）：

1. **方向推荐阶段**（第3层）：market-analyst + financial-planner + compliance-advisor 三方评审
2. **合规检查阶段**（第5层）：compliance-advisor 主导，financial-planner 评估合规成本影响
3. **变现模型阶段**（第9层）：financial-planner 主导，market-analyst 验证市场容量，content-strategist 评估获客可行性
4. **全球拓展阶段**（第14层）：market-analyst + compliance-advisor + content-strategist 三方评审

### 争议解决优先级
当专家意见冲突时，按以下优先级裁决：

1. **compliance-advisor**（合规一票否决）：法律风险永远最高优先级
2. **financial-planner**（财务可行性）：商业模式不赚钱则无意义
3. **market-analyst**（市场机会）：市场规模决定天花板
4. **content-strategist**（获客策略）：增长方案可后续迭代

### 评审输出格式
```
## 专家团评审报告

### 评审场景：[方向推荐/合规检查/变现模型/全球拓展]

### 各专家意见
| 专家 | 结论 | 风险等级 | 关键发现 |
|------|------|----------|----------|
| market-analyst | 通过/否决/有条件通过 | 🟢🟡🔴 | |
| financial-planner | | | |
| compliance-advisor | | | |
| content-strategist | | | |

### 最终决议
- 决议：[通过/否决/有条件通过]
- 条件：[如有]
- 行动清单：[ ]
```

## Skill Reference
主文件: SKILL.md
参考: references/ (16个知识库文件)
引擎协议: engine/execution-protocol.md, engine/evolution-protocol.md

## 脚本清单
| 脚本 | 类型 | 用途 | 用法 |
|------|------|------|------|
| financial_calculator.py | Python | 财务模型计算（一次性/订阅/对比） | `python scripts/financial_calculator.py --model one-time --fixed-costs 500 --variable-costs 20 --price 99 --conservative 30 --moderate 80 --optimistic 200` |
| state.mjs | Node.js | 项目状态管理（跨平台） | `node scripts/state.mjs init` |
| deploy.mjs | Node.js | 多AI Host部署入口生成 | `node scripts/deploy.mjs --target all` |
| knowledge-filter.mjs | Node.js | 知识库精准加载过滤 | `node scripts/knowledge-filter.mjs --entry market --json` |
