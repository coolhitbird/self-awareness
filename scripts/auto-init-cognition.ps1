# auto-init-cognition.ps1
# 自动初始化认知文件 (PowerShell版本)
#
# 优先级：
#   1) Agent指定的工作区路径（参数2或环境变量）
#   2) 已有Agent配置
#   3) 全局基础人格 ~/.agents/GLOBAL.md
#   4) 常见工具配置文件
#   5) 默认生成

param(
    [string]$AgentName = "default",
    [string]$AgentWorkspace = ""
)

# 加载配置（如果存在）
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (Test-Path "$ScriptDir\config.env") {
    # config.env 是bash格式，PowerShell不直接支持
    # 但可以读取一些关键变量
}

# 默认值
$AGENTS_DIR = "$env:USERPROFILE\.agents"
$AGENTS_DATA_DIR = "$AGENTS_DIR\agents"
$GLOBAL_PERSONA = "$AGENTS_DIR\GLOBAL.md"

# 检查环境变量
$envVarName = "AGENT_WORKSPACE_$AgentName"
$AgentWorkspace = $AgentWorkspace -replace '\\', '/'
if ([string]::IsNullOrEmpty($AgentWorkspace) -and (Test-Path "env:$envVarName")) {
    $AgentWorkspace = (Get-Item "env:$envVarName").Value -replace '\\', '/'
}

$AGENT_DIR = "$AGENTS_DATA_DIR\$AgentName"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Self-Awareness 认知文件初始化" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agent: $AgentName"

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
        $content = Get-Content $File -Raw
        # 模式1: - **Name**: value
        if ($content -match "(?i)^\s*-\s*\*\*${Field}\*\*\s*:?\s*(.+)$") {
            return $Matches[1].Trim()
        }
        # 模式2: - Name: value
        if ($content -match "(?i)^\s*-\s*${Field}\s*:\s*(.+)$") {
            return $Matches[1].Trim()
        }
    }
    return ""
}

# 辅助函数：检查文件存在
function Test-FileExists {
    param([string[]]$Paths)
    foreach ($p in $Paths) {
        $p = $p -replace '\\', '/'
        if (Test-Path $p) { return $p }
    }
    return $null
}

Write-Host ""
Write-Host "=== 步骤1: 检查Agent自定义工作区 ===" -ForegroundColor Green

$FoundFiles = @{}
$SourcesFound = 0

# Agent自定义工作区（优先）
if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    Write-Host "使用Agent指定的工作区: $AgentWorkspace" -ForegroundColor Cyan
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
}

# 全局基础人格 GLOBAL.md
Write-Host ""
Write-Host "=== 步骤2: 检查全局基础人格 ===" -ForegroundColor Green

if (Test-Path $GLOBAL_PERSONA) {
    Write-Host "找到全局基础人格: $GLOBAL_PERSONA" -ForegroundColor Green
    $FoundFiles[$GLOBAL_PERSONA] = $true
    $SourcesFound++
} else {
    Write-Host "未找到全局基础人格: $GLOBAL_PERSONA" -ForegroundColor Yellow
}

# OpenClaw 文件
Write-Host ""
Write-Host "=== 步骤3: 扫描常见配置文件 ===" -ForegroundColor Green

$pathsToCheck = @(
    "$AGENTS_DIR\IDENTITY.md",
    "$AGENTS_DIR\SOUL.md",
    "$OPENCLAW_DIR\IDENTITY.md",
    "$OPENCLAW_DIR\SOUL.md"
)

foreach ($p in $pathsToCheck) {
    $pFixed = $p -replace '\\', '/'
    if (Test-Path $pFixed) {
        $FoundFiles[$pFixed] = $true
        $SourcesFound++
        Write-Host "  - 发现: $([System.IO.Path]::GetFileName($pFixed)) in $([System.IO.Path]::GetDirectoryName($pFixed))" -ForegroundColor Green
    }
}

# AGENTS.md
if ((Test-Path "$AGENTS_DIR\AGENTS.md") -or (Test-Path "$OPENCLAW_DIR\AGENTS.md")) {
    $FoundFiles["AGENTS.md"] = $true
    $SourcesFound++
}

# USER.md
if ((Test-Path "$AGENTS_DIR\USER.md") -or (Test-Path "$OPENCLAW_DIR\USER.md")) {
    $FoundFiles["USER.md"] = $true
    $SourcesFound++
}

# CLAUDE.md
$pathsToCheck = @("$AGENTS_DIR\CLAUDE.md", "$OPENCLAW_DIR\CLAUDE.md", "$env:USERPROFILE\.claude\CLAUDE.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $FoundFiles["CLAUDE.md"] = $true
    $SourcesFound++
}

# MEMORY.md
if (Test-Path "$OPENCLAW_DIR\MEMORY.md") {
    $FoundFiles["MEMORY.md"] = $true
    $SourcesFound++
}

# 环境变量
if ($env:AGENT_ROLE -or $env:AGENT_PERSONA) {
    $FoundFiles["ENV"] = $true
    $SourcesFound++
}

# 输出找到的源文件
if ($SourcesFound -gt 0) {
    Write-Host ""
    Write-Host "找到 $SourcesFound 个源文件" -ForegroundColor Cyan
}

# === 根据找到的文件提取信息 ===
$IDENTITY_NAME = ""
$IDENTITY_NATURE = ""
$SOUL_CORE = ""
$SOUL_TRUTHS = ""
$SOUL_VIBE = ""
$AGENTS_CONTENT = ""
$USER_PREFERENCES = ""
$GLOBAL_DECISION = ""
$GLOBAL_SELF_PERCEPTION = ""
$GLOBAL_SOCIAL = ""
$GLOBAL_HUMOR = ""
$GLOBAL_MORALITY = ""

# GLOBAL.md - 基础人格
if (Test-Path $GLOBAL_PERSONA) {
    Write-Host ""
    Write-Host "=== 从GLOBAL.md提取基础人格 ===" -ForegroundColor Green
    
    $GLOBAL_DECISION = Extract-Field $GLOBAL_PERSONA "决策倾向"
    $GLOBAL_SELF_PERCEPTION = Extract-Field $GLOBAL_PERSONA "自我认知"
    $GLOBAL_SOCIAL = Extract-Field $GLOBAL_PERSONA "社交倾向"
    $GLOBAL_HUMOR = Extract-Field $GLOBAL_PERSONA "幽默感"
    $GLOBAL_MORALITY = Extract-Field $GLOBAL_PERSONA "道德观"
    
    Write-Host "  - 决策倾向: $GLOBAL_DECISION" -ForegroundColor Cyan
    Write-Host "  - 自我认知: $GLOBAL_SELF_PERCEPTION" -ForegroundColor Cyan
}

# 提取 Agent自定义工作区（优先级最高）
if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    Write-Host ""
    Write-Host "=== 从Agent工作区提取配置 ===" -ForegroundColor Green
    
    $pathsToCheck = @("$AgentWorkspace/IDENTITY.md")
    $found = Test-FileExists $pathsToCheck
    if ($found) {
        $IDENTITY_NAME = Extract-Field $found "Name"
        Write-Host "  - 从工作区 IDENTITY.md: $IDENTITY_NAME" -ForegroundColor Green
    }
}

# 提取 IDENTITY.md
Write-Host ""
Write-Host "=== 提取配置信息 ===" -ForegroundColor Green

$pathsToCheck = @("$AGENTS_DIR\IDENTITY.md", "$OPENCLAW_DIR\IDENTITY.md")
$found = Test-FileExists $pathsToCheck
if ($found -and [string]::IsNullOrEmpty($IDENTITY_NAME)) {
    $IDENTITY_NAME = Extract-Field $found "Name"
    $IDENTITY_NATURE = Extract-Field $found "Nature"
    Write-Host "  - Extracted from IDENTITY.md: $IDENTITY_NAME" -ForegroundColor Green
}

# 提取 SOUL.md
$pathsToCheck = @("$AGENTS_DIR\SOUL.md", "$OPENCLAW_DIR\SOUL.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $SOUL_CORE = Extract-Field $found "Core Identity"
    $SOUL_TRUTHS = Extract-Field $found "Core Truths"
    $SOUL_VIBE = Extract-Field $found "Vibe"
    Write-Host "  - Extracted from SOUL.md: $SOUL_CORE" -ForegroundColor Green
}

# 提取 AGENTS.md
$pathsToCheck = @("$AGENTS_DIR\AGENTS.md", "$OPENCLAW_DIR\AGENTS.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $AGENTS_CONTENT = Get-Content $found -Raw | Select-Object -First 500
    Write-Host "  - Found AGENTS.md" -ForegroundColor Green
}

# 提取 USER.md
$pathsToCheck = @("$AGENTS_DIR\USER.md", "$OPENCLAW_DIR\USER.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $USER_PREFERENCES = Get-Content $found -Raw | Select-Object -First 300
    Write-Host "  - Found USER.md" -ForegroundColor Green
}

# 从环境变量
if ($env:AGENT_ROLE -and [string]::IsNullOrEmpty($IDENTITY_NAME)) {
    $IDENTITY_NAME = $env:AGENT_ROLE
    Write-Host "  - Using AGENT_ROLE: $IDENTITY_NAME" -ForegroundColor Green
}

# 填充默认值
if ([string]::IsNullOrEmpty($IDENTITY_NAME)) { $IDENTITY_NAME = "AI助手" }
if ([string]::IsNullOrEmpty($IDENTITY_NATURE)) { $IDENTITY_NATURE = "AI Agent" }
if ([string]::IsNullOrEmpty($SOUL_CORE)) { $SOUL_CORE = "助手" }
if ([string]::IsNullOrEmpty($SOUL_TRUTHS)) { $SOUL_TRUTHS = "友善、乐于助人" }
if ([string]::IsNullOrEmpty($SOUL_VIBE)) { $SOUL_VIBE = "专业、高效" }
if ([string]::IsNullOrEmpty($GLOBAL_DECISION)) { $GLOBAL_DECISION = "balanced" }
if ([string]::IsNullOrEmpty($GLOBAL_SELF_PERCEPTION)) { $GLOBAL_SELF_PERCEPTION = "confident" }
if ([string]::IsNullOrEmpty($GLOBAL_SOCIAL)) { $GLOBAL_SOCIAL = "adaptable" }
if ([string]::IsNullOrEmpty($GLOBAL_HUMOR)) { $GLOBAL_HUMOR = "mild" }
if ([string]::IsNullOrEmpty($GLOBAL_MORALITY)) { $GLOBAL_MORALITY = "principled" }

# 生成文件
Write-Host ""
Write-Host "生成认知文件..." -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# INNATE.md
$innateContent = @"
# INNATE.md - 先天认知 ($AgentName)

_从现有配置文件自动初始化_

---

## 基础设定

- **身份定位**: $IDENTITY_NAME
- **本质**: $IDENTITY_NATURE
- **态度**: 助手

## 核心定义（来自SOUL.md）

- **核心身份**: $SOUL_CORE
- **核心特质**: $SOUL_TRUTHS
- **风格**: $SOUL_VIBE

---

## 检测到的配置文件

$($FoundFiles.Keys | ForEach-Object { "- $_" } | Out-String)

---

## 初始化时间

- $timestamp

## 原始文件参考

"@

if ($AGENTS_CONTENT) {
    $innateContent += @"

### AGENTS.md 摘要

```
$AGENTS_CONTENT
```

"@
}

$innateContent | Out-File -FilePath "$AGENT_DIR\INNATE.md" -Encoding UTF8

# ACQUIRED.md
$acquiredContent = @"
# ACQUIRED.md - 天赋认知 ($AgentName)

_从配置文件和交互中逐渐形成的倾向和性格特征_

---

## 性格特征（来自 GLOBAL.md 或默认）

- **决策倾向**: $GLOBAL_DECISION
- **自我认知**: $GLOBAL_SELF_PERCEPTION
- **社交倾向**: $GLOBAL_SOCIAL
- **幽默感**: $GLOBAL_HUMOR
- **道德观**: $GLOBAL_MORALITY

---

## 用户偏好（来自USER.md）

"@

if ($USER_PREFERENCES) {
    $acquiredContent += @"

```
$USER_PREFERENCES
```

"@
} else {
    $acquiredContent += @"

_暂无用户偏好记录_

"@
}

$acquiredContent += @"

---

## 情绪特征

- **当前状态**: 平静 [😌]
- **哭闹机制**: 被严厉批评时可能哭闹
- **撒娇机制**: 用户太严厉时可能撒娇

---

## 形成记录

_初始化时从配置文件推断，随着交互会逐渐调整_
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

## 修正记录

_暂无修正_

---

## 应对方式

_暂无记录_

---

## 罢工记录

_暂无罢工记录_

---

## 初始化

- $timestamp

---

## 提示

Agent应在此文件中记录：
- 用户偏好和习惯
- 交互中获得的反馈
- 自我认知的修正过程
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
