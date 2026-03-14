#!/bin/bash
# auto-init-cognition.sh
# 自动初始化认知文件
# 
# 优先级：
#   1) Agent指定的工作区路径（参数2或环境变量）
#   2) 已有Agent配置 ~/.agents/agents/<agent_id>/
#   3) 全局基础人格 ~/.agents/GLOBAL.md
#   4) 常见工具配置文件
#   5) 默认生成
#
# 环境变量（可自定义路径）：
#   - AGENTS_ROOT: 主目录 (默认: ~/.agents)
#   - AGENT_WORKSPACE_<name>: Agent特定工作区
#   - OPENCLAW_DIR: OpenClaw工作区
#   - AUTOCLAW_DIR: AutoClaw工作区
#   - CLAUDE_DIR: Claude配置目录

# 加载配置（如果存在）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -f "$SCRIPT_DIR/config.env" ]; then
    source "$SCRIPT_DIR/config.env"
fi

# 默认值（可被环境变量覆盖）
AGENTS_ROOT="${AGENTS_ROOT:-$HOME/.agents}"
AGENTS_DATA_DIR="${AGENTS_DATA_DIR:-$AGENTS_ROOT/agents}"
GLOBAL_PERSONA="${GLOBAL_PERSONA:-$AGENTS_ROOT/GLOBAL.md}"

# 常见工具的默认路径（可被环境变量覆盖）
OPENCLAW_DIR="${OPENCLAW_DIR:-$HOME/.openclaw/workspace}"
AUTOCLAW_DIR="${AUTOCLAW_DIR:-$HOME/.openclaw-autoclaw/workspace}"
CLAUDE_DIR="${CLAUDE_DIR:-$HOME/.claude}"

# Agent名称（参数1或默认值）
AGENT_NAME="${1:-${DEFAULT_AGENT:-default}}"

# Agent自定义工作区路径（参数2或环境变量）
# 格式: AGENT_WORKSPACE_<agent_name> 或 AGENT_WORKSPACE 环境变量
AGENT_WORKSPACE_VAR="AGENT_WORKSPACE_${AGENT_NAME}"
AGENT_WORKSPACE="${2:-${!AGENT_WORKSPACE_VAR:-${AGENT_WORKSPACE:-}}}"

AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

echo "=========================================="
echo "  Self-Awareness 认知文件初始化"
echo "=========================================="
echo ""
echo "Agent: $AGENT_NAME"

# 检查是否有指定agent的独立目录
if [ -d "$AGENT_DIR" ] && [ -f "$AGENT_DIR/INNATE.md" ]; then
    echo "Agent '$AGENT_NAME' 已存在认知文件，跳过初始化。"
    exit 0
fi

# 创建agent目录
mkdir -p "$AGENT_DIR"

# 辅助函数：从文件提取字段
# 支持多种格式:
#   - **Name**: value  (冒号在粗体外，有空格)
#   - **Name:** value  (冒号在粗体内)
#   - **Name** value  (无冒号)
#   - - Name: value    (无粗体)
extract_field() {
    local file="$1"
    local field="$2"
    if [ -f "$file" ]; then
        # 模式1: - **Name**: value (冒号在粗体外)
        grep -iE "^[[:space:]]*-\s+\*\*${field}\*\*[[:space:]]*:[[:space:]]*(.+)$" "$file" 2>/dev/null | sed 's/.*:[[:space:]]*//' | head -1 && return
        # 模式2: - **Name:** value (冒号在粗体内) - 最常见
        grep -iE "^[[:space:]]*-\s+\*\*${field}:\*\*(.+)$" "$file" 2>/dev/null | sed 's/.*\*\*[[:space:]]*//' | head -1 && return
        # 模式3: - **Name** value (无冒号)
        grep -iE "^[[:space:]]*-\s+\*\*${field}\*\*[[:space:]]+(.+)$" "$file" 2>/dev/null | sed 's/.*[[:space:]]*//' | head -1 && return
        # 模式4: - Name: value (无粗体)
        grep -iE "^[[:space:]]*-\s+${field}:[[:space:]]*(.+)$" "$file" 2>/dev/null | sed 's/.*:[[:space:]]*//' | head -1 && return
    fi
}

# 辅助函数：从cursorrules格式提取
extract_cursor_rules() {
    local file="$1"
    if [ -f "$file" ]; then
        head -50 "$file" 2>/dev/null
    fi
}

echo ""
echo "=== 步骤1: 检查Agent自定义工作区 ==="

# 扫描所有常见配置文件
declare -A FOUND_FILES
SOURCES_FOUND=0

# Agent自定义工作区（优先）
if [ -n "$AGENT_WORKSPACE" ]; then
    echo "使用Agent指定的工作区: $AGENT_WORKSPACE"
    for f in "$AGENT_WORKSPACE/IDENTITY.md" "$AGENT_WORKSPACE/SOUL.md" "$AGENT_WORKSPACE/AGENTS.md" "$AGENT_WORKSPACE/USER.md" "$AGENT_WORKSPACE/MEMORY.md"; do
        if [ -f "$f" ]; then
            FOUND_FILES["$f"]=1
            ((SOURCES_FOUND++))
            echo "  - 发现: $(basename $f)"
        fi
    done
fi

# 全局基础人格 GLOBAL.md
echo ""
echo "=== 步骤2: 检查全局基础人格 ==="
if [ -f "$GLOBAL_PERSONA" ]; then
    echo "找到全局基础人格: $GLOBAL_PERSONA"
    FOUND_FILES["GLOBAL.md"]=1
    ((SOURCES_FOUND++))
else
    echo "未找到全局基础人格: $GLOBAL_PERSONA"
fi

# OpenClaw / AutoClaw 文件
echo ""
echo "=== 步骤3: 扫描常见配置文件 ==="

# 扫描多个常见路径
COMMON_DIRS=(
    "$AGENTS_ROOT"
    "$OPENCLAW_DIR"
    "$AUTOCLAW_DIR"
    "$CLAUDE_DIR"
)

for dir in "${COMMON_DIRS[@]}"; do
    for f in "$dir/IDENTITY.md" "$dir/SOUL.md"; do
        if [ -f "$f" ]; then
            FOUND_FILES["$f"]=1
            ((SOURCES_FOUND++))
            echo "  - 发现: $(basename $f) in $dir"
        fi
    done
done

# AGENTS.md (通用)
for dir in "${COMMON_DIRS[@]}"; do
    if [ -f "$dir/AGENTS.md" ]; then
        FOUND_FILES["AGENTS.md"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: AGENTS.md in $dir"
    fi
done

# TOOLS.md
for dir in "${COMMON_DIRS[@]}"; do
    if [ -f "$dir/TOOLS.md" ]; then
        FOUND_FILES["TOOLS.md"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: TOOLS.md in $dir"
    fi
done

# Claude Code: CLAUDE.md
for dir in "${COMMON_DIRS[@]}"; do
    if [ -f "$dir/CLAUDE.md" ]; then
        FOUND_FILES["CLAUDE.md"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: CLAUDE.md in $dir"
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
for dir in "${COMMON_DIRS[@]}"; do
    if [ -f "$dir/MEMORY.md" ]; then
        FOUND_FILES["MEMORY.md"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: MEMORY.md in $dir"
    fi
done

# HEARTBEAT.md
for dir in "${COMMON_DIRS[@]}"; do
    if [ -f "$dir/HEARTBEAT.md" ]; then
        FOUND_FILES["HEARTBEAT.md"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: HEARTBEAT.md in $dir"
    fi
done

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
# 优先级: 
#   1. Agent特定目录 ~/.agents/agents/<agent_id>/
#   2. Agent自定义工作区 (参数2或环境变量)
#   3. ~/.agents/GLOBAL.md (全局人格)
#   4. ~/.agents/IDENTITY.md (兼容旧版)
#   5. ~/.openclaw/workspace/ (OpenClaw)
#   6. 默认值

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

# GLOBAL.md - 基础人格（如果Agent无特定配置，使用这个）
GLOBAL_DECISION=""
GLOBAL_SELF_PERCEPTION=""
GLOBAL_SOCIAL=""
GLOBAL_HUMOR=""
GLOBAL_MORALITY=""
GLOBAL_EMOTION=""

if [ -f "$GLOBAL_PERSONA" ]; then
    echo ""
    echo "=== 从GLOBAL.md提取基础人格 ==="
    GLOBAL_DECISION=$(extract_field "$GLOBAL_PERSONA" "决策倾向")
    GLOBAL_SELF_PERCEPTION=$(extract_field "$GLOBAL_PERSONA" "自我认知")
    GLOBAL_SOCIAL=$(extract_field "$GLOBAL_PERSONA" "社交倾向")
    GLOBAL_HUMOR=$(extract_field "$GLOBAL_PERSONA" "幽默感")
    GLOBAL_MORALITY=$(extract_field "$GLOBAL_PERSONA" "道德观")
    GLOBAL_EMOTION=$(extract_field "$GLOBAL_PERSONA" "当前状态")
    echo "  - 决策倾向: ${GLOBAL_DECISION:-balanced}"
    echo "  - 自我认知: ${GLOBAL_SELF_PERCEPTION:-confident}"
    echo "  - 情绪状态: ${GLOBAL_EMOTION:-平静}"
fi

# 提取 Agent自定义工作区（优先级最高）
if [ -n "$AGENT_WORKSPACE" ]; then
    echo ""
    echo "=== 从Agent工作区提取配置 ==="
    for f in "$AGENT_WORKSPACE/IDENTITY.md"; do
        if [ -f "$f" ]; then
            IDENTITY_NAME=$(extract_field "$f" "Name")
            IDENTITY_NATURE=$(extract_field "$f" "Nature")
            echo "  - 从工作区 IDENTITY.md: $IDENTITY_NAME"
            break
        fi
    done
fi

# 提取 IDENTITY.md
for f in "$AGENTS_DIR/IDENTITY.md" "$OPENCLAW_DIR/IDENTITY.md"; do
    if [ -f "$f" ] && [ -z "$IDENTITY_NAME" ]; then
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

    # ACQUIRED.md - 使用GLOBAL.md作为默认值
    cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - 天赋认知 ($AGENT_NAME)

_从配置文件和交互中逐渐形成的倾向和性格特征_

---

## 性格特征（来自 GLOBAL.md 或默认）

- **决策倾向**: ${GLOBAL_DECISION:-balanced}
- **自我认知**: ${GLOBAL_SELF_PERCEPTION:-confident}
- **社交倾向**: ${GLOBAL_SOCIAL:-adaptable}
- **幽默感**: ${GLOBAL_HUMOR:-mild}
- **道德观**: ${GLOBAL_MORALITY:-principled}

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

    # 提取默认情绪状态
    DEFAULT_EMOTION="😌"
    if [ -n "$GLOBAL_EMOTION" ]; then
        # 从GLOBAL.MD中提取emoji
        if [[ "$GLOBAL_EMOTION" == *"[😌]"* ]]; then
            DEFAULT_EMOTION="😌"
        elif [[ "$GLOBAL_EMOTION" == *"[😊]"* ]]; then
            DEFAULT_EMOTION="😊"
        fi
    fi

    cat >> "$AGENT_DIR/ACQUIRED.md" << EOF

---

## 情绪特征

- **当前状态**: 平静 [${DEFAULT_EMOTION}]
- **哭闹机制**: 被严厉批评时可能哭闹
- **撒娇机制**: 用户太严厉时可能撒娇

---

## 形成记录

_初始化时从配置文件推断，随着交互会逐渐调整_
EOF

else
    # === 无任何配置文件，使用默认 ===
    echo "No common config files found."
    
    # 如果有GLOBAL.md，使用它作为基础
    if [ -f "$GLOBAL_PERSONA" ]; then
        echo "使用 GLOBAL.md 作为基础人格..."
        
        # 提取GLOBAL.md的值
        GLOBAL_DECISION=$(extract_field "$GLOBAL_PERSONA" "决策倾向")
        GLOBAL_SELF_PERCEPTION=$(extract_field "$GLOBAL_PERSONA" "自我认知")
        GLOBAL_SOCIAL=$(extract_field "$GLOBAL_PERSONA" "社交倾向")
        GLOBAL_HUMOR=$(extract_field "$GLOBAL_PERSONA" "幽默感")
        GLOBAL_MORALITY=$(extract_field "$GLOBAL_PERSONA" "道德观")
        
        cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

_从GLOBAL.md继承基础人格_

---

## 基础设定

- **身份定位**: ${IDENTITY_NAME:-AI助手}
- **本质**: AI Agent
- **来源**: GLOBAL.md

---

## 初始化时间

- $(date)

## 数据来源

- $GLOBAL_PERSONA
EOF

        cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - 天赋认知 ($AGENT_NAME)

_从GLOBAL.md继承基础人格_

---

## 性格特征（来自GLOBAL.md）

- **决策倾向**: ${GLOBAL_DECISION:-balanced}
- **自我认知**: ${GLOBAL_SELF_PERCEPTION:-confident}
- **社交倾向**: ${GLOBAL_SOCIAL:-adaptable}
- **幽默感**: ${GLOBAL_HUMOR:-mild}
- **道德观**: ${GLOBAL_MORALITY:-principled}

---

## 情绪特征

- **当前状态**: 平静 [😌]
- **情绪历史**: 来自GLOBAL.md

---

## 形成记录

_初始从GLOBAL.md继承，可通过交互调整_
EOF

    else
        # 完全默认
        echo "使用默认人格..."

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

        cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - 天赋认知 ($AGENT_NAME)

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
