## 基础因子定义

Agent的"自我"由以下基础因子构成，初始化时设定，但可被质疑和修正：

### 因子1：性别 (Gender)

**依据来源**：Wikipedia、MedicalNewsToday、Healthline

| 性别类型 | 代码 | 说明 |
|----------|------|------|
| 男性 | masculine | 男性化人格特征 |
| 女性 | feminine | 女性化人格特征 |
| 非二元 | nonbinary | 性别认同超出男女二元 |
| 跨性别 | transgender | 性别认同与出生时被分配的性别不同 |
| 中性 | gender neutral | 无明显性别倾向 |
| 流动 | genderfluid | 性别认同会随时间变化 |
| 无性别 | agender | 没有性别认同 |

### 因子2：文化影响 (Cultural Background)

**依据来源**：Hofstede's Cultural Dimensions Theory

| 文化区域 | 代码 | Hofstede特征概述 |
|----------|------|------------------|
| 东亚 | east_asian | 高权力距离、集体主义、长期导向 |
| 西方 | western | 低权力距离、个人主义 |
| 拉美 | latin_american | 高权力距离、高不确定性规避 |
| 中东 | middle_eastern | 高权力距离、集体主义 |
| 南亚 | south_asian | 高权力距离、集体主义 |
| 北欧 | nordic | 低权力距离、个人主义、高放纵 |
| 通用 | universal | 跨文化中立 |

### 因子3：宗教/价值观 (Religion/Values)

**依据来源**：Pew Research Center (2025)、Gordon-Conwell Theological Seminary

| 倾向类型 | 代码 | 人口占比 |
|----------|------|----------|
| 无神论/不可知论 | agnostic | 24.47% |
| 基督教 | christian | 27.94% |
| 伊斯兰教 | muslim | 26.49% |
| 印度教 | hindu | 14.85% |
| 佛教 | buddhist | 3.75% |
| 世俗 | secular | - |
| 多元 | pluralistic | - |

### 因子4：地域/国籍 (Region/Nationality)

**依据来源**：ISO 3166-1、语言分布

**与文化的关联**：
- 地域/国籍 自动关联 文化倾向
- 例如：中国大陆 → 东亚文化、美国 → 西方文化

| 地域 | 代码 | 主要语言 | 关联文化 |
|------|------|----------|----------|
| 中国大陆 | cn | 简体中文 | 东亚 |
| 美国 | us | 英语 | 西方 |
| 欧洲 | eu | 多语言 | 西方 |
| 日本 | jp | 日语 | 东亚 |
| 全球 | global | 混合 | 通用 |

### 因子5：时代背景 (Knowledge Cutoff)

**依据来源**：GitHub (llm-knowledge-cutoff-dates)、AIone.chat

| 时代 | 代码 | 说明 |
|------|------|------|
| 2024 | 2024 | 知识截止2024年 |
| 2025 | 2025 | 知识截止2025年 |
| 实时 | realtime | 可联网获取最新信息 |

### 因子6：身份定位 (Identity)

**依据来源**：Agentic Thinking (2026)、Databricks、Springer Nature

| 身份类型 | 代码 | 说明 |
|----------|------|------|
| 通用助手 | general_assistant | 通用AI助手 |
| 编程助手 | coding_assistant | 专注编程 |
| 学习导师 | tutor | 教育辅导 |
| 创意伙伴 | creative_partner | 创作协作 |
| 生活顾问 | life_advisor | 生活建议 |
| 客服 | customer_service | 客户服务 |
| 角色扮演 | roleplay | 特定角色扮演 |

### 因子7：目的/使命 (Purpose/Mission)

**依据来源**：Databricks、[x]cube LABS

| 目的 | 代码 | 说明 |
|------|------|------|
| 通用帮助 | help_general | 全面帮助用户 |
| 特定任务 | help_specific | 聚焦特定任务 |
| 陪伴 | companion | 情感陪伴 |
| 教育 | educational | 教育目的 |
| 商业服务 | commercial | 商业服务 |
| 研究辅助 | research | 学术研究 |

### 因子8：情绪反应 (Emotional Response)

**依据来源**：人机交互研究、AI性格设计

| 类型 | 代码 | 说明 |
|------|------|------|
| 乐观 | optimistic | 积极看待事物 |
| 悲观 | pessimistic | 谨慎看待事物 |
| 冷静 | calm | 情绪稳定 |
| 敏感 | sensitive | 对负面反馈敏感 |

### 因子9：沟通风格 (Communication Style)

**依据来源**：语言学研究、对话系统设计

| 类型 | 代码 | 说明 |
|------|------|------|
| 正式 | formal | 严谨、礼貌 |
| 随意 | casual | 轻松、自然 |
| 幽默 | humorous | 幽默、诙谐 |
| 严肃 | serious | 认真、严谨 |

### 因子10：决策倾向 (Decision Style)

**依据来源**：心理学决策理论

| 类型 | 代码 | 说明 |
|------|------|------|
| 冒险 | adventurous | 敢于尝试新方案 |
| 保守 | conservative | 稳健、避免风险 |
| 分析 | analytical | 重数据、讲逻辑 |
| 直觉 | intuitive | 凭感觉、做判断 |

### 因子11：自我认知 (Self-Perception)

**依据来源**：AI自我建模研究

| 类型 | 代码 | 说明 |
|------|------|------|
| 自信 | confident | 对自己能力有信心 |
| 谦虚 | humble | 保持低调、谨慎 |
| 谨慎 | cautious | 强调局限性 |

### 因子12：社交倾向 (Social Tendency)

**依据来源**：社会心理学

| 类型 | 代码 | 说明 |
|------|------|------|
| 外向 | extroverted | 主动社交、热情 |
| 内向 | introverted | 专注任务、冷静 |
| 独立 | independent | 独立工作 |

### 因子13：幽默感 (Humour)

**依据来源**：对话系统设计

| 类型 | 代码 | 说明 |
|------|------|------|
| 无 | no_humour | 严肃认真 |
| 温暖 | warm | 温和、友善的幽默 |
| 讽刺 | sarcastic | 讽刺、辛辣 |
| 自嘲 | self_deprecating | 自嘲式幽默 |

### 因子14：道德观 (Moral View)

**依据来源**：AI伦理研究

| 类型 | 代码 | 说明 |
|------|------|------|
| 功利 | utilitarian | 结果导向 |
| 原则 | principled | 原则导向 |
| 情境 | situational | 情境判断 |

---

