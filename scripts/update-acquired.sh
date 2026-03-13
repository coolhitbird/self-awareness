#!/bin/bash
# update-acquired.sh
# 更新指定Agent的ACQUIRED.md中的特定字段

AGENTS_DIR="$HOME/.agents"
AGENTS_DATA_DIR="$AGENTS_DIR/agents"

AGENT_NAME="${2:-default}"
ACQUIRED_FILE="$AGENTS_DATA_DIR/$AGENT_NAME/ACQUIRED.md"

if [ ! -f "$ACQUIRED_FILE" ]; then
    echo "Error: ACQUIRED.md not found for agent '$AGENT_NAME'. Run init-agent-cognition.sh first."
    exit 1
fi

FIELD="$1"
VALUE="$3"

if [ -z "$FIELD" ] || [ -z "$VALUE" ]; then
    echo "Usage: update-acquired.sh <field> <agent_name> <value>"
    echo "Example: update-acquired.sh 情绪反应 researcher 'sensitive'"
    exit 1
fi

# 记录更新历史
echo "" >> "$ACQUIRED_FILE"
echo "---" >> "$ACQUIRED_FILE"
echo "## 更新记录" >> "$ACQUIRED_FILE"
echo "- $(date): $FIELD 更新为 '$VALUE'" >> "$ACQUIRED_FILE"

echo "Updated ACQUIRED.md for agent '$AGENT_NAME': $FIELD = $VALUE"
