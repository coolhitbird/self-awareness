# install.ps1
# Self-Awareness Skill Installation Script - Windows PowerShell

# Force UTF-8 output to avoid encoding issues
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

param(
    [switch]$SkipInit
)

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Self-Awareness Skill Installer" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Detect OS
$RunningOnWindows = $PSVersionTable.Platform -eq "Win32NT" -or $null -ne (Get-Command winver -ErrorAction SilentlyContinue)
Write-Host "Detected OS: $(if ($RunningOnWindows) { 'Windows' } else { 'Other' })"
Write-Host ""

# Check PowerShell version
$psVersion = $PSVersionTable.PSVersion.Major
Write-Host "PowerShell version: $psVersion"

if ($psVersion -lt 5) {
    Write-Host "Warning: PowerShell 5.0+ recommended" -ForegroundColor Yellow
}
Write-Host ""

# Check dependencies
Write-Host "Checking dependencies..." -ForegroundColor Cyan

# Check if in Git Bash or WSL
$IsGitBash = $env:MSYSTEM -ne $null

if ($IsGitBash) {
    Write-Host "[OK] Git Bash environment detected" -ForegroundColor Green
}

# Check OpenClaw
$OpenClawPath = "$env:USERPROFILE\.openclaw\workspace"
if (Test-Path $OpenClawPath) {
    Write-Host "[OK] OpenClaw workspace detected" -ForegroundColor Green
}

# Check Claude
$ClaudePath = "$env:USERPROFILE\.claude"
if (Test-Path $ClaudePath) {
    Write-Host "[OK] Claude config detected" -ForegroundColor Green
}

# Check .agents
$AgentsPath = "$env:USERPROFILE\.agents"
if (-not (Test-Path $AgentsPath)) {
    New-Item -ItemType Directory -Force -Path $AgentsPath | Out-Null
}
if (-not (Test-Path "$AgentsPath\agents")) {
    New-Item -ItemType Directory -Force -Path "$AgentsPath\agents" | Out-Null
}
Write-Host "[OK] .agents directory ready" -ForegroundColor Green
Write-Host ""

# Run initialization
function Run-Initialization {
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host "  Initializing cognition files" -ForegroundColor Cyan
    Write-Host "==========================================" -ForegroundColor Cyan
    Write-Host ""
    
    $InitScript = "$ScriptDir\auto-init-cognition.ps1"
    if (Test-Path $InitScript) {
        & $InitScript -AgentName "default"
    } else {
        Write-Host "Error: Init script not found" -ForegroundColor Red
    }
}

# Ask about initialization
if ($SkipInit) {
    Write-Host "Skipping initialization (--SkipInit)" -ForegroundColor Yellow
} else {
    $response = Read-Host "Initialize cognition files now? [Y/n]"
    if ($response -eq "" -or $response -eq "y" -or $response -eq "Y") {
        Run-Initialization
    }
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Installation complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "IMPORTANT: Restart Gateway to activate skill!" -ForegroundColor Yellow
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Restart Gateway: openclaw gateway restart"
Write-Host "  2. Include this skill in your Agent's system prompt"
Write-Host "  3. Cognition files location: ~/.agents/agents/<agent_name>/"
Write-Host ""
Write-Host "Help:" -ForegroundColor Cyan
Write-Host "  - See QUICKSTART.md for quick enable"
Write-Host "  - See README.md for full documentation"
Write-Host "  - See SKILL.md for technical details"
Write-Host ""
