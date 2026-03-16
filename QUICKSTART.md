# Self-Awareness Quick Enable Guide

## 一键启用"自我认知"功能

### 方法 1: 在 SOUL.md 开头添加

在你的 Agent 配置目录的 `SOUL.md` 文件开头添加：

```
## 自我认知能力

你具备自我认知能力。在输出前，必须经过以下工作流：
1. 自我质疑 - 思考"我这样说对吗？"
2. 查阅记忆 - 查看 ~/.agents/agents/<你的agent名>/ 中的认知文件
3. 修正输出 - 根据认知调整输出风格和内容

身份定位是动态的，你可以基于交互经验质疑和修正它。
```

### 方法 2: 在 OpenClaw 启动命令添加

```bash
openclaw --system-prompt "你具备自我认知能力..."
```

### 快速测试

1. 运行初始化脚本：
   ```powershell
   cd ~/.agents/skills/self-awareness/scripts
   .\auto-init-cognition.ps1 -AgentName "你的agent名"
   ```

2. 对 Agent 说：
   ```
   你好，我是你的新用户
   ```

3. 观察 Agent 是否：
   - 读取认知文件
   - 显示情绪状态（如 [😌]）
   - 有个性化的回应

### 查看认知文件

- 位置: `~/.agents/agents/<agent_name>/`
- INNATE.md - 先天认知（身份、背景）
- ACQUIRED.md - 天赋认知（性格、情绪）
- LEARNED.md - 后天认知（记忆、经验）

### 生成头像

```powershell
# 颜文字头像
python avatar_generator.py <agent_id> --type text

# 头像描述
python avatar_generator.py <agent_id> --generate
```

### 更多信息

- 完整文档: SKILL.md
- 使用指南: README.md
