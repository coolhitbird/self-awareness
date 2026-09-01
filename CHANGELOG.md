# Changelog

All notable changes to this project will be documented in this file.

## [v0.4.1] - 2026-09-01

### Changed
- **SKILL.md 瘦身**：从 1226 行 / 38KB 拆分为 415 行正文 + `references/` 四个参考文件（factors.md 14 因子全表、emotions.md 情绪状态机、avatar.md 头像设计、automation.md 热加载与自动触发），消除巨型 Prompt 反模式
- `description` 改为标准路由公式（"当用户需要…时使用"），长度 156→73 字
- 删除 SKILL.md 正文中的寒暄词「我来帮你」（违反 self-awareness 自身铁律 12）
- 补 `agent_created: true` frontmatter 字段，使 SkillManage 可管理

### Fixed
- 顺带修复上游 skill-studio `audit.py` 的 `py_compile` 误报：语法检查改为内存编译，不再在被审计 skill 的 `scripts/__pycache__/` 写下 `.pyc` 再误报为残留

## [v0.4.0] - 2026-03-16

### Added
- Avatar generation feature (颜文字 + 图形头像)
- avatar_generator.py script with multi-provider support
- QUICKSTART.md for easy enable
- Support for agent self-generation (recommended), FluxImageGen, OpenAI DALL-E, etc.
- Auto-trigger mechanism: init/first_response/periodic_5/idle/emotion_decay/heartbeat
- Restart Gateway reminder in install scripts
- Hot reload mechanism (keyword trigger + manual command)

### Fixed
- UTF-8 encoding in PowerShell scripts
- Field alias support in avatar generator

### Changed
- Default provider changed to "agent" (let AI generate its own avatar)
- SKILL.md: added prominent restart warning

## [v0.3.2] - 2026-03-15

### Fixed
- PowerShell encoding issues causing script parse errors
- Chinese characters causing UTF-8 corruption

### Changed
- All scripts now use English output only (cross-platform safe)
- PowerShell scripts: added `[Console]::OutputEncoding = [System.Text.Encoding]::UTF8`
- Generated cognition files (INNATE.md etc.) still contain Chinese for user readability

## [v0.3.1] - 2026-03-14

### Fixed
- Auto-scan not working reliably (removed)
- GLOBAL.md not found (now uses skill's built-in template)
- Agent-driven configuration simplified

### Changed
- Simplified to Agent-driven approach (no auto-scan)
- GLOBAL.md priority: skill template > user config > default

## [v0.3.0] - 2026-03-14

### Added
- Cross-platform support (Linux/macOS/Windows PowerShell)
- Agent-driven configuration (Agent tells Skill where its config is)
- GLOBAL.md template for default personality
- Auto-detection of 13+ common config files
- Environment variable support for custom paths

### Fixed
- Field extraction regex patterns (support multiple formats)
- Multi-path scanning (scan common directories)
- PowerShell syntax issues

### Changed
- Improved README documentation
- Enhanced SKILL.md with agent-driven approach

## [v0.2.0] - 2026-03-13

### Added
- Emotional state machine with 13 emotions
- Visible emoji indicators for emotions
- Version control for cognitive files
- Hybrid trigger rules (keyword + semantic)

## [v0.1.0] - 2026-03-13

### Added
- Initial release
- Three-layer cognition system (INNATE/ACQUIRED/LEARNED)
- 14 base personality factors
- Per-agent independent personality files
