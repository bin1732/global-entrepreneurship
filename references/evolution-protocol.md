# 反幻觉与自进化协议

## 一、反幻觉机制

### 自检触发器

以下高风险场景必须触发自检：

| 场景 | 触发条件 | 自检内容 |
|------|----------|----------|
| 市场数据引用 | 引用具体市场规模/增长率数字 | 数据来源是否为references/或web_search？如无来源则标注"估算" |
| 合规建议 | 给出目标国法规/税率/政策 | 是否基于references/industry-knowledge.md？是否建议用户咨询专业律师？ |
| 财务预测 | 给出收入/成本/利润数字 | 是否调用financial_calculator.py计算？还是LLM估算？必须标注 |
| 政策匹配 | 引用中国OPC扶持政策 | 是否基于references/opc-policy.md？政策时效是否已核实？ |
| 国家/地区建议 | 推荐特定国家创业 | 是否有references/world-markets.md数据支撑？ |

### 幻觉纠正协议

当检测到可能的幻觉时：

1. **立即标注**：在输出中添加 `⚠️ 此数据为AI估算，未经核实，建议通过web_search或专业渠道确认`
2. **补充来源**：如有references/中的数据，引用具体文件
3. **建议核实**：引导用户使用web_search或咨询专业人士
4. **记录事件**：在交互末尾记录本次幻觉纠正事件（不影响用户可见输出）

### 禁止行为

- ❌ 编造不存在的政策文件/法规条款
- ❌ 给出未经计算的具体财务数字却不标注"估算"
- ❌ 声称某国有某项创业补贴但无references/支撑
- ❌ 引用不存在的市场数据来源

## 二、自进化机制

### 知识更新

- 用户反馈"这个信息过时了" → 标记对应reference文件需要更新
- web_search获得新数据 → 在输出中引用，并建议更新references/
- 用户分享目标国实际经验 → 记录为"用户实测数据"，建议纳入references/

### 进化记录

每次交互后，如有以下情况，记录到 `.project-state/evolution-log.jsonl`：

```json
{
  "timestamp": "ISO时间",
  "type": "data_update_needed|new_knowledge|user_feedback",
  "target_file": "references/xxx.md",
  "description": "描述",
  "action": "建议更新/建议新增/已记录"
}
```

**注意**：自进化是被动记录机制，不会自动修改references/文件。所有更新建议由用户确认后执行。

## 三、SOP时效巡检

### 元数据规范

所有reference文件应在头部包含时效元数据：

```markdown
<!-- sopMeta: { lastVerified: "2026-08-11", verifyCycleDays: 90, nextVerifyAt: "2026-11-09" } -->
```

### 状态定义

| 状态 | 条件 | 处理 |
|------|------|------|
| ok | 距最后核实<核定周期的80% | 正常使用 |
| due-soon | 距最后核实80-100%周期 | 标注"即将到期，建议核实" |
| overdue | 超过核定周期 | 标注"已过期，数据可能不准" |
| missing-meta | 无时效元数据 | 标注"未跟踪时效" |
| malformed-date | 日期格式错误 | 标注"元数据格式错误" |

### 巡检触发

- 用户首次触发skill时自动巡检所有references/
- 用户明确要求"检查数据时效"时
- 每次交互中引用reference文件前检查该文件时效状态
