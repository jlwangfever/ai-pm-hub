# 05 · 能力地图详细

> 本文档是 `docs/images/capability-map.svg` 的文字版——SVG 适合快速浏览，本文适合查询细节。

## 1. 5 个子技能

| 子技能 | 段位 | 颜色 | reference 数量 |
|--------|-----|-----|--------------|
| `market-insight-writer` | 1 | 🟣 紫 | 8 |
| `user-value-definer` | 2 | 🔵 蓝 | 7 |
| `validation-business-model` | 3 | 🟦 青 | 10 |
| `product-design-writer` | 4, 6, 7, 8 | 🟢 绿 | 26 |
| `prd-style-learner` | 5 | 🔴 红 | 3 |

## 2. 8 段位详表

### 段 1：市场洞察（`market-insight-writer`）

- **覆盖文档**：PESTLE 宏观环境 · 市场规模 TAM/SAM/SOM · SWOT · 竞品分析 · 产品愿景
- **段内顺序**：PESTLE → 市场规模 → SWOT ⇄ 竞品 → 产品愿景
- **产出物**：5 份框架文档 + 1 套示例 + 4 段提示词
- **reference 文件**：
  - `framework-overview.md` — 总览
  - `01-pestle.md` — 宏观环境
  - `02-swot.md` — SWOT
  - `03-market-size.md` — 市场规模
  - `04-competitor.md` — 竞品分析
  - `05-vision.md` — 产品愿景
  - `_example-chemai.md` — ChemAI 项目样例
  - `prompts-swot.md` — SWOT 配套 4 段提示词

### 段 2：用户与价值定义（`user-value-definer`）

- **覆盖文档**：用户画像 Persona · 价值主张 · 理想客户画像 ICP · 定位策略 · 滩头阵地
- **段内顺序**：用户画像 → 价值主张 → ICP → 定位 → 滩头
- **产出物**：5 份框架文档 + 1 套示例
- **reference 文件**：
  - `framework-overview.md`
  - `06-persona.md`
  - `07-value-proposition.md`
  - `08-icp.md`
  - `09-positioning.md`
  - `10-beachhead.md`
  - `_example-chemai.md`

### 段 3：验证与商业模式（`validation-business-model`）

- **覆盖文档**：假设识别与验证 · 精益画布 · 北极星指标 · 机会解决方案树 · 干系人地图 · Pre-Mortem · GTM 策略 · 功能优先级
- **段内顺序**：
  - 验证线：假设 → OST → Pre-Mortem
  - 商业线：精益画布 → 北极星 → GTM → 优先级
  - 干系人贯穿
- **产出物**：8 份框架文档 + 1 套示例
- **reference 文件**：
  - `framework-overview.md`
  - `11-assumption-validation.md` — 假设识别与验证
  - `12-lean-canvas.md` — 精益画布
  - `13-north-star-metric.md` — 北极星指标
  - `14-opportunity-solution-tree.md` — 机会解决方案树
  - `15-stakeholder-map.md` — 干系人地图
  - `16-pre-mortem.md` — Pre-Mortem 事前验尸
  - `17-gtm.md` — GTM 策略
  - `18-feature-prioritization.md` — 功能优先级
  - `_example-chemai.md`

### 段 4：产品设计（`product-design-writer`，1/4）

- **覆盖文档**：信息架构 · 交互流程 · 权限模型 · 业务系统×6（批改/出题/审核/诊断/自适应/复习）· Agent 系统 · 分析预警 · 评测体系 · 外围端 · 数据/API/设计系统/部署/选型 · 前端规格 · 流式渲染 · 知识图谱 · 系统架构
- **段内顺序**：信息架构 → 流程权限 → 业务系统 → Agent → 数据分析 → 支撑系统 → 技术基础 → 前端整合
- **产出物**：22 份框架 + 2 套示例
- **reference 文件**（前 10 个）：
  - `framework-overview.md`
  - `20-information-architecture.md` — 信息架构
  - `21-interaction-flow.md` — 交互流程
  - `22-permission-model.md` — 权限模型
  - `23-ocr-grading-pipeline.md` — 识别批改类管线
  - `24-question-bank-generation.md` — 出题与题库
  - `25-safety-review-engine.md` — 安全审核引擎
  - `26-diagnosis-barrier.md` — 诊断与障碍分类
  - `27-adaptive-practice.md` — 自适应练习
  - `28-spaced-repetition.md` — 间隔复习
- **reference 文件**（中 10 个）：
  - `29-agent-system.md` — Agent 对话系统
  - `30-analytics-warning.md` — 学情分析与预警
  - `31-evaluation-system.md` — 评测体系
  - `32-parent-notification.md` — 外围角色端与通知
  - `33-37-tech-foundation.md` — 技术基础（数据模型/API/设计系统/桌面/选型）
  - `38-frontend-spec.md` — 前端页面集中规格
  - `39-sse-rendering.md` — 流式渲染
  - `40-graphrag-knowledge.md` — 检索增强知识系统
  - `41-prototype-validation.md` — 原型验证
  - `42-system-architecture.md` — 系统架构图
- **reference 文件**（后 4 个）：
  - `44-prototype-spec.md` — 原型说明文档
  - `45-ui-vibe-coding.md` — UI 实现 / Vibe Coding
  - `_example-chemai.md`
  - `_example-designmd-chemai.md`

### 段 5：PRD 风格学习与写作（`prd-style-learner`）

- **覆盖文档**：学习我的 PRD 风格档案 · 按我的风格写新领域 PRD · 三种结构变体（A 标准 / B 极简 / C Agent 全生命周期）
- **段内顺序**：learn 提取风格 → write 按风格写
- **产出物**：1 份风格档案 + 模板 + 解析脚本
- **reference 文件**：
  - `profile/prd_style_profile.md` — 风格档案
  - `references/style_profile_template.md` — 风格档案模板
  - `scripts/parse_docx.py` + `parse_pdf.py` — 解析脚本

### 段 6：DESIGN.md 设计规范落地（`product-design-writer` / 43 号）

- **覆盖文档**：AI 编码代理自动读取的设计规范 · YAML token + 复用矩阵 + MUST/NEVER 规则 · C 编号约束表 + G 编号缺口表与回填
- **段内顺序**：提取设计参数 → 抽象组件模式 → 翻译约束规则 → 整体约束与缺口表
- **产出物**：1 份框架 + 1 套 ChemAI 真实成品样例
- **reference 文件**：
  - `43-design-md.md`
  - `_example-designmd-chemai.md`

### 段 7：原型设计（`product-design-writer` / 41+44 号）

- **覆盖文档**：七维度方案 · Review 三关 · 原型生成（HTML / figma / 墨刀 / stitch）· 需求标注追溯码 · 原型说明文档
- **段内顺序**：先画施工图，再盖楼：方案 → Review → 生成 → 标注 → 交开发
- **产出物**：2 份框架（七维度 + 说明文档）
- **reference 文件**：
  - `41-prototype-validation.md`
  - `44-prototype-spec.md`

### 段 8：UI 实现 / Vibe Coding（`product-design-writer` / 45 号）

- **覆盖文档**：五步法（问框架 → 选组件库 → 对组件名 → 写代码 → 要迭代）· 自做/公司两场景话术 · 框架-组件库对照表
- **段内顺序**：问框架 → 选组件库 → 对组件名 → 写代码 → 要迭代
- **产出物**：1 份框架（五步法 + 对照表）
- **reference 文件**：
  - `45-ui-vibe-coding.md`

## 3. 3 份教学课件

| 课件 | 覆盖段位 | 路径 |
|------|---------|------|
| 03-直播课件《第一节课 · 用 WorkBuddy 写出 ChemAI 18 份文档》 | 1→3 段串讲 | `skills/ai-pm-hub/references/teaching/courseware-1to3.html` + `.md`（索引） |
| ChemAI 产品设计七层（v41，46 页） | 4+6+7 段 | `skills/product-design-writer/references/teaching/courseware-design.html` + `.md`（索引） |
| SWOT 配套提示词（4 段） | 第 1 段 02-SWOT 配套 | `skills/market-insight-writer/references/prompts-swot.md` |

## 4. 10 条段间承接关系

| 从 | 到 | 承接内容 |
|----|----|---------|
| 1 市场洞察 | 2 用户与价值 | 市场规模 + 竞品 → ICP/滩头边界 |
| 2 用户与价值 | 3 验证与商业 | 用户痛点 → 待验证假设；价值主张 → 画布/定价 |
| 3 验证与商业 | 4 产品设计 | 功能优先级 → 落地顺序；NSM → 评测埋点 |
| 4 产品设计 | 5 PRD | 设计模块 + 状态 → PRD 功能详述；愿景 → 背景/目标 |
| 4 产品设计 | 6 DESIGN.md | 35 设计系统 + 38 前端规格 → 压缩提炼（零发明） |
| 4 产品设计 + 5 PRD | 7 原型设计 | 设计文档 + PRD → 七维度方案 |
| 6 DESIGN.md + 7 原型 | 8 UI 实现 | 视觉约束 + 交互基准 → 组件选型 |
| 6 DESIGN.md → 7 原型 | (内部) | 视觉约束支撑原型说明文档 |
| 5 PRD → 7 原型 | (内部) | 需求编号 → 标注追溯码 |
| 7 原型 → 8 UI | (内部) | 交互与状态 → 组件实现基准 |

## 5. 总体数据

- **5 子技能** + **8 段位** + **54 reference** + **3 教学课件** = 70 个能力单元
- **0 项待扩充**
- **10 条段间承接**显式沉淀
- 全部 8 段位已启用 ✅

## 6. 能力地图可视化同步

`docs/images/capability-map.svg` 由 `tools/capability-map-gen.py` 从 `skills/ai-pm-hub/references/capability-map-data.json` 生成。

**不要手改 SVG**。改完 JSON 后跑：

```bash
python3 tools/capability-map-gen.py
```

详见 [docs/04-how-to-extend.md](04-how-to-extend.md) 的「怎么维护能力地图」一节。
