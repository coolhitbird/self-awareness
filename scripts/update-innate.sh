#!/bin/bash
# update-innate.sh
# 更新指定Agent的INNATE.md中的特定字段

AGENTS_DIR="$HOME/.agents"
AGENTS_DATA_DIR="$AGENTS_DIR/agents"

AGENT_NAME="${2:-default}"
INNATE_FILE="$AGENTS_DATA_DIR/$AGENT_NAME/INNATE.md"

if [ ! -f "$INNATE_FILE" ]; then
    echo "Error: INNATE.md not found for agent '$AGENT_NAME'. Run init-agent-cognition.sh first."
    exit 1
fi

FIELD="$1"
VALUE="$3"

if [ -z "$FIELD" ] || [ -z "$VALUE" ]; then
    echo "Usage: update-innate.sh <field> <agent_name> <value>"
    echo "Example: update-innate.sh identity researcher 'Researcher + Life Advisor'"
    echo ""
    echo "Or use default agent:"
    echo "Example: update-innate.sh identity default 'New Identity'"
    exit 1
fi

# 记录更新历史
echo "" >> "$INNATE_FILE"
echo "---" >> "$INNATE_FILE"
echo "## 更新记录" >> "$INNATE_FILE"
echo "- $(date): $FIELD 更新为 '$VALUE'" >> "$INNATE_FILE"

echo "Updated INNATE.md for agent '$AGENT_NAME': $FIELD = $VALUE"
