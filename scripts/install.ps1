# install.ps1
# Skill 安装脚本 - Windows PowerShell版本

param(
    [switch]$SkipInit
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Self-Awareness Skill 安装脚本" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# 检测操作系统
$IsWindows = $PSVersionTable.Platform -eq "Win32NT" -or $null -ne (Get-Command winver -ErrorAction SilentlyContinue)
Write-Host "检测到操作系统: Windows" 
Write-Host ""

# 检查 PowerShell 版本
$psVersion = $PSVersionTable.PSVersion.Major
Write-Host "PowerShell 版本: $psVersion"

if ($psVersion -lt 5) {
    Write-Host "警告: 建议使用 PowerShell 5.0 或更高版本" -ForegroundColor Yellow
}
Write-Host ""

# 检查必要工具
Write-Host "检查依赖..." -ForegroundColor Cyan

# 检查是否在 Git Bash 或 WSL 中
$IsGitBash = $env:MSYSTEM -ne $null

if ($IsGitBash) {
    Write-Host "✓ 检测到 Git Bash 环境" -ForegroundColor Green
}

# 检查 OpenClaw
$OpenClawPath = "$env:USERPROFILE\.openclaw\workspace"
if (Test-Path $OpenClawPath) {
    Write-Host "✓ 检测到 OpenClaw 工作区" -ForegroundColor Green
}

# 检查 Claude
$ClaudePath = "$env:USERPROFILE\.claude"
if (Test-Path $ClaudePath) {
    Write-Host "✓ 检测到 Claude 配置" -ForegroundColor Green
}

# 检查 .agents
$AgentsPath = "$env:USERPROFILE\.agents"
if (-not (Test-Path $AgentsPath)) {
    New-Item -ItemType Directory -Force -Path $AgentsPath | Out-Null
}
if (-not (Test-Path "$AgentsPath\agents")) {
    New-Item -ItemType Directory -Force -Path "$AgentsPath\agents" | Out-Null
}
Write-Host "✓ .agents 目录已创建" -ForegroundColor Green
Write-Host ""

# 运行初始化
function Run-Initialization {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  初始化认知文件" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $InitScript = "$ScriptDir\auto-init-cognition.ps1"
    if (Test-Path $InitScript) {
        & $InitScript -AgentName "default"
    } else {
        Write-Host "错误: 找不到初始化脚本" -ForegroundColor Red
    }
}

# 询问是否初始化
if ($SkipInit) {
    Write-Host "跳过初始化 (--SkipInit)" -ForegroundColor Yellow
} else {
    $response = Read-Host "是否立即初始化认知文件? [Y/n]"
    if ($response -eq "" -or $response -eq "y" -or $response -eq "Y") {
        Run-Initialization
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  安装完成!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "下一步:" -ForegroundColor Cyan
Write-Host "  1. 在 Agent 的 system prompt 中引入 skill"
Write-Host "  2. 认知文件位于: ~/.agents/agents/<agent_name>/"
Write-Host ""
Write-Host "使用帮助:" -ForegroundColor Cyan
Write-Host "  - 查看 README.md 了解完整功能"
Write-Host "  - 查看 SKILL.md 了解技术细节"
Write-Host ""
