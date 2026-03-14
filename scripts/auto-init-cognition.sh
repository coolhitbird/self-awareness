#!/bin/bash
# auto-init-cognition.sh
# 自动初始化认知文件
# 
# 核心设计：Agent告诉Skill自己的配置在哪里
# 
# 使用方式：
#   bash auto-init-cognition.sh <agent_name> [agent_workspace_dir]
#
# 环境变量（Agent可设置）：
#   - AGENT_WORKSPACE_<name>: Agent告诉Skill自己的配置目录
#   - DEFAULT_AGENT: 默认Agent名称

# Agent名称（参数1或默认值）
AGENT_NAME="${1:-${DEFAULT_AGENT:-default}}"

# Agent告诉Skill自己的配置目录（参数2优先，否则检查环境变量）
AGENT_WORKSPACE_VAR="AGENT_WORKSPACE_${AGENT_NAME}"
AGENT_WORKSPACE="${2:-${!AGENT_WORKSPACE_VAR:-${AGENT_WORKSPACE:-}}}"

# Agent配置文件目录
AGENTS_ROOT="${AGENTS_ROOT:-$HOME/.agents}"
AGENTS_DATA_DIR="${AGENTS_ROOT}/agents"
GLOBAL_PERSONA="${AGENTS_ROOT}/GLOBAL.md"

# skill目录（用于获取默认模板）
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DEFAULT_GLOBAL="$SKILL_DIR/data/GLOBAL.md"
AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

echo "=========================================="
echo "  Self-Awareness 认知文件初始化"
echo "=========================================="
echo ""
echo "Agent: $AGENT_NAME"
echo "Agent工作区: ${AGENT_WORKSPACE:-未指定}"

# 检查是否有指定agent的独立目录
if [ -d "$AGENT_DIR" ] && [ -f "$AGENT_DIR/INNATE.md" ]; then
    echo "Agent '$AGENT_NAME' 已存在认知文件，跳过初始化。"
    exit 0
fi

# 创建agent目录
mkdir -p "$AGENT_DIR"

# 辅助函数：从文件提取字段
extract_field() {
    local file="$1"
    local field="$2"
    if [ -f "$file" ]; then
        grep -iE "^[[:space:]]*-\s+\*\*${field}\*\*[[:space:]]*:[[:space:]]*(.+)$" "$file" 2>/dev/null | sed 's/.*:[[:space:]]*//' | head -1 && return
        grep -iE "^[[:space:]]*-\s+\*\*${field}:\*\*(.+)$" "$file" 2>/dev/null | sed 's/.*\*\*[[:space:]]*//' | head -1 && return
        grep -iE "^[[:space:]]*-\s+\*\*${field}\*\*[[:space:]]+(.+)$" "$file" 2>/dev/null | sed 's/.*[[:space:]]*//' | head -1 && return
        grep -iE "^[[:space:]]*-\s+${field}:[[:space:]]*(.+)$" "$file" 2>/dev/null | sed 's/.*:[[:space:]]*//' | head -1 && return
    fi
}

declare -A FOUND_FILES
SOURCES_FOUND=0

echo ""
echo "=== 步骤1: 检查Agent告知的工作区 ==="

# Agent告知的工作区（优先）
if [ -n "$AGENT_WORKSPACE" ]; then
    echo "使用Agent告知的工作区: $AGENT_WORKSPACE"
    for f in "$AGENT_WORKSPACE/IDENTITY.md" "$AGENT_WORKSPACE/SOUL.md" "$AGENT_WORKSPACE/AGENTS.md" "$AGENT_WORKSPACE/USER.md" "$AGENT_WORKSPACE/MEMORY.md"; do
        if [ -f "$f" ]; then
            FOUND_FILES["$f"]=1
            ((SOURCES_FOUND++))
            echo "  - 发现: $(basename $f)"
        fi
    done
else
    echo "  Agent未指定工作区"
fi

# 全局基础人格 GLOBAL.md
echo ""
echo "=== 步骤2: 检查全局基础人格 ==="

# 优先使用skill自带的模板
if [ -f "$DEFAULT_GLOBAL" ]; then
    GLOBAL_SOURCE="$DEFAULT_GLOBAL"
    echo "使用Skill默认模板: $DEFAULT_GLOBAL"
# 其次使用用户目录的
elif [ -f "$GLOBAL_PERSONA" ]; then
    GLOBAL_SOURCE="$GLOBAL_PERSONA"
    echo "使用用户配置: $GLOBAL_PERSONA"
else
    GLOBAL_SOURCE=""
    echo "未找到全局基础人格，将使用默认值"
fi

if [ -n "$GLOBAL_SOURCE" ]; then
    FOUND_FILES["GLOBAL.md"]=1
    ((SOURCES_FOUND++))
fi

# Agent本地配置文件
echo ""
echo "=== 步骤3: 检查Agent本地配置 ==="
for f in "$AGENTS_ROOT/IDENTITY.md" "$AGENTS_ROOT/SOUL.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["$f"]=1
        ((SOURCES_FOUND++))
        echo "  - 发现: $(basename $f) in $AGENTS_ROOT"
    fi
done

[ -f "$AGENTS_ROOT/USER.md" ] && FOUND_FILES["USER.md"]=1 && ((SOURCES_FOUND++))
[ -f "$AGENTS_ROOT/AGENTS.md" ] && FOUND_FILES["AGENTS.md"]=1 && ((SOURCES_FOUND++))

# 输出找到的源文件
if [ $SOURCES_FOUND -gt 0 ]; then
    echo ""
    echo "找到 $SOURCES_FOUND 个源文件"
fi

# 提取配置
IDENTITY_NAME=""
IDENTITY_NATURE=""
GLOBAL_DECISION=""
GLOBAL_SELF_PERCEPTION=""

# 从Agent告知的工作区提取
if [ -n "$AGENT_WORKSPACE" ]; then
    if [ -f "$AGENT_WORKSPACE/IDENTITY.md" ]; then
        IDENTITY_NAME=$(extract_field "$AGENT_WORKSPACE/IDENTITY.md" "Name")
        IDENTITY_NATURE=$(extract_field "$AGENT_WORKSPACE/IDENTITY.md" "Creature")
        echo "  - 从工作区提取: $IDENTITY_NAME"
    fi
fi

# 从本地配置提取
if [ -z "$IDENTITY_NAME" ] && [ -f "$AGENTS_ROOT/IDENTITY.md" ]; then
    IDENTITY_NAME=$(extract_field "$AGENTS_ROOT/IDENTITY.md" "Name")
    IDENTITY_NATURE=$(extract_field "$AGENTS_ROOT/IDENTITY.md" "Creature")
    echo "  - 从本地提取: $IDENTITY_NAME"
fi

# 从GLOBAL提取
if [ -n "$GLOBAL_SOURCE" ]; then
    GLOBAL_DECISION=$(extract_field "$GLOBAL_SOURCE" "决策倾向")
    GLOBAL_SELF_PERCEPTION=$(extract_field "$GLOBAL_SOURCE" "自我认知")
fi

# 默认值
IDENTITY_NAME="${IDENTITY_NAME:-AI助手}"
IDENTITY_NATURE="${IDENTITY_NATURE:-AI Agent}"
GLOBAL_DECISION="${GLOBAL_DECISION:-balanced}"
GLOBAL_SELF_PERCEPTION="${GLOBAL_SELF_PERCEPTION:-confident}"

# 生成文件
echo ""
echo "生成认知文件..."

cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

_从Agent配置初始化_

---

## 基础设定

- **身份定位**: $IDENTITY_NAME
- **本质**: $IDENTITY_NATURE
- **来源**: Agent告知的工作区

---

## 初始化时间

- $(date)
EOF

cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - 天赋认知 ($AGENT_NAME)

_从交互中逐渐形成的倾向和性格特征_

---

## 性格特征

- **决策倾向**: $GLOBAL_DECISION
- **自我认知**: $GLOBAL_SELF_PERCEPTION

---

## 情绪特征

- **当前状态**: 平静 [😌]

---

## 形成记录

_初始化时从配置推断，随着交互会逐渐调整_
EOF

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

## 初始化

- $(date)
EOF

echo ""
echo "=========================================="
echo "  初始化完成!"
echo "=========================================="
echo ""
echo "Agent: $AGENT_NAME"
echo "位置: $AGENT_DIR/"
echo "创建: INNATE.md, ACQUIRED.md, LEARNED.md"
