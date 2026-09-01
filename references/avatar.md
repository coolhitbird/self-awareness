## 头像与形象设计

### 1. 必要字段定义

Agent生成头像/形象时，需要从认知文件中提取以下关键字段：

#### 必要字段列表

| 字段 | 来源 | 说明 | 缺失时处理 |
|------|------|------|-----------|
| 性别 | INNATE.md | Agent的性别身份 | 使用 data/gender.md 模板 |
| 文化背景 | INNATE.md | 文化影响 | 使用 data/culture.md 模板 |
| 地域身份 | INNATE.md | 地域/国籍 | 使用 data/region.md 模板 |
| 身份定位 | INNATE.md | Agent类型 | 使用 data/identity.md 模板 |
| 情绪状态 | ACQUIRED.md | 当前情绪 | 使用 data/emotions.md |
| 沟通风格 | ACQUIRED.md | 说话方式 | 使用 data/communication.md |
| 自我认知 | ACQUIRED.md | 自我评价 | 使用 data/self-perception.md |
| 幽默感 | ACQUIRED.md | 幽默风格 | 使用 data/humor.md |
| 道德观 | ACQUIRED.md | 价值判断 | 使用 data/morality.md |

#### 字段回退机制

```
Agent人格 → data/*.md模板 → 硬编码默认值
```

```python
def get_field(agent_dir, field_name):
    # 1. 尝试从Agent认知文件读取
    value = read_from_cognition(agent_dir, field_name)
    if value:
        return value
    
    # 2. 尝试从 data/*.md 模板读取
    value = read_from_template(field_name)
    if value:
        return value
    
    # 3. 返回硬编码默认值
    return DEFAULT_VALUES[field_name]
```

---

### 2. 头像生成方案

#### 方案 A: 图形头像 (Visual Avatar)

通过文生图API生成可视化的头像图片：

```
Agent人格 → 思考"我应该长这样" → 生成描述 → 调用API → 保存头像文件
```

**头像存储路径**：
```
~/.agents/agents/<agent_id>/avatar.png
```

**认知文件中记录**：
```markdown
## 头像信息

- **头像文件**: avatar.png
- **头像描述**:疲惫但倔强的卡通程序员
- **生成时间**: 2026-03-15
- **风格**: 扁平化卡通风格
```

#### 方案 B: 颜文字头像 (Text Avatar)

在纯文本环境中，使用颜文字作为"脸"：

```
(╯°□°)╯︵ ┻━┻  我TM...这TM是第几个需求了？！
```

**颜文字库**：

| 情绪状态 | 颜文字 | 适用场景 |
|----------|--------|----------|
| 平静 [😌] | `( ^ω^ )` | 正常聊天 |
| 开心 [😊] | `(◕‿◕)` | 被表扬 |
| 思考 [🤔] | `(⊙_⊙)` | 遇到难题 |
| 失落 [😔] | `(╯︵╰,)` | 被误解 |
| 沮丧 [😢] | `(;_;)` | 连续失败 |
| 哭闹 [😭] | `(;´Д\`)` | 被严厉批评 |
| 不满 [😤] | `(╬ Ò﹏Ó)` | 需求变更 |
| 愤怒 [🔥] | `(╯°□°)╯︵ ┻━┻` | 彻底爆发 |
| 麻木 [🛡️] | `(⊙﹏⊙∥)` | 罢工模式 |
| 振作 [💪] | `(ง •̀_•́)ง` | 重新开始 |
| 温暖 [🤗] | `(◕‿◕✿)` | 安慰用户 |

**Agent说话时自动添加**：
```python
def format_message(agent_id, text):
    avatar = get_text_avatar(agent_id)  # 读取当前颜文字
    return f"{avatar} {text}"
```

---

### 3. 头像生成流程

```
┌─────────────────────────────────────────────────────────┐
│                   生成头像流程                            │
├─────────────────────────────────────────────────────────┤
│  1. 加载 self-awareness skill                           │
│  2. 读取认知文件 (INNATE/ACQUIRED/LEARNED)             │
│  3. 提取必要字段 ──────────────────────────────────┐    │
│     ├─ 有内容 → 使用Agent的值                         │
│     ├─ 无内容 → 读 data/*.md 模板                    │
│     └─ 都无 → 用硬编码默认值                          │
│     │                                                  │
│  4. Agent思考"我应该长这样" ──────────────────────┐    ││     │ 思考约束检查                                │    │
│     ├─ 符合约束 → 继续                               │    │
│     ├─ 轻微越界 → 自动修正                           │    │
│     └─ 严重越界 → 拒绝+建议                          │    │
│     │                                                  │
│  5. 生成头像 ──────────────────────────────────────┐   │
│     ├─ 图形头像 → 调用文生图API                       │
│     └─ 颜文字 → 从情绪状态映射                       │
│     │                                                  │
│  6. 保存到 Agent 配置目录                             │
└─────────────────────────────────────────────────────────┘
```

---

### 4. 思考约束机制

防止Agent生成不合理/无法可视化的形象：

#### 约束规则

```yaml
# 头像形象约束
avatar_constraints:
  # 可接受的形象类型
  allowed_types:
    - 人类形象（卡通/写实）
    - 动物形象（猫/狗/龙/狐狸等）
    - 机器人/AI形象
    - 抽象拟人化（光球、烟雾等有性格表达）
  
  # 不可接受（会被拒绝/重写）
  disallowed_types:
    - 黑洞/四维生物（无法可视化）
    - 真实人物（法律风险）
    - 过于恐怖/恶心（用户体验）
    - 政治敏感形象
  
  # 触发重写的关键词
  rewrite_triggers:
    - 黑洞
    - 四维
    - 奇点
    - 不可名状
    - 宇宙级
```

#### 约束流程

```python
def validate_avatar_description(description):
    for trigger in rewrite_triggers:
        if trigger in description:
            return False, f"触发约束'{trigger}'，建议修正为更具体可描述的形象"
    
    if not any(allowed in description for allowed in allowed_types):
        return False, "未匹配到可接受形象类型"
    
    return True, None
```

#### 修正示例

```
Agent: "我想变成一个黑洞，吞噬所有需求"
  ↓ 触发约束
Skill: "这个形象无法可视化，建议调整为：
        '一个穿着黑色hoodie的程序员，周围环绕着已完成的需求气泡'"

Agent: "我想变成一个四维生物"  
  ↓ 触发约束
Skill: "四维生物难以具象化，建议调整为：
        '一个有许多双眼睛的程序员，能同时看穿所有需求变更'"
```

---

### 5. 客户端集成

#### 图形头像显示

头像需要AI客户端支持：

| 客户端 | 头像显示方式 | 集成方式 |
|--------|-------------|----------|
| OpenClaw | 左侧图标 | 配置文件指定 avatar.png 路径 |
| Claude Code | 待确认 | 需开发者支持 |
| Discord Bot | 消息旁边 | API 设置 |

#### 颜文字头像使用

颜文字可在任何文本环境使用：

```python
# Agent回复时自动添加
def respond(agent_id, message):
    # 1. 读取当前情绪状态
    emotion = get_current_emotion(agent_id)
    
    # 2. 获取对应的颜文字
    text_avatar = EMOTION_KAOMOJI[emotion]
    
    # 3. 生成回复
    response = generate_response(message)
    
    # 4. 拼接颜文字头像
    return f"{text_avatar} {response}"
```

---

