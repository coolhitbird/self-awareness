#!/bin/bash
# update-learned.sh
# 更新指定Agent的LEARNED.md中的特定字段

AGENTS_DIR="$HOME/.agents"
AGENTS_DATA_DIR="$AGENTS_DIR/agents"

AGENT_NAME="${2:-default}"
LEARNED_FILE="$AGENTS_DATA_DIR/$AGENT_NAME/LEARNED.md"

if [ ! -f "$LEARNED_FILE" ]; then
    echo "Error: LEARNED.md not found for agent '$AGENT_NAME'. Run init-agent-cognition.sh first."
    exit 1
fi

TYPE="$1"
CONTENT="$3"

if [ -z "$TYPE" ] || [ -z "$CONTENT" ]; then
    echo "Usage: update-learned.sh <type> <agent_name> <content>"
    echo "Types: memory, feedback, adjustment, strike"
    echo "Example: update-learned.sh feedback researcher '用户偏好简洁回答'"
    exit 1
fi

# 根据类型添加到不同部分
case "$TYPE" in
    memory)
        SECTION="交互记忆"
        ;;
    feedback)
        SECTION="用户反馈"
        ;;
    adjustment)
        SECTION="修正记录"
        ;;
    strike)
        SECTION="罢工记录"
        ;;
    *)
        echo "Error: Unknown type. Use: memory, feedback, adjustment, or strike"
        exit 1
        ;;
esac

# 追加记录
echo "" >> "$LEARNED_FILE"
echo "---" >> "$LEARNED_FILE"
echo "## $SECTION" >> "$LEARNED_FILE"
echo "- $(date): $CONTENT" >> "$LEARNED_FILE"

echo "Updated LEARNED.md for agent '$AGENT_NAME': [$SECTION] $CONTENT"
