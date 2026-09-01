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

