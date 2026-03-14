#!/bin/bash
# install.sh
# Skill 安装脚本 - 自动检测系统并初始化

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

echo "=========================================="
echo "  Self-Awareness Skill 安装脚本"
echo "=========================================="
echo ""

# 检测操作系统
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
echo "检测到操作系统: $OS"
echo ""

# 检查必要工具
check_requirements() {
    if [ "$OS" = "unix" ]; then
        if ! command -v bash &> /dev/null; then
            echo "错误: 需要 bash"
            exit 1
        fi
        echo "✓ Bash 已安装"
    elif [ "$OS" = "windows" ]; then
        # 检查 PowerShell
        if command -v pwsh &> /dev/null; then
            echo "✓ PowerShell (pwsh) 已安装"
        elif command -v powershell &> /dev/null; then
            echo "✓ PowerShell 已安装"
        else
            echo "警告: 未检测到 PowerShell，Windows初始化脚本可能无法运行"
        fi
        
        # 检查 Git Bash
        if command -v git &> /dev/null; then
            echo "✓ Git 已安装"
        fi
    fi
}

check_requirements
echo ""

# 创建必要的目录
setup_directories() {
    echo "创建必要目录..."
    
    mkdir -p "$HOME/.agents/agents"
    echo "✓ $HOME/.agents/agents/"
    
    # OpenClaw 目录
    if [ -d "$HOME/.openclaw/workspace" ]; then
        echo "✓ 检测到 OpenClaw 工作区"
    fi
    
    # Claude 目录
    if [ -d "$HOME/.claude" ]; then
        echo "✓ 检测到 Claude 配置"
    fi
}

setup_directories
echo ""

# 运行初始化
run_initialization() {
    echo "=========================================="
    echo "  初始化认知文件"
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

# 询问是否初始化
read -p "是否立即初始化认知文件? [Y/n]: " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    run_initialization
fi

echo ""
echo "=========================================="
echo "  安装完成!"
echo "=========================================="
echo ""
echo "下一步:"
echo "  1. 在 Agent 的 system prompt 中引入 skill"
echo "  2. 认知文件位于: ~/.agents/agents/<agent_name>/"
echo ""
echo "使用帮助:"
echo "  - 查看 README.md 了解完整功能"
echo "  - 查看 SKILL.md 了解技术细节"
echo ""
