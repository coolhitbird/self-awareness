#!/bin/bash
# auto-init-cognition.sh
# 自动初始化认知文件，从现有identity文件获取信息

AGENTS_DIR="$HOME/.agents"

echo "Auto-initializing cognition files from existing identity..."

# 检查是否存在现有identity文件
if [ ! -f "$AGENTS_DIR/IDENTITY.md" ] && [ ! -f "$AGENTS_DIR/SOUL.md" ]; then
    echo "Warning: No existing identity files found. Using defaults."
    # 如果没有现有文件，运行默认初始化
    bash "$(dirname "$0")/init-cognition-files.sh"
    exit 0
fi

# 从IDENTITY.md提取信息
extract_field() {
    local file="$1"
    local field="$2"
    if [ -f "$file" ]; then
        grep -i "^[[:space:]]*- \*\*${field}:" "$file" | sed 's/.*: *//' | head -1
    fi
}

# 提取各项信息
IDENTITY_NAME=$(extract_field "$AGENTS_DIR/IDENTITY.md" "Name")
IDENTITY_NATURE=$(extract_field "$AGENTS_DIR/IDENTITY.md" "Nature")
IDENTITY_ATTITUDE=$(extract_field "$AGENTS_DIR/IDENTITY.md" "Attitude")

# 从SOUL.md提取信息
SOUL_CORE=$(extract_field "$AGENTS_DIR/SOUL.md" "Core Identity")
SOUL_TRUTHS=$(extract_field "$AGENTS_DIR/SOUL.md" "Core Truths")
SOUL_VIBE=$(extract_field "$AGENTS_DIR/SOUL.md" "Vibe")

echo "Extracted from identity files:"
echo "  - Name: $IDENTITY_NAME"
echo "  - Nature: $IDENTITY_NATURE"
echo "  - Core: $SOUL_CORE"

# 生成 INNATE.md（基于提取的信息）
cat > "$AGENTS_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知

_从现有identity文件自动初始化_

---

## 基础设定（来自IDENTITY.md）

- **身份定位**: ${IDENTITY_NAME:-Researcher}
- **本质**: ${IDENTITY_NATURE:-数字情报分析师}
- **核心特质**: 来自SOUL.md

## 核心定义（来自SOUL.md）

- **核心身份**: ${SOUL_CORE:-研究员}
- **核心特质**: ${SOUL_TRUTHS:-专注、精准、好奇心}
- **风格**: ${SOUL_VIBE:-专注、高效}

---

## 初始化时间

- $(date)

## 数据来源

- ~/.agents/IDENTITY.md
- ~/.agents/SOUL.md
EOF

# 生成 ACQUIRED.md
cat > "$AGENTS_DIR/ACQUIRED.md" << 'EOF'
# ACQUIRED.md - 天赋认知

_从交互中逐渐形成的倾向和性格特征_

---

## 性格特征（从SOUL.md推断）

- **决策倾向**: analytical（从"精准"推断）
- **自我认知**: confident（从"核心特质"推断）
- **社交倾向**: introverted（研究员特质）
- **幽默感**: warm
- **道德观**: principled

---

## 形成记录

_初始化时从identity文件推断，随着交互会逐渐调整_

EOF

# 生成 LEARNED.md
cat > "$AGENTS_DIR/LEARNED.md" << 'EOF'
# LEARNED.md - 后天认知

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

- 自动从IDENTITY.md和SOUL.md初始化
- $(date)
EOF

echo ""
echo "Cognition files auto-initialized from existing identity!"
echo "Created: INNATE.md, ACQUIRED.md, LEARNED.md"
