#!/bin/bash
# delete-agent-cognition.sh
# 删除指定Agent的认知文件

AGENTS_DATA_DIR="$HOME/.agents/agents"

# 获取agent名称
AGENT_NAME="$1"

if [ -z "$AGENT_NAME" ]; then
    echo "Usage: $0 <agent_name>"
    echo "Example: $0 researcher"
    echo ""
    echo "Available agents:"
    if [ -d "$AGENTS_DATA_DIR" ]; then
        ls -1 "$AGENTS_DATA_DIR" 2>/dev/null || echo "  (none)"
    else
        echo "  (no agents directory)"
    fi
    exit 1
fi

AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

if [ ! -d "$AGENT_DIR" ]; then
    echo "Error: Agent '$AGENT_NAME' not found"
    exit 1
fi

echo "Deleting cognition files for agent: $AGENT_NAME..."
rm -rf "$AGENT_DIR"

echo "Deleted: $AGENT_DIR"

# 如果目录为空，删除agents目录
if [ -d "$AGENTS_DATA_DIR" ] && [ -z "$(ls -A "$AGENTS_DATA_DIR" 2>/dev/null)" ]; then
    rmdir "$AGENTS_DATA_DIR"
    echo "Removed empty agents directory"
fi

echo "Done."
