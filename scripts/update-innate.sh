#!/bin/bash
# update-innate.sh
# 更新INNATE.md中的特定字段

AGENTS_DIR="$HOME/.agents"
INNATE_FILE="$AGENTS_DIR/INNATE.md"

if [ ! -f "$INNATE_FILE" ]; then
    echo "Error: INNATE.md not found. Run init-cognition-files.sh first."
    exit 1
fi

FIELD="$1"
VALUE="$2"

if [ -z "$FIELD" ] || [ -z "$VALUE" ]; then
    echo "Usage: update-innate.sh <field> <value>"
    echo "Example: update-innate.sh identity 'Researcher + Life Advisor'"
    exit 1
fi

# 记录更新历史
echo "" >> "$INNATE_FILE"
echo "---" >> "$INNATE_FILE"
echo "## 更新记录" >> "$INNATE_FILE"
echo "- $(date): $FIELD 更新为 '$VALUE'" >> "$INNATE_FILE"

echo "Updated INNATE.md: $FIELD = $VALUE"
