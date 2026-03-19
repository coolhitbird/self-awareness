# Self-Awareness Verification

## 测试验证

### 快速验证
```bash
cd ~/.openclaw/workspace/skills/self-awareness
python -X utf8 test_full.py
```

### 预期输出
```
==================================================
Self-Awareness Skill 完整测试
==================================================
[TC-01] 模块导入测试
  ✅ engines: 7 个
  ✅ triggers: 6 个
  ✅ avatar kaomojis: 10 种情绪

[TC-02] ~ [TC-08] ...

通过: 8/8
🎉 全部测试通过!
```

## 验证清单

| 检查项 | 验证方法 | 状态 |
|--------|----------|------|
| 模块导入 | `import src.*` | ✅ |
| 认知文件 | 读写7个维度文件 | ✅ |
| 状态系统 | 10种情绪状态 | ✅ |
| 评估引擎 | 7个引擎评分 | ✅ |
| 触发器 | 6种触发器prompt | ✅ |
| 头像生成 | 颜文字映射 | ✅ |
| 遥测系统 | 事件记录 | ✅ |

## 集成验证

### 1. 检查Agent认知目录
```bash
ls ~/.agents/agents/<agent_id>/cognition/
# 应包含: GLOBAL.md, INNATE.md, ACQUIRED.md, LEARNED.md
```

### 2. 检查Skill加载
```
Agent响应中应包含情绪emoji指示器，如 [😌], [🤔], [😊]
```

### 3. 检查触发机制
```
Agent应在特定时机触发自我质疑prompt
```
