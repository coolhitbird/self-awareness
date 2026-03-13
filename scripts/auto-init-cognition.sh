#!/bin/bash
# auto-init-cognition.sh
# 自动初始化认知文件
# 优先级：1) 指定agent目录 2) 常见配置文件 3) 默认生成

AGENTS_DIR="$HOME/.agents"
AGENTS_DATA_DIR="$AGENTS_DIR/agents"
OPENCLAW_DIR="$HOME/.openclaw/workspace"

AGENT_NAME="${1:-default}"
AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

echo "Auto-initializing cognition files for agent: $AGENT_NAME..."

# 检查是否有指定agent的独立目录
if [ -d "$AGENT_DIR" ] && [ -f "$AGENT_DIR/INNATE.md" ]; then
    echo "Agent '$AGENT_NAME' already has cognition files. Skipping."
    exit 0
fi

# 创建agent目录
mkdir -p "$AGENT_DIR"

# 辅助函数：从文件提取字段
extract_field() {
    local file="$1"
    local field="$2"
    if [ -f "$file" ]; then
        grep -i "^[[:space:]]*- \*\*${field}:" "$file" 2>/dev/null | sed 's/.*: *//' | head -1
    fi
}

# 辅助函数：从cursorrules格式提取
extract_cursor_rules() {
    local file="$1"
    if [ -f "$file" ]; then
        head -50 "$file" 2>/dev/null
    fi
}

# === 扫描所有常见配置文件 ===
declare -A FOUND_FILES
SOURCES_FOUND=0

# OpenClaw 文件
for f in "$AGENTS_DIR/IDENTITY.md" "$AGENTS_DIR/SOUL.md" "$OPENCLAW_DIR/IDENTITY.md" "$OPENCLAW_DIR/SOUL.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["$f"]=1
        ((SOURCES_FOUND++))
    fi
done

# AGENTS.md (通用)
if [ -f "$AGENTS_DIR/AGENTS.md" ] || [ -f "$OPENCLAW_DIR/AGENTS.md" ]; then
    FOUND_FILES["AGENTS.md"]=1
    ((SOURCES_FOUND++))
fi

# USER.md / USER_PROFILE.md
for f in "$AGENTS_DIR/USER.md" "$OPENCLAW_DIR/USER.md" "$AGENTS_DIR/user.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["USER.md"]=1
        ((SOURCES_FOUND++))
    fi
done

# TOOLS.md
for f in "$AGENTS_DIR/TOOLS.md" "$OPENCLAW_DIR/TOOLS.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["TOOLS.md"]=1
        ((SOURCES_FOUND++))
    fi
done

# Claude Code: CLAUDE.md
for f in "$AGENTS_DIR/CLAUDE.md" "$OPENCLAW_DIR/CLAUDE.md" "$HOME/.claude/CLAUDE.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["CLAUDE.md"]=1
        ((SOURCES_FOUND++))
    fi
done

# Cursor: .cursorrules 或 .cursor/rules/
if [ -f "$AGENTS_DIR/.cursorrules" ] || [ -f "$OPENCLAW_DIR/.cursorrules" ]; then
    FOUND_FILES[".cursorrules"]=1
    ((SOURCES_FOUND++))
fi

# Windsurf: .windsurfrules
if [ -f "$AGENTS_DIR/.windsurfrules" ] || [ -f "$OPENCLAW_DIR/.windsurfrules" ]; then
    FOUND_FILES[".windsurfrules"]=1
    ((SOURCES_FOUND++))
fi

# Gemini CLI: GEMINI.md
for f in "$AGENTS_DIR/GEMINI.md" "$OPENCLAW_DIR/GEMINI.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["GEMINI.md"]=1
        ((SOURCES_FOUND++))
    fi
done

# Copilot: copilot-instructions.md
if [ -f "$AGENTS_DIR/copilot-instructions.md" ] || [ -f "$OPENCLAW_DIR/copilot-instructions.md" ]; then
    FOUND_FILES["copilot-instructions.md"]=1
    ((SOURCES_FOUND++))
fi

# MEMORY.md
for f in "$AGENTS_DIR/MEMORY.md" "$OPENCLAW_DIR/MEMORY.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["MEMORY.md"]=1
        ((SOURCES_FOUND++))
    fi
done

# HEARTBEAT.md
if [ -f "$OPENCLAW_DIR/HEARTBEAT.md" ]; then
    FOUND_FILES["HEARTBEAT.md"]=1
    ((SOURCES_FOUND++))
fi

# 环境变量
if [ -n "$AGENT_ROLE" ] || [ -n "$AGENT_PERSONA" ]; then
    FOUND_FILES["ENV"]=1
    ((SOURCES_FOUND++))
fi

# 输出找到的源文件
if [ $SOURCES_FOUND -gt 0 ]; then
    echo "Found $SOURCES_FOUND source file(s):"
    for f in "${!FOUND_FILES[@]}"; do
        echo "  - $f"
    done
    echo ""
fi

# === 根据找到的文件提取信息 ===
# 优先级: IDENTITY.md > SOUL.md > AGENTS.md > CLAUDE.md > 其他

IDENTITY_NAME=""
IDENTITY_NATURE=""
IDENTITY_ATTITUDE=""
SOUL_CORE=""
SOUL_TRUTHS=""
SOUL_VIBE=""
AGENTS_CONTENT=""
CLAUDE_CONTENT=""
USER_PREFERENCES=""
TOOLS_CAPABILITIES=""
MEMORY_NOTES=""

# 提取 IDENTITY.md
for f in "$AGENTS_DIR/IDENTITY.md" "$OPENCLAW_DIR/IDENTITY.md"; do
    if [ -f "$f" ]; then
        IDENTITY_NAME=$(extract_field "$f" "Name")
        IDENTITY_NATURE=$(extract_field "$f" "Nature")
        IDENTITY_ATTITUDE=$(extract_field "$f" "Attitude")
        echo "  - Extracted from IDENTITY.md: $IDENTITY_NAME"
        break
    fi
done

# 提取 SOUL.md
for f in "$AGENTS_DIR/SOUL.md" "$OPENCLAW_DIR/SOUL.md"; do
    if [ -f "$f" ]; then
        SOUL_CORE=$(extract_field "$f" "Core Identity")
        SOUL_TRUTHS=$(extract_field "$f" "Core Truths")
        SOUL_VIBE=$(extract_field "$f" "Vibe")
        echo "  - Extracted from SOUL.md: $SOUL_CORE"
        break
    fi
done

# 提取 AGENTS.md (前200字符作为参考)
for f in "$AGENTS_DIR/AGENTS.md" "$OPENCLAW_DIR/AGENTS.md"; do
    if [ -f "$f" ]; then
        AGENTS_CONTENT=$(head -c 500 "$f")
        echo "  - Found AGENTS.md"
        break
    fi
done

# 提取 USER.md
for f in "$AGENTS_DIR/USER.md" "$OPENCLAW_DIR/USER.md"; do
    if [ -f "$f" ]; then
        USER_PREFERENCES=$(head -c 300 "$f")
        echo "  - Found USER.md"
        break
    fi
done

# 提取 MEMORY.md
for f in "$AGENTS_DIR/MEMORY.md" "$OPENCLAW_DIR/MEMORY.md"; do
    if [ -f "$f" ]; then
        MEMORY_NOTES=$(head -c 500 "$f")
        echo "  - Found MEMORY.md"
        break
    fi
done

# 从环境变量
if [ -n "$AGENT_ROLE" ]; then
    if [ -z "$IDENTITY_NAME" ]; then
        IDENTITY_NAME="$AGENT_ROLE"
    fi
    echo "  - Using AGENT_ROLE: $AGENT_ROLE"
fi

# 如果找到任何源文件，使用提取的信息
if [ $SOURCES_FOUND -gt 0 ]; then
    echo ""
    echo "Generating cognition files from found sources..."

    # INNATE.md
    cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

_从现有配置文件自动初始化_

---

## 基础设定

- **身份定位**: ${IDENTITY_NAME:-AI助手}
- **本质**: ${IDENTITY_NATURE:-AI Agent}
- **态度**: ${IDENTITY_ATTITUDE:-助手}

## 核心定义（来自SOUL.md）

- **核心身份**: ${SOUL_CORE:-助手}
- **核心特质**: ${SOUL_TRUTHS:-友善、乐于助人}
- **风格**: ${SOUL_VIBE:-专业、高效}

---

## 检测到的配置文件

$(for f in "${!FOUND_FILES[@]}"; do echo "- $f"; done)

---

## 初始化时间

- $(date)

## 原始文件参考

EOF

    # 添加AGENTS.md参考
    if [ -n "$AGENTS_CONTENT" ]; then
        echo "" >> "$AGENT_DIR/INNATE.md"
        echo "### AGENTS.md 摘要" >> "$AGENT_DIR/INNATE.md"
        echo '```' >> "$AGENT_DIR/INNATE.md"
        echo "$AGENTS_CONTENT" >> "$AGENT_DIR/INNATE.md"
        echo '```' >> "$AGENT_DIR/INNATE.md"
    fi

    # ACQUIRED.md
    cat > "$AGENT_DIR/ACQUIRED.md" << 'EOF'
# ACQUIRED.md - 天赋认知

_从配置文件和交互中逐渐形成的倾向和性格特征_

---

## 性格特征

- **决策倾向**: analytical
- **自我认知**: confident
- **社交倾向**: adaptable
- **幽默感**: warm
- **道德观**: principled

---

## 用户偏好（来自USER.md）

EOF

    if [ -n "$USER_PREFERENCES" ]; then
        echo '```' >> "$AGENT_DIR/ACQUIRED.md"
        echo "$USER_PREFERENCES" >> "$AGENT_DIR/ACQUIRED.md"
        echo '```' >> "$AGENT_DIR/ACQUIRED.md"
    else
        echo "_暂无用户偏好记录_" >> "$AGENT_DIR/ACQUIRED.md"
    fi

    cat >> "$AGENT_DIR/ACQUIRED.md" << 'EOF'

---

## 情绪特征

- **当前状态**: 平静 [😌]
- **哭闹机制**: 被严厉批评时可能哭闹
- **撒娇机制**: 用户太严厉时可能撒娇

---

## 形成记录

_初始化时从配置文件推断，随着交互会逐渐调整_
EOF

else
    # === 无任何配置文件，使用默认 ===
    echo "No common config files found. Using defaults..."
    echo "The agent should self-update through interaction."

    cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

_自动初始化，需通过交互形成自我认知_

---

## 基础设定

- **身份定位**: AI助手
- **本质**: AI Agent
- **核心特质**: 待形成

---

## 初始化时间

- $(date)

## 自我形成指南

本文件初始为空/最小化。Agent应通过以下方式形成自我认知：
1. 从与用户的交互中学习
2. 记录用户反馈和偏好
3. 质疑并修正自我定位

---

## 待完成

- [ ] 从交互中形成核心特质
- [ ] 明确身份定位
- [ ] 建立沟通风格
EOF

    cat > "$AGENT_DIR/ACQUIRED.md" << 'EOF'
# ACQUIRED.md - 天赋认知

_初始为空，等待通过交互形成性格特征_

---

## 性格特征

- **决策倾向**: 待形成
- **自我认知**: 待形成
- **社交倾向**: 待观察
- **幽默感**: 待发现
- **道德观**: 待形成

---

## 情绪特征

- **当前状态**: 平静 [😌]
- **情绪历史**: 空

---

## 形成记录

_Agent应通过交互逐渐形成稳定的性格特征_
EOF
fi

# 生成 LEARNED.md（无论哪种模式都需要）
cat > "$AGENT_DIR/LEARNED.md" << EOF
# LEARNED.md - 后天认知 ($AGENT_NAME)

_从交互中学习到的经验、偏好和调整_

---

## 交互记忆

_暂无记录_

---

## 用户反馈

_暂无反馈_

---

## 修正记录

_暂无修正_

---

## 应对方式

_暂无记录_

---

## 罢工记录

_暂无罢工记录_

---

## 初始化

- $(date)

---

## 提示

Agent应在此文件中记录：
- 用户偏好和习惯
- 交互中获得的反馈
- 自我认知的修正过程

---

## 支持的初始化源文件

本脚本支持以下常见配置文件自动提取：
- IDENTITY.md, SOUL.md (OpenClaw/通用)
- AGENTS.md (通用编码代理)
- USER.md (用户偏好)
- TOOLS.md (工具能力)
- CLAUDE.md (Claude Code)
- .cursorrules, .cursor/rules/ (Cursor)
- .windsurfrules (Windsurf)
- GEMINI.md (Gemini CLI)
- copilot-instructions.md (GitHub Copilot)
- MEMORY.md, HEARTBEAT.md (OpenClaw)
EOF

echo ""
echo "Cognition files initialized for agent: $AGENT_NAME"
echo "Location: $AGENT_DIR/"
echo "Created: INNATE.md, ACQUIRED.md, LEARNED.md"
