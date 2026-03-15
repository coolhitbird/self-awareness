#!/bin/bash
# auto-init-cognition.sh
# Auto-initialize cognition files
#
# Core Design: Agent tells Skill where its config is located
#
# Usage:
#   bash auto-init-cognition.sh <agent_name> [agent_workspace_dir]
#
# Environment variables (Agent can set):
#   - AGENT_WORKSPACE_<name>: Agent tells Skill its config directory
#   - DEFAULT_AGENT: Default agent name

# Agent name (param 1 or default)
AGENT_NAME="${1:-${DEFAULT_AGENT:-default}}"

# Agent tells Skill its config directory (param 2 priority, then env var)
AGENT_WORKSPACE_VAR="AGENT_WORKSPACE_${AGENT_NAME}"
AGENT_WORKSPACE="${2:-${!AGENT_WORKSPACE_VAR:-${AGENT_WORKSPACE:-}}}"

# Agent config directory
AGENTS_ROOT="${AGENTS_ROOT:-$HOME/.agents}"
AGENTS_DATA_DIR="${AGENTS_ROOT}/agents"
GLOBAL_PERSONA="${AGENTS_ROOT}/GLOBAL.md"

# Skill directory (for default templates)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
DEFAULT_GLOBAL="$SKILL_DIR/data/GLOBAL.md"
AGENT_DIR="$AGENTS_DATA_DIR/$AGENT_NAME"

echo "=========================================="
echo "  Self-Awareness Cognition File Init"
echo "=========================================="
echo ""
echo "Agent: $AGENT_NAME"
echo "Agent workspace: ${AGENT_WORKSPACE:-not specified}"

# Check if agent already has cognition files
if [ -d "$AGENT_DIR" ] && [ -f "$AGENT_DIR/INNATE.md" ]; then
    echo "Agent '$AGENT_NAME' already has cognition files, skipping."
    exit 0
fi

# Create agent directory
mkdir -p "$AGENT_DIR"

# Helper: Extract field from file
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
echo "=== Step 1: Check Agent-told workspace ==="

# Agent-told workspace (priority)
if [ -n "$AGENT_WORKSPACE" ]; then
    echo "Using Agent-told workspace: $AGENT_WORKSPACE"
    for f in "$AGENT_WORKSPACE/IDENTITY.md" "$AGENT_WORKSPACE/SOUL.md" "$AGENT_WORKSPACE/AGENTS.md" "$AGENT_WORKSPACE/USER.md" "$AGENT_WORKSPACE/MEMORY.md"; do
        if [ -f "$f" ]; then
            FOUND_FILES["$f"]=1
            ((SOURCES_FOUND++))
            echo "  - Found: $(basename $f)"
        fi
    done
else
    echo "  Agent did not specify workspace"
fi

# Global base persona GLOBAL.md
echo ""
echo "=== Step 2: Check global base persona ==="

# Prefer skill's built-in template
if [ -f "$DEFAULT_GLOBAL" ]; then
    GLOBAL_SOURCE="$DEFAULT_GLOBAL"
    echo "Using Skill default template: $DEFAULT_GLOBAL"
elif [ -f "$GLOBAL_PERSONA" ]; then
    GLOBAL_SOURCE="$GLOBAL_PERSONA"
    echo "Using user config: $GLOBAL_PERSONA"
else
    GLOBAL_SOURCE=""
    echo "No global base persona found, using defaults"
fi

if [ -n "$GLOBAL_SOURCE" ]; then
    FOUND_FILES["GLOBAL.md"]=1
    ((SOURCES_FOUND++))
fi

# Agent local config files
echo ""
echo "=== Step 3: Check Agent local config ==="
for f in "$AGENTS_ROOT/IDENTITY.md" "$AGENTS_ROOT/SOUL.md"; do
    if [ -f "$f" ]; then
        FOUND_FILES["$f"]=1
        ((SOURCES_FOUND++))
        echo "  - Found: $(basename $f) in $AGENTS_ROOT"
    fi
done

[ -f "$AGENTS_ROOT/USER.md" ] && FOUND_FILES["USER.md"]=1 && ((SOURCES_FOUND++))
[ -f "$AGENTS_ROOT/AGENTS.md" ] && FOUND_FILES["AGENTS.md"]=1 && ((SOURCES_FOUND++))

# Output found sources
if [ $SOURCES_FOUND -gt 0 ]; then
    echo ""
    echo "Found $SOURCES_FOUND source files"
fi

# Extract config
IDENTITY_NAME=""
IDENTITY_NATURE=""
GLOBAL_DECISION=""
GLOBAL_SELF_PERCEPTION=""

# Extract from Agent-told workspace
if [ -n "$AGENT_WORKSPACE" ]; then
    if [ -f "$AGENT_WORKSPACE/IDENTITY.md" ]; then
        IDENTITY_NAME=$(extract_field "$AGENT_WORKSPACE/IDENTITY.md" "Name")
        IDENTITY_NATURE=$(extract_field "$AGENT_WORKSPACE/IDENTITY.md" "Creature")
        echo "  - From workspace: $IDENTITY_NAME"
    fi
fi

# Extract from local config
if [ -z "$IDENTITY_NAME" ] && [ -f "$AGENTS_ROOT/IDENTITY.md" ]; then
    IDENTITY_NAME=$(extract_field "$AGENTS_ROOT/IDENTITY.md" "Name")
    IDENTITY_NATURE=$(extract_field "$AGENTS_ROOT/IDENTITY.md" "Creature")
    echo "  - From local: $IDENTITY_NAME"
fi

# From GLOBAL
if [ -n "$GLOBAL_SOURCE" ]; then
    GLOBAL_DECISION=$(extract_field "$GLOBAL_SOURCE" "Decision")
    GLOBAL_SELF_PERCEPTION=$(extract_field "$GLOBAL_SOURCE" "SelfPerception")
fi

# Defaults
IDENTITY_NAME="${IDENTITY_NAME:-AI Assistant}"
IDENTITY_NATURE="${IDENTITY_NATURE:-AI Agent}"
GLOBAL_DECISION="${GLOBAL_DECISION:-balanced}"
GLOBAL_SELF_PERCEPTION="${GLOBAL_SELF_PERCEPTION:-confident}"

# Generate files
echo ""
echo "Generating cognition files..."

cat > "$AGENT_DIR/INNATE.md" << EOF
# INNATE.md - Innate Cognition ($AGENT_NAME)

_Init from Agent config_

---

## Basic Settings

- **Identity**: $IDENTITY_NAME
- **Nature**: $IDENTITY_NATURE
- **Source**: Agent-told workspace

---

## Init Time

- $(date)
EOF

cat > "$AGENT_DIR/ACQUIRED.md" << EOF
# ACQUIRED.md - Acquired Cognition ($AGENT_NAME)

_Traits and characteristics formed from interactions_

---

## Personality Traits

- **Decision Style**: $GLOBAL_DECISION
- **Self Perception**: $GLOBAL_SELF_PERCEPTION

---

## Emotional Traits

- **Current State**: calm [😌]

---

## Formation Record

_Inferred from config during init, will adjust over time_
EOF

cat > "$AGENT_DIR/LEARNED.md" << EOF
# LEARNED.md - Learned Cognition ($AGENT_NAME)

_Learned experiences, preferences and adjustments from interactions_

---

## Interaction Memory

_No records yet_

---

## User Feedback

_No feedback yet_

---

## Init

- $(date)
EOF

echo ""
echo "=========================================="
echo "  Initialization complete!"
echo "=========================================="
echo ""
echo "Agent: $AGENT_NAME"
echo "Location: $AGENT_DIR/"
echo "Created: INNATE.md, ACQUIRED.md, LEARNED.md"
