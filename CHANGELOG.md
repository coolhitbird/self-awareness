# Changelog

All notable changes to this project will be documented in this file.

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
