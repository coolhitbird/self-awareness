# auto-init-cognition.ps1
# Auto-initialize cognition files (PowerShell version)
#
# Core Design: Agent tells Skill where its config is located
#
# Usage:
#   .\auto-init-cognition.ps1 -AgentName "myagent" -AgentWorkspace "C:\path\to\workspace"
#
# Environment variables (Agent can set):
#   - AGENT_WORKSPACE_<name>: Agent tells Skill its config directory
#   - DEFAULT_AGENT: Default agent name
#   - AGENTS_ROOT: Agent config root directory

# Force UTF-8 output
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$PSDefaultParameterValues['Out-File:Encoding'] = 'utf8'

param(
    [string]$AgentName = "default",
    [string]$AgentWorkspace = ""
)

# Core Design: Agent tells Skill its config directory
$AGENTS_ROOT = if ($env:AGENTS_ROOT) { $env:AGENTS_ROOT } else { "$env:USERPROFILE\.agents" }
$AGENTS_DATA_DIR = "$AGENTS_ROOT\agents"
$GLOBAL_PERSONA = "$AGENTS_ROOT\GLOBAL.md"

# Skill directory (for default templates)
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$SkillDir = Split-Path -Parent $ScriptDir
$DEFAULT_GLOBAL = "$SkillDir\data\GLOBAL.md"

# Agent tells Skill its config directory (param priority, then env var)
$envVarName = "AGENT_WORKSPACE_$AgentName"
if ([string]::IsNullOrEmpty($AgentWorkspace) -and $env:$envVarName) {
    $AgentWorkspace = $env:$envVarName
}
$AgentWorkspace = $AgentWorkspace -replace '\\', '/'

$AGENT_DIR = "$AGENTS_DATA_DIR\$AgentName"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  Self-Awareness Cognition File Init" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Agent: $AgentName" -ForegroundColor Cyan
Write-Host "Agent workspace: $AgentWorkspace" -ForegroundColor Cyan

# Check if agent already has cognition files
if ((Test-Path $AGENT_DIR) -and (Test-Path "$AGENT_DIR\INNATE.md")) {
    Write-Host "Agent '$AgentName' already has cognition files, skipping." -ForegroundColor Yellow
    exit 0
}

# Create agent directory
New-Item -ItemType Directory -Force -Path $AGENT_DIR | Out-Null

# Helper: Extract field from file
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

# Step 1: Agent-told workspace
Write-Host ""
Write-Host "=== Step 1: Check Agent-told workspace ===" -ForegroundColor Green

if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    Write-Host "Using Agent-told workspace: $AgentWorkspace" -ForegroundColor Cyan
    
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
            Write-Host "  - Found: $([System.IO.Path]::GetFileName($f))" -ForegroundColor Green
        }
    }
} else {
    Write-Host "  Agent did not specify workspace" -ForegroundColor Yellow
}

# Step 2: Global base persona
Write-Host ""
Write-Host "=== Step 2: Check global base persona ===" -ForegroundColor Green

# Prefer skill's built-in template
$GLOBAL_SOURCE = ""
if (Test-Path $DEFAULT_GLOBAL) {
    $GLOBAL_SOURCE = $DEFAULT_GLOBAL
    Write-Host "Using Skill default template: $DEFAULT_GLOBAL" -ForegroundColor Green
} elseif (Test-Path $GLOBAL_PERSONA) {
    $GLOBAL_SOURCE = $GLOBAL_PERSONA
    Write-Host "Using user config: $GLOBAL_PERSONA" -ForegroundColor Green
} else {
    Write-Host "No global base persona found, using defaults" -ForegroundColor Yellow
}

if ($GLOBAL_SOURCE) {
    $FoundFiles[$GLOBAL_SOURCE] = $true
    $SourcesFound++
}

# Step 3: Agent local config
Write-Host ""
Write-Host "=== Step 3: Check Agent local config ===" -ForegroundColor Green

foreach ($file in @("IDENTITY.md", "SOUL.md", "AGENTS.md", "USER.md")) {
    $path = "$AGENTS_ROOT\$file"
    if (Test-Path $path) {
        $FoundFiles[$path] = $true
        $SourcesFound++
        Write-Host "  - Found: $file in $AGENTS_ROOT" -ForegroundColor Green
    }
}

# Output found sources
if ($SourcesFound -gt 0) {
    Write-Host ""
    Write-Host "Found $SourcesFound source files" -ForegroundColor Cyan
}

# Extract config
$IDENTITY_NAME = ""
$IDENTITY_NATURE = ""
$SOUL_CORE = ""
$GLOBAL_DECISION = ""
$GLOBAL_SELF_PERCEPTION = ""

# Extract from Agent-told workspace
if (-not [string]::IsNullOrEmpty($AgentWorkspace)) {
    $workspaceId = "$AgentWorkspace/IDENTITY.md"
    if (Test-Path $workspaceId) {
        $IDENTITY_NAME = Extract-Field $workspaceId "Name"
        $IDENTITY_NATURE = Extract-Field $workspaceId "Creature"
        Write-Host "  - From workspace: $IDENTITY_NAME" -ForegroundColor Green
    }
}

# Extract from local config
if ([string]::IsNullOrEmpty($IDENTITY_NAME)) {
    $localId = "$AGENTS_ROOT\IDENTITY.md"
    if (Test-Path $localId) {
        $IDENTITY_NAME = Extract-Field $localId "Name"
        $IDENTITY_NATURE = Extract-Field $localId "Creature"
        Write-Host "  - From local: $IDENTITY_NAME" -ForegroundColor Green
    }
}

# From GLOBAL
if ($GLOBAL_SOURCE) {
    $GLOBAL_DECISION = Extract-Field $GLOBAL_SOURCE "Decision"
    $GLOBAL_SELF_PERCEPTION = Extract-Field $GLOBAL_SOURCE "SelfPerception"
}

# Defaults
if ([string]::IsNullOrEmpty($IDENTITY_NAME)) { $IDENTITY_NAME = "AI Assistant" }
if ([string]::IsNullOrEmpty($IDENTITY_NATURE)) { $IDENTITY_NATURE = "AI Agent" }
if ([string]::IsNullOrEmpty($GLOBAL_DECISION)) { $GLOBAL_DECISION = "balanced" }
if ([string]::IsNullOrEmpty($GLOBAL_SELF_PERCEPTION)) { $GLOBAL_SELF_PERCEPTION = "confident" }

# Generate files
Write-Host ""
Write-Host "Generating cognition files..." -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# INNATE.md
$innateContent = @"
# INNATE.md - Innate Cognition ($AgentName)

_Init from Agent config_

---

## Basic Settings

- **Identity**: $IDENTITY_NAME
- **Nature**: $IDENTITY_NATURE
- **Source**: Agent-told workspace

---

## Init Time

- $timestamp

## Detected Config Files

$($FoundFiles.Keys | ForEach-Object { "- $_" } | Out-String)
"@

$innateContent | Out-File -FilePath "$AGENT_DIR\INNATE.md" -Encoding UTF8

# ACQUIRED.md
$acquiredContent = @"
# ACQUIRED.md - Acquired Cognition ($AgentName)

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
"@

$acquiredContent | Out-File -FilePath "$AGENT_DIR\ACQUIRED.md" -Encoding UTF8

# LEARNED.md
$learnedContent = @"
# LEARNED.md - Learned Cognition ($AgentName)

_Learned experiences, preferences and adjustments from interactions_

---

## Interaction Memory

_No records yet_

---

## User Feedback

_No feedback yet_

---

## Init

- $timestamp
"@

$learnedContent | Out-File -FilePath "$AGENT_DIR\LEARNED.md" -Encoding UTF8

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "  Initialization complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "Agent: $AgentName" -ForegroundColor Cyan
Write-Host "Location: $AGENT_DIR" -ForegroundColor Cyan
Write-Host "Created: INNATE.md, ACQUIRED.md, LEARNED.md" -ForegroundColor Cyan
