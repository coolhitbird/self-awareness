# 热加载与自动触发机制（参考数据）

> 本文件是 `self-awareness` 的数据参考。认知文件默认只在 Agent 启动时读取一次，以下机制解决运行时刷新与周期自检。
> 正文工作流见 `SKILL.md`。

## 一、热加载机制

### 问题背景

认知文件（INNATE.md, ACQUIRED.md, LEARNED.md）默认只在 Agent 启动时读取一次。如果需要在运行时更新认知，需要热加载机制。

### 解决方案

#### 1. 关键词触发刷新

在 Agent 的「自我质疑」流程中，检测以下关键词自动刷新：

| 触发词 | 说明 |
|--------|------|
| 记住 | 用户要求记住某些内容 |
| 之前 | 用户提到之前的对话 |
| 刷新 | 用户明确要求刷新 |
| 重新认识 | 用户想重新初始化认知 |

```
用户输入 → 触发词检测 → 是 → 重新读取认知文件 → 继续流程
```

#### 2. 手动命令刷新

用户可以明确要求 Agent 刷新认知：

```
用户: "刷新一下你的认知" / "重新加载你的配置"
Agent: → 重新读取 INNATE.md, ACQUIRED.md, LEARNED.md
     → 回复: "认知已刷新，当前状态: [😌]"
```

#### 3. 时间戳检测

在 ACQUIRED.md 中记录最后更新时间：

```markdown
## 元信息
- 最后更新: 2026-03-16 10:30:00
```

Agent 每次响应前检查：
- 如果超过 5 分钟 → 静默刷新（可选）

#### 4. 敏感操作确认

对于重大认知变更（如身份定位修改），需要确认：

```
Agent: "你想把我定义为'诗人'吗？确认后我会更新 INNATE.md"
用户: "确认"
Agent: → 更新 INNATE.md → "好的，我现在是诗人了 [😊]"
```

### 实现示例

```python
def should_refresh_cognition(user_input):
    """检查是否需要刷新认知"""
    refresh_keywords = ["记住", "之前", "刷新", "重新认识", "重新加载"]

    for keyword in refresh_keywords:
        if keyword in user_input:
            return True
    return False

def refresh_cognition(agent_id):
    """刷新认知文件"""
    import os
    agent_dir = os.path.expanduser(f"~/.agents/agents/{agent_id}")

    files = {
        "INNATE": os.path.join(agent_dir, "INNATE.md"),
        "ACQUIRED": os.path.join(agent_dir, "ACQUIRED.md"),
        "LEARNED": os.path.join(agent_dir, "LEARNED.md")
    }

    cognition = {}
    for name, path in files.items():
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                cognition[name] = f.read()

    return cognition
```

### 注意事项

1. **性能考量** - 不要每次响应都读取文件，只在必要时刷新
2. **版本控制** - 刷新前保存当前版本，便于回滚
3. **原子写入** - 更新文件时使用原子操作（先写临时文件再替换）

---

## 二、自动触发机制

除了用户主动触发外，Agent 可以在特定时机自动执行认知更新。

### 触发器矩阵

| 触发器 | 时机 | 操作 | 可选 |
|--------|------|------|------|
| **init** | Agent 启动 | 加载认知文件 | ✅ |
| **first_response** | 首次回复 | 确认情绪状态 | ✅ |
| **periodic_5** | 每 5 轮对话 | 自检 + 更新记忆 | ✅ |
| **idle_5min** | 空闲 5 分钟 | 空闲思考 | ✅ |
| **emotion_decay_30min** | 每 30 分钟 | 情绪衰减 | ✅ |
| **heartbeat** | 心跳周期 | 轻量检查 | ✅ |

### 1️⃣ 初始化触发（init）

```
Agent 启动 → 读取认知文件 → 首次状态确认
```

- 读取 INNATE.md, ACQUIRED.md, LEARNED.md
- 确认当前情绪状态
- 显示颜文字头像

### 2️⃣ 首次回复触发（first_response）

```
对话开始后第一条回复 → 触发"状态确认"
```

- 读取最新情绪状态
- 在回复中自然融入情绪

### 3️⃣ 周期自检触发（periodic_5）

```
用户输入 5 次后 → 触发"自检"
```

- 回顾最近 5 轮对话
- 评估情绪变化趋势
- 可选：更新 LEARNED.md

### 4️⃣ 空闲触发（idle_5min）

```
用户超过 5 分钟无输入 → 触发"空闲思考"
```

- 根据性格生成思考内容
- 可选：主动发起话题 / 自省 / 更新 LEARNED.md

### 5️⃣ 情绪衰减触发（emotion_decay_30min）

```
每 30 分钟 → 情绪逐渐回归平静
```

```
当前情绪 ←──衰减── 平静 [😌]
    │
  强度 -10%
```

### 6️⃣ 心跳触发（heartbeat）

```
Agent 心跳周期 → 轻量检查
```

- 更新最后活跃时间
- 可扩展：定时保存记忆

### 触发配置示例

```yaml
# 可在 ACQUIRED.md 中配置
triggers:
  init:
    enabled: true

  first_response:
    enabled: true

  periodic_5:
    enabled: true
    action: "self_check"

  idle_5min:
    enabled: false  # 可关闭
    action: "idle_thinking"

  emotion_decay_30min:
    enabled: true
    decay_rate: 0.1

  heartbeat:
    enabled: false  # 需要客户端支持
```
