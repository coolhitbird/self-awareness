# Self-Awareness Execution

## 使用流程

### 1. 安装
```bash
cd ~/.openclaw/workspace/skills/self-awareness
git pull origin master
powershell -ExecutionPolicy Bypass -File scripts/install.ps1
openclaw gateway restart
```

### 2. 初始化Agent认知文件
```bash
bash scripts/auto-init-cognition.sh <agent_name>
```

### 3. 运行测试
```bash
cd ~/.openclaw/workspace/skills/self-awareness
python -X utf8 test_full.py
```

## 核心模块

| 模块 | 路径 | 功能 |
|------|------|------|
| cognition | `src/cognition/` | 认知文件读写 |
| models | `src/models/` | 状态系统 |
| engines | `src/engines/` | 评估引擎 |
| triggers | `src/triggers/` | 触发机制 |
| avatar | `src/avatar/` | 头像生成 |
| telemetry | `src/telemetry/` | 遥测分析 |

## 状态机

```
calm → curious → engaged → confident
                  ↓
              frustrated → anxious → tired
                              ↓
                          inspired → nurturing
```

## 触发时机

| 触发器 | 时机 | prompt长度 |
|--------|------|------------|
| INIT | 初始化 | 339字符 |
| FIRST_RESPONSE | 首次响应 | 268字符 |
| PERIODIC_5 | 每5分钟 | 248字符 |
| IDLE_5MIN | 空闲5分钟 | 242字符 |
| EMOTION_DECAY | 30分钟衰减 | 0字符 |
| HEARTBEAT | 心跳检查 | 182字符 |
