## 自动触发机制

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

---

