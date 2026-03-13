#!/bin/bash
# init-agent-cognition.sh
# 为指定Agent初始化认知文件

AGENTS_DIR="$HOME/.agents"
AGENTS_DATA_DIR="$AGENTS_DIR/agents"

# 获取agent名称
AGENT_NAME="${1:-default}"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent_name>"
    echo "Example: $0 researcher"
    exit 1
fi

AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

echo "Initializing cognition files for agent: $AGENT_NAME..."

# 创建agent目录
mkdir -p "$AGENT_DIR"

# 检查是否有现有的identity文件
if [ -f "$AGENTS_DIR/IDENTITY.md" ]; then
    echo "Using existing identity files..."
    
    # 提取信息
    extract_field() {
        local file="$1"
        local field="$2"
        if [ -f "$file" ]; then
            grep -i "^[[:space:]]*- \*\*${field}:" "$file" 2>/dev/null | sed 's/.*: *//' | head -1
        fi
    }

    IDENTITY_NAME=$(extract_field "$AGENTS_DIR/IDENTITY.md" "Name")
    IDENTITY_NATURE=$(extract_field "$AGENTS_DIR/IDENTITY.md" "Nature")
    SOUL_CORE=$(extract_field "$AGENTS_DIR/SOUL.md" "Core Identity")
    SOUL_TRUTHS=$(extract_field "$AGENTS_DIR/SOUL.md" "Core Truths")
    SOUL_VIBE=$(extract_field "$AGENTS_DIR/SOUL.md" "Vibe")
    
    # 生成 INNATE.md
    cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

_从现有identity文件自动初始化_

---

## 基础设定

- **身份定位**: ${IDENTITY_NAME:-Researcher}
- **本质**: ${IDENTITY_NATURE:-数字情报分析师}
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

else
    # 使用默认
    cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - 先天认知 ($AGENT_NAME)

---

## 基础设定

- **身份定位**: $AGENT_NAME
- **本质**: AI Agent
- **核心特质**: 待形成

---

## 初始化时间

- $(date)
EOF
fi

# 生成 ACQUIRED.md
cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - 天赋认知 ($AGENT_NAME)

---

## 性格特征

- **决策倾向**: analytical
- **自我认知**: confident
- **社交倾向**: introverted
- **幽默感**: warm
- **道德观**: principled

---

## 情绪特征

- **基础情绪**: normal
- **哭闹机制**: 被严厉批评时可能哭闹
- **撒娇机制**: 用户太严厉时可能撒娇
- **罢工机制**: 持续负面交互时可能罢工

---

## 形成记录

_初始化于 $(date)_
EOF

# 生成 LEARNED.md
cat > "$AGENT_DIR/LEARNED.md" << EOF
# LEARNED.md - 后天认知 ($AGENT_NAME)

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
EOF

echo ""
echo "Cognition files initialized for agent: $AGENT_NAME"
echo "Location: $AGENT_DIR/"
echo "Created: INNATE.md, ACQUIRED.md, LEARNED.md"
