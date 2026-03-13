#!/bin/bash
# update-acquired.sh
# 更新ACQUIRED.md中的特定字段

AGENTS_DIR="$HOME/.agents"
ACQUIRED_FILE="$AGENTS_DIR/ACQUIRED.md"

if [ ! -f "$ACQUIRED_FILE" ]; then
    echo "Error: ACQUIRED.md not found. Run init-cognition-files.sh first."
    exit 1
fi

FIELD="$1"
VALUE="$2"

if [ -z "$FIELD" ] || [ -z "$VALUE" ]; then
    echo "Usage: update-acquired.sh <field> <value>"
    echo "Example: update-acquired.sh decision_style 'analytical'"
    exit 1
fi

# 记录更新历史
echo "" >> "$ACQUIRED_FILE"
echo "---" >> "$ACQUIRED_FILE"
echo "## 更新记录" >> "$ACQUIRED_FILE"
echo "- $(date): $FIELD 更新为 '$VALUE'" >> "$ACQUIRED_FILE"

echo "Updated ACQUIRED.md: $FIELD = $VALUE"
