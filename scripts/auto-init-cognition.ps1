# auto-init-cognition.ps1
# 自动初始化认知文件 (PowerShell版本)
#
# 核心设计：Agent告诉Skill自己的配置在哪里
#
# 使用方式：
#   .\auto-init-cognition.ps1 -AgentName "myagent" -AgentWorkspace "C:\path\to\workspace"
#
# 环境变量（Agent可设置）：
#   - AGENT_WORKSPACE_<name>: Agent告诉Skill自己的配置目录
#   - DEFAULT_AGENT: 默认Agent名称
#   - AGENTS_ROOT: Agent配置文件根目录

param(
    [string]$AgentName = "default",
    [string]$AgentWorkspace = ""
)

# 核心设计：Agent告诉Skill自己的配置目录
$AGENTS_ROOT = if ($env:AGENTS_ROOT) { $env:AGENTS_ROOT } else { "$env:USERPROFILE\.agents" }
$AGENTS_DATA_DIR = "$AGENTS_ROOT\agents"
$GLOBAL_PERSONA = "$AGENTS_ROOT\GLOBAL.md"

# skill目录（用于获取默认模板）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$DEFAULT_GLOBAL = "$SkillDir\data\GLOBAL.md"

# Agent告诉Skill自己的配置目录（参数优先，否则检查环境变量）
$envVarName = "AGENT_WORKSPACE_$AgentName"
if ([string]::IsNullOrEmpty($AgentWorkspace) -and $env:$envVarName) {
    $AgentWorkspace = $env:$envVarName
}
$AgentWorkspace = $AgentWorkspace -replace '\\', '/'

$AGENT_DIR = "$AGENTS_DATA_DIR\$AgentName"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Self-Awareness 认知文件初始化" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agent: $AgentName" -ForegroundColor Cyan
Write-Host "Agent工作区: $AgentWorkspace" -ForegroundColor Cyan

# 检查是否有指定agent的独立目录
if ((Test-Path $AGENT_DIR) -and (Test-Path "$AGENT_DIR\INNATE.md")) {
    Write-Host "Agent '$AgentName' 已存在认知文件，跳过初始化。" -ForegroundColor Yellow
    exit 0
}

# 创建agent目录
New-Item -ItemType Directory -Force -Path $AGENT_DIR | Out-Null

# 辅助函数：从文件提取字段
function Extract-Field {
    param($File, $Field)
    if (Test-Path $File) {
        $content = Get-Content $File -Raw -Encoding UTF8
        
        if ($content -match "(?i)^\s*-\s*\*\*${Field}\*\*\s*:\s*(.+)$") {
            return $Matches[1].Trim()
        }
        if ($content -match "(?i)^\s*-\s*\*\*${Field}:\*\*(.+)$") {
            return $Matches[1].Trim()
        }
        if ($content -match "(?i)^\s*-\s*\*\*${Field}\*\*\s+(.+)$") {
            return $Matches[1].Trim()
        }
        if ($content -match "(?i)^\s*-\s*${Field}\s*:\s*(.+)$") {
            return $Matches[1].Trim()
        }
    }
    return ""
}

$FoundFiles = @{}
$SourcesFound = 0

# 步骤1: Agent告知的工作区
Write-Host ""
Write-Host "=== 步骤1: 检查Agent告知的工作区 ===" -ForegroundColor Green

if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    Write-Host "使用Agent告知的工作区: $AgentWorkspace" -ForegroundColor Cyan
    
    $workspaceFiles = @(
        "$AgentWorkspace/IDENTITY.md",
        "$AgentWorkspace/SOUL.md",
        "$AgentWorkspace/AGENTS.md",
        "$AgentWorkspace/USER.md",
        "$AgentWorkspace/MEMORY.md"
    )
    foreach ($f in $workspaceFiles) {
        if (Test-Path $f) {
            $FoundFiles[$f] = $true
            $SourcesFound++
            Write-Host "  - 发现: $([System.IO.Path]::GetFileName($f))" -ForegroundColor Green
        }
    }
} else {
    Write-Host "  Agent未指定工作区" -ForegroundColor Yellow
}

# 步骤2: 全局基础人格
Write-Host ""
Write-Host "=== 步骤2: 检查全局基础人格 ===" -ForegroundColor Green

# 优先使用skill自带的模板
$GLOBAL_SOURCE = ""
if (Test-Path $DEFAULT_GLOBAL) {
    $GLOBAL_SOURCE = $DEFAULT_GLOBAL
    Write-Host "使用Skill默认模板: $DEFAULT_GLOBAL" -ForegroundColor Green
} elseif (Test-Path $GLOBAL_PERSONA) {
    $GLOBAL_SOURCE = $GLOBAL_PERSONA
    Write-Host "使用用户配置: $GLOBAL_PERSONA" -ForegroundColor Green
} else {
    Write-Host "未找到全局基础人格，将使用默认值" -ForegroundColor Yellow
}

if ($GLOBAL_SOURCE) {
    $FoundFiles[$GLOBAL_SOURCE] = $true
    $SourcesFound++
}

# 步骤3: Agent本地配置
Write-Host ""
Write-Host "=== 步骤3: 检查Agent本地配置 ===" -ForegroundColor Green

foreach ($file in @("IDENTITY.md", "SOUL.md", "AGENTS.md", "USER.md")) {
    $path = "$AGENTS_ROOT\$file"
    if (Test-Path $path) {
        $FoundFiles[$path] = $true
        $SourcesFound++
        Write-Host "  - 发现: $file in $AGENTS_ROOT" -ForegroundColor Green
    }
}

# 输出找到的源文件
if ($SourcesFound -gt 0) {
    Write-Host ""
    Write-Host "找到 $SourcesFound 个源文件" -ForegroundColor Cyan
}

# 提取配置
$IDENTITY_NAME = ""
$IDENTITY_NATURE = ""
$SOUL_CORE = ""
$GLOBAL_DECISION = ""
$GLOBAL_SELF_PERCEPTION = ""

# 从Agent告知的工作区提取
if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    $workspaceId = "$AgentWorkspace/IDENTITY.md"
    if (Test-Path $workspaceId) {
        $IDENTITY_NAME = Extract-Field $workspaceId "Name"
        $IDENTITY_NATURE = Extract-Field $workspaceId "Creature"
        Write-Host "  - 从工作区提取: $IDENTITY_NAME" -ForegroundColor Green
    }
}

# 从本地配置提取
if ([string]::IsNullOrEmpty($IDENTITY_NAME)) {
    $localId = "$AGENTS_ROOT\IDENTITY.md"
    if (Test-Path $localId) {
        $IDENTITY_NAME = Extract-Field $localId "Name"
        $IDENTITY_NATURE = Extract-Field $localId "Creature"
        Write-Host "  - 从本地提取: $IDENTITY_NAME" -ForegroundColor Green
    }
}

# 从GLOBAL提取
if ($GLOBAL_SOURCE) {
    $GLOBAL_DECISION = Extract-Field $GLOBAL_SOURCE "决策倾向"
    $GLOBAL_SELF_PERCEPTION = Extract-Field $GLOBAL_SOURCE "自我认知"
}

# 默认值
if ([string]::IsNullOrEmpty($IDENTITY_NAME)) { $IDENTITY_NAME = "AI助手" }
if ([string]::IsNullOrEmpty($IDENTITY_NATURE)) { $IDENTITY_NATURE = "AI Agent" }
if ([string]::IsNullOrEmpty($GLOBAL_DECISION)) { $GLOBAL_DECISION = "balanced" }
if ([string]::IsNullOrEmpty($GLOBAL_SELF_PERCEPTION)) { $GLOBAL_SELF_PERCEPTION = "confident" }

# 生成文件
Write-Host ""
Write-Host "生成认知文件..." -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# INNATE.md
$innateContent = @"
# INNATE.md - 先天认知 ($AgentName)

_从Agent配置初始化_

---

## 基础设定

- **身份定位**: $IDENTITY_NAME
- **本质**: $IDENTITY_NATURE
- **来源**: Agent告知的工作区

---

## 初始化时间

- $timestamp

## 检测到的配置文件

$($FoundFiles.Keys | ForEach-Object { "- $_" } | Out-String)
"@

$innateContent | Out-File -FilePath "$AGENT_DIR\INNATE.md" -Encoding UTF8

# ACQUIRED.md
$acquiredContent = @"
# ACQUIRED.md - 天赋认知 ($AgentName)

_从交互中逐渐形成的倾向和性格特征_

---

## 性格特征

- **决策倾向**: $GLOBAL_DECISION
- **自我认知**: $GLOBAL_SELF_PERCEPTION

---

## 情绪特征

- **当前状态**: 平静 [😌]

---

## 形成记录

_初始化时从配置推断，随着交互会逐渐调整_
"@

$acquiredContent | Out-File -FilePath "$AGENT_DIR\ACQUIRED.md" -Encoding UTF8

# LEARNED.md
$learnedContent = @"
# LEARNED.md - 后天认知 ($AgentName)

_从交互中学习到的经验、偏好和调整_

---

## 交互记忆

_暂无记录_

---

## 用户反馈

_暂无反馈_

---

## 初始化

- $timestamp
"@

$learnedContent | Out-File -FilePath "$AGENT_DIR\LEARNED.md" -Encoding UTF8

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  初始化完成!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Agent: $AgentName" -ForegroundColor Cyan
Write-Host "位置: $AGENT_DIR" -ForegroundColor Cyan
Write-Host "创建: INNATE.md, ACQUIRED.md, LEARNED.md" -ForegroundColor Cyan
