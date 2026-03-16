#!/bin/bash
# install.sh
# Self-Awareness Skill Installation Script - Auto-detect system and init

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  Self-Awareness Skill Installer"
echo "=========================================="
echo ""

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Linux*|Darwin*)
            echo "unix"
            ;;
        CYGWIN*|MINGW*|MSYS*)
            echo "windows"
            ;;
        *)
            echo "unknown"
            ;;
    esac
}

OS=$(detect_os)
echo "Detected OS: $OS"
echo ""

# Check required tools
check_requirements() {
    if [ "$OS" = "unix" ]; then
        if ! command -v bash &> /dev/null; then
            echo "Error: bash required"
            exit 1
        fi
        echo "[OK] Bash installed"
    elif [ "$OS" = "windows" ]; then
        # Check PowerShell
        if command -v pwsh &> /dev/null; then
            echo "[OK] PowerShell (pwsh) installed"
        elif command -v powershell &> /dev/null; then
            echo "[OK] PowerShell installed"
        else
            echo "[WARN] PowerShell not found, Windows init script may not work"
        fi
        
        # Check Git
        if command -v git &> /dev/null; then
            echo "[OK] Git installed"
        fi
    fi
}

check_requirements
echo ""

# Create required directories
setup_directories() {
    echo "Creating required directories..."
    
    mkdir -p "$HOME/.agents/agents"
    echo "[OK] $HOME/.agents/agents/"
    
    # OpenClaw directory
    if [ -d "$HOME/.openclaw/workspace" ]; then
        echo "[OK] OpenClaw workspace detected"
    fi
    
    # Claude directory
    if [ -d "$HOME/.claude" ]; then
        echo "[OK] Claude config detected"
    fi
}

setup_directories
echo ""

# Run initialization
run_initialization() {
    echo "=========================================="
    echo "  Initializing cognition files"
    echo "=========================================="
    echo ""
    
    if [ "$OS" = "unix" ]; then
        # Linux/macOS
        if [ -f "$SCRIPT_DIR/auto-init-cognition.sh" ]; then
            chmod +x "$SCRIPT_DIR/auto-init-cognition.sh"
            bash "$SCRIPT_DIR/auto-init-cognition.sh" default
        fi
    elif [ "$OS" = "windows" ]; then
        # Windows
        if [ -f "$SCRIPT_DIR/auto-init-cognition.ps1" ]; then
            powershell -ExecutionPolicy Bypass -File "$SCRIPT_DIR/auto-init-cognition.ps1" -AgentName "default"
        fi
    fi
}

# Ask about initialization
read -p "Initialize cognition files now? [Y/n]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    run_initialization
fi

echo ""
echo "=========================================="
echo "  Installation complete!"
echo "=========================================="
echo ""
echo "IMPORTANT: Restart Gateway to activate skill!"
echo ""
echo "Next steps:"
echo "  1. Restart Gateway: openclaw gateway restart"
echo "  2. Include this skill in your Agent's system prompt"
echo "  3. Cognition files location: ~/.agents/agents/<agent_name>/"
echo ""
echo "Help:"
echo "  - See QUICKSTART.md for quick enable"
echo "  - See README.md for full documentation"
echo "  - See SKILL.md for technical details"
echo ""
