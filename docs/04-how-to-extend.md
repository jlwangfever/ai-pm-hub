# 04 · 扩展指南

> 想给 ai-pm-hub 加新段位、新子技能、新 reference 之前，先读本文。

## 三种扩展场景

| 场景 | 难度 | 例子 |
|------|-----|------|
| 给现有子技能加一份新 reference | 低 | 给 `product-design-writer` 加一份「权限审计」参考 |
| 新增一个独立段位 | 中 | 加「第 9 段：发布与运营」 |
| 新增一个完整子技能 | 高 | 加 `data-analytics-writer`（数据分析方法论） |

下面分别说明。

## 场景 A：给现有子技能加新 reference

1. **选段位**：在 `skills/<子技能>/references/` 看现有 reference，确认你要加的内容**不与现有重复**
2. **读金标准**：至少读 3 份同子技能的 reference，确保风格一致
3. **写 reference**：五段式结构 + 跨领域通用 + 可执行细节
4. **写索引**：在 `skills/<子技能>/SKILL.md` 的「如何按需加载框架」表加一行
5. **不更新能力地图**：reference 数量变更不影响段位定义
6. **提 PR**

工作量：约 2–4 小时（写 80–120 行 reference + 自检）

## 场景 B：新增一个独立段位

新增段位**比**加 reference 影响大很多。先评估三件事：

### 评估 1：它真的独立吗？

问自己：
- 它有**自己的输入链**吗？（输入来自哪些上游）
- 它有**自己的产出物**吗？（输出不是另一个段位的中间产物）
- 它有**自己的方法论骨架**吗？（不能用现有 reference 拼凑）

如果任一答「否」，它应该作为现有段位的一份 reference，而不是新段位。

### 评估 2：它和现有 8 段位怎么衔接？

画出新段位在流程图中的位置（前面吃谁的输出、后面给谁输入）。如果找不到上下游，它就不属于产品全流程。

### 评估 3：能不能拆成独立子技能？

段位 ≠ 子技能。一个段位可能由一个或多个子技能承载（如第 4 段产品设计已由 1 个子技能承载多份 reference）。

**推荐**：先建独立子技能，再挂到现有段位上。

### 实操步骤

1. **提 Issue 讨论**（先看 [CONTRIBUTING.md](../CONTRIBUTING.md)）
2. 写 `skills/<新子技能>/SKILL.md`
3. 写 `references/framework-overview.md` + 3–5 份 reference + 1 份 `_example-*.md`
4. 更新 `skills/ai-pm-hub/references/capability-map.md`（能力清单加一行）
5. 更新 `skills/ai-pm-hub/SKILL.md`（能力地图表 + 路由规则 + 跨能力编排）
6. 更新 `skills/ai-pm-hub/references/capability-map-data.json`（同步给谱系图）
7. 跑 `python3 tools/capability-map-gen.py` 重新生成 SVG
8. 更新 `README.md` 的 8 段全流程图与表
9. 更新 `CHANGELOG.md`
10. 提 PR

工作量：约 2–4 天

## 场景 C：新增一个完整子技能

子技能是**独立的方法论体系**。当你想把 ai-pm-hub 扩展到其他角色（如「设计师」「数据分析师」「工程师」），就需要新子技能。

### 评估

- 它有自己的**触发词**吗？（如「写代码」「做数据看板」）
- 它有自己的**产出物**吗？（如代码模块、数据报告）
- 它能被**独立调用**吗？（不依赖 ai-pm-hub 也能用）

### 实操步骤

1. **提 Issue 讨论**
2. 设计子技能的：
   - 名称、定位、一句话
   - 内部 reference 结构（建议沿用五段式）
   - 与 ai-pm-hub 的关系（独立 / 协作 / 补充）
3. 创建 `skills/<新子技能>/SKILL.md` + 5–10 份 reference
4. 在 `ai-pm-hub/SKILL.md` 路由规则表加一行
5. 更新能力地图数据与 SVG
6. 更新 README
7. 提 PR

工作量：约 1–2 周

## 命名规范

| 类型 | 命名 | 例子 |
|------|-----|------|
| 子技能目录 | `<英文名>-<角色>`，全小写、连字符 | `product-design-writer` |
| 子技能主文件 | `SKILL.md` | `ai-pm-hub/SKILL.md` |
| reference 文档 | `<编号>-<主题>.md` | `02-swot.md` |
| 框架总览 | `framework-overview.md` | — |
| 示范样例 | `_example-<领域>.md` | `_example-chemai.md` |
| 教学课件 | `courseware-<主题>.md` / `.html` | `courseware-1to3.md` |

> `_` 前缀让样例在 `ls` 中排第一，提示读者「先读这个」。

## 提交前自检

- [ ] 五段式结构完整
- [ ] `grep -E "行业词|产品名|技术栈"` 命中数 = 0
- [ ] 状态机/矩阵/降级链有可执行细节
- [ ] 及格线 4–6 条用 ☑ 开头
- [ ] 「不在范围内」声明
- [ ] `_example-*.md` 开头有「本文件是示范参考，不是模板」声明
- [ ] 行数 ≥ 70 且 ≤ 250
- [ ] 不重新定义上游决策（如果是流程中后段的文档）
- [ ] `capability-map.svg` 重新生成且无溢出

## 怎么维护「能力地图」

`docs/images/capability-map.svg` 是**自动生成的**——它从 `skills/ai-pm-hub/references/capability-map-data.json` 读取数据。

**不要手改 SVG**。改完数据后跑：

```bash
cd ~/ai-pm-hub-repo
python3 tools/capability-map-gen.py
# 检查 docs/images/capability-map.svg 视觉无溢出
```

JSON 数据结构详见 `capability-map-data.json` 本身（含 `skills` / `segments` / `teaching_assets` / `dependencies` 四个字段）。

## 提 PR 的标准流程

参见 [CONTRIBUTING.md](../CONTRIBUTING.md) 末尾的「提 PR 流程」章节。

## 进阶：把方法论沉淀成新子技能（工作流）

如果你手头有一批成品文档（如公司内部的某类规范、某行业的方法论文档），想把它们沉淀成本仓库的子技能：

1. **找金标准**：先读 `market-insight-writer` 与 `prd-style-learner` 的 SKILL.md
2. **抽样摸骨架**（只读）：用 `grep -E "^## |^# "` 提取每份文档的章节标题
3. **去行业化质检**：识别行业专属内容并按 [docs/02-anti-plagiarism.md](02-anti-plagiarism.md) 替换
4. **写 SKILL.md**：核心理念 / 一句话定位表 / 输入链 / 通用工作流 / 如何按需加载框架 / 跨领域适配规则 / 输出约定 / 注意事项
5. **写 framework-overview.md**：素材对应表 / 一句话话术表 / 输入链 / 统一写作主线 / 及格线总表 / 统一红线
6. **写每份 reference**：五段式 + 可执行细节 + 不在范围内
7. **写 _example-*.md**：示范样例（不是模板）
8. **注册到 ai-pm-hub**：路由 + 能力地图 + SVG

整个流程约 1 周（一个方法论体系），建议分多次小 PR 提交（先框架后样例）。

## 总结

| 场景 | 何时 | 工作量 |
|------|----|------|
| 加 reference | 缺某份具体方法论 | 2–4 小时 |
| 加段位 | 跨多个段位、需要独立方法论 | 2–4 天 |
| 加子技能 | 扩展到其他角色 | 1–2 周 |

总原则：**先讨论再写**。任何新段位或新子技能，先提 Issue 描述动机与设计——避免返工。
