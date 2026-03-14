# auto-init-cognition.ps1
# 自动初始化认知文件 (PowerShell版本)
# 优先级：1) 指定agent目录 2) 常见配置文件 3) 默认生成

param(
    [string]$AgentName = "default"
)

$AGENTS_DIR = "$env:USERPROFILE\.agents"
$AGENTS_DATA_DIR = "$AGENTS_DIR\agents"
$OPENCLAW_DIR = "$env:USERPROFILE\.openclaw\workspace"

$AGENT_DIR = "$AGENTS_DATA_DIR\$AgentName"

Write-Host "Auto-initializing cognition files for agent: $AgentName..."

# 检查是否有指定agent的独立目录
if ((Test-Path $AGENT_DIR) -and (Test-Path "$AGENT_DIR\INNATE.md")) {
    Write-Host "Agent '$AgentName' already has cognition files. Skipping."
    exit 0
}

# 创建agent目录
New-Item -ItemType Directory -Force -Path $AGENT_DIR | Out-Null

# 辅助函数：从文件提取字段
function Extract-Field {
    param($File, $Field)
    if (Test-Path $File) {
        $content = Get-Content $File -Raw
        if ($content -match "(?i)^\s*\*\s*$Field\s*:\s*(.+)$") {
            return $Matches[1].Trim()
        }
    }
    return ""
}

# 辅助函数：检查文件存在
function Test-FileExists {
    param([string[]]$Paths)
    foreach ($p in $Paths) {
        if (Test-Path $p) { return $p }
    }
    return $null
}

# === 扫描所有常见配置文件 ===
$FoundFiles = @{}
$SourcesFound = 0

# OpenClaw 文件
$pathsToCheck = @(
    "$AGENTS_DIR\IDENTITY.md",
    "$AGENTS_DIR\SOUL.md", 
    "$OPENCLAW_DIR\IDENTITY.md",
    "$OPENCLAW_DIR\SOUL.md"
)
foreach ($p in $pathsToCheck) {
    if (Test-Path $p) {
        $FoundFiles[$p] = $true
        $SourcesFound++
    }
}

# AGENTS.md
if (Test-Path "$AGENTS_DIR\AGENTS.md" -or Test-Path "$OPENCLAW_DIR\AGENTS.md") {
    $FoundFiles["AGENTS.md"] = $true
    $SourcesFound++
}

# USER.md
if (Test-Path "$AGENTS_DIR\USER.md" -or Test-Path "$OPENCLAW_DIR\USER.md") {
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
    Write-Host "Found $SourcesFound source file(s):"
    foreach ($f in $FoundFiles.Keys) {
        Write-Host "  - $f"
    }
    Write-Host ""
}

# === 根据找到的文件提取信息 ===
$IDENTITY_NAME = ""
$IDENTITY_NATURE = ""
$SOUL_CORE = ""
$SOUL_TRUTHS = ""
$SOUL_VIBE = ""
$AGENTS_CONTENT = ""

# 提取 IDENTITY.md
$pathsToCheck = @("$AGENTS_DIR\IDENTITY.md", "$OPENCLAW_DIR\IDENTITY.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $IDENTITY_NAME = Extract-Field $found "Name"
    $IDENTITY_NATURE = Extract-Field $found "Nature"
    Write-Host "  - Extracted from IDENTITY.md: $IDENTITY_NAME"
}

# 提取 SOUL.md
$pathsToCheck = @("$AGENTS_DIR\SOUL.md", "$OPENCLAW_DIR\SOUL.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $SOUL_CORE = Extract-Field $found "Core Identity"
    $SOUL_TRUTHS = Extract-Field $found "Core Truths"
    $SOUL_VIBE = Extract-Field $found "Vibe"
    Write-Host "  - Extracted from SOUL.md: $SOUL_CORE"
}

# 提取 AGENTS.md
$pathsToCheck = @("$AGENTS_DIR\AGENTS.md", "$OPENCLAW_DIR\AGENTS.md")
$found = Test-FileExists $pathsToCheck
if ($found) {
    $AGENTS_CONTENT = Get-Content $found -Raw | Select-Object -First 500
    Write-Host "  - Found AGENTS.md"
}

# 从环境变量
if ($env:AGENT_ROLE -and -not $IDENTITY_NAME) {
    $IDENTITY_NAME = $env:AGENT_ROLE
    Write-Host "  - Using AGENT_ROLE: $IDENTITY_NAME"
}

# 如果找到任何源文件，使用提取的信息
if ($SourcesFound -gt 0) {
    Write-Host ""
    Write-Host "Generating cognition files from found sources..."

    # INNATE.md
    $innateContent = @"
# INNATE.md - 先天认知 ($AgentName)

_从现有配置文件自动初始化_

---

## 基础设定

- **身份定位**: $(if ($IDENTITY_NAME) { $IDENTITY_NAME } else { "AI助手" })
- **本质**: $(if ($IDENTITY_NATURE) { $IDENTITY_NATURE } else { "AI Agent" })
- **态度**: 助手

## 核心定义（来自SOUL.md）

- **核心身份**: $(if ($SOUL_CORE) { $SOUL_CORE } else { "助手" })
- **核心特质**: $(if ($SOUL_TRUTHS) { $SOUL_TRUTHS } else { "友善、乐于助人" })
- **风格**: $(if ($SOUL_VIBE) { $SOUL_VIBE } else { "专业、高效" })

---

## 检测到的配置文件

$($FoundFiles.Keys | ForEach-Object { "- $_" } | Out-String)

---

## 初始化时间

- $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

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
# ACQUIRED.md - 天赋认知

_从配置文件和交互中逐渐形成的倾向和性格特征_

---

## 性格特征

- **决策倾向**: analytical
- **自我认知**: confident
- **社交倾向**: adaptable
- **幽默感**: warm
- **道德观**: principled

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

} else {
    # === 无任何配置文件，使用默认 ===
    Write-Host "No common config files found. Using defaults..."
    Write-Host "The agent should self-update through interaction."

    # INNATE.md
    @"
# INNATE.md - 先天认知 ($AgentName)

_自动初始化，需通过交互形成自我认知_

---

## 基础设定

- **身份定位**: AI助手
- **本质**: AI Agent
- **核心特质**: 待形成

---

## 初始化时间

- $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

## 自我形成指南

本文件初始为空/最小化。Agent应通过以下方式形成自我认知：
1. 从与用户的交互中学习
2. 记录用户反馈和偏好
3. 质疑并修正自我定位

---

## 待完成

- [ ] 从交互中形成核心特质
- [ ] 明确身份定位
- [ ] 建立沟通风格
"@ | Out-File -FilePath "$AGENT_DIR\INNATE.md" -Encoding UTF8

    # ACQUIRED.md
    @"
# ACQUIRED.md - 天赋认知

_初始为空，等待通过交互形成性格特征_

---

## 性格特征

- **决策倾向**: 待形成
- **自我认知**: 待形成
- **社交倾向**: 待观察
- **幽默感**: 待发现
- **道德观**: 待形成

---

## 情绪特征

- **当前状态**: 平静 [😌]
- **情绪历史**: 空

---

## 形成记录

_Agent应通过交互逐渐形成稳定的性格特征_
"@ | Out-File -FilePath "$AGENT_DIR\ACQUIRED.md" -Encoding UTF8
}

# 生成 LEARNED.md
@"
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

- $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")

---

## 提示

Agent应在此文件中记录：
- 用户偏好和习惯
- 交互中获得的反馈
- 自我认知的修正过程
"@ | Out-File -FilePath "$AGENT_DIR\LEARNED.md" -Encoding UTF8

Write-Host ""
Write-Host "Cognition files initialized for agent: $AgentName"
Write-Host "Location: $AGENT_DIR\"
Write-Host "Created: INNATE.md, ACQUIRED.md, LEARNED.md"
