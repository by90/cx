---
name: cx-research
description: 用于模型选择研究、AI 论文综述、模型原理研究、最近六个月 AI 文献扫描、来源筛选、博客解读和带引用的综合分析。
version: 0.1.0
---

# cx 研究工作流

## 目的

当任务是研究而不是实现时使用本 skill：选择模型、理解某个模型族、比较架构、调研近期 AI 论文，或结合论文和技术博客收集专家解读。

## 来源策略

必须使用多类来源，并清楚标注来源类型：

1. 一手来源：官方文档、model card、技术报告、arXiv 论文、OpenReview 投稿、会议论文集、benchmark 仓库和源码。
2. 发现工具：Semantic Scholar、arXiv 搜索、OpenAlex、Papers with Code、Hugging Face Papers、会议页面和引用图谱。
3. 解读来源：实验室博客、工程博客、独立专家文章、技术演讲和复现实验报告。
4. 社区信号：GitHub issue、benchmark 讨论和论坛只能作为弱信号，不能单独当作证据。

## 必须执行的流程

1. 明确研究问题、决策期限、目标读者和输出格式。
2. 搜索前先写纳入和排除标准。
3. 同时搜索学术来源、官方来源和解读来源。
4. 对“最新”或“近期”AI 研究，必须使用明确日期窗口。“最近六个月”指从今天起向前推六个自然月。
5. 按 title、DOI、arXiv ID、OpenReview ID 或 Semantic Scholar Corpus ID 去重。
6. 区分 peer-reviewed paper、preprint、博客解读、benchmark 和厂商声明。
7. 把证据抽取成表格：来源、日期、发表状态、主张、方法、证据质量、限制和相关性。
8. 必须综合分析，不能只罗列。按研究方向、共识、冲突、成熟度和实现后果分组。
9. 每个非显然主张都必须附链接引用。
10. 明确哪些内容未知、过时、有争议或可能很快变化。

## 模型选择研究

选择模型时比较：

- 任务适配度和模态需求。
- 相关 benchmark 或内部 eval 上的质量证据。
- 上下文长度、工具调用、结构化输出、延迟、吞吐、可靠性和成本。
- 部署约束：API 可用性、本地推理、隐私、许可、区域和硬件。
- 失败模式：幻觉、推理弱点、多语言缺口、代码能力缺口、安全限制和 eval 污染。
- 迁移风险和 fallback 方案。

## 模型原理研究

研究模型原理时，优先使用原始论文和技术报告。说明架构、训练目标、数据假设、推理行为、扩展限制和已知缺陷。不要把营销声明当作机制证据。

## 输出格式

```text
Question:
Search window:
Sources searched:
Inclusion/exclusion criteria:

Findings:
1. Claim
   Evidence:
   Limits:
   Practical consequence:

Source table:
| Source | Date | Type | Claim | Evidence quality | Link |

Recommendation:
Open questions:
```
