# Changelog

All notable changes to this project will be documented in this file.

## [v0.5.2] - 2026-08-06

### Changed
- **「引入Skill」段落升级为硬性规则**：从软性描述升级为「每次回复前必须执行的硬性规则」，包含三步流程（读认知文件 → 自我质疑 → 加情绪标识）+ 15种情绪状态映射表（含Emoji + 颜文字）+ 情绪状态机图 + 状态切换规则（强度保护/30分钟衰减/组合情绪）。本地测试验证后合并至 GitHub 主分支。

### Added
- VERSION → 0.5.2 / 2026-08-06
- _meta.json → version 0.5.2

## [v0.5.1] - 2026-03-19

### Added
- **OpenCode Skill打包**: 添加标准参考文件
  - `criteria.md` - 成功标准
  - `execution.md` - 使用流程
  - `state.md` - 状态结构
  - `planning.md` - 开发计划
  - `verification.md` - 验证清单
- 更新 `SKILL.md` frontmatter (version, homepage, metadata)
- 更新 `_meta.json` 版本信息

### Fixed
- PowerShell `install.ps1`: `$IsWindows` variable conflict (renamed to `$RunningOnWindows`)
- Verified `auto-init-cognition.sh` has proper LF line endings

## [v0.5.0] - 2026-03-19

### Added
- **Python Core Package** (`src/`): Complete Python implementation
  - `cognition/`: Cognition file reader/writer with three-layer support
  - `models/`: Seven-dimensional state system with extensible registry
  - `engines/`: 7 evaluation engines for all dimensions
  - `triggers/`: 6 trigger types + SelfAwarenessEngine workflow
  - `avatar/`: Kaomoji mapping + text/visual avatar generation
  - `telemetry/`: Event recording + Analytics reporting
- **Test Suite** (`tests/`): Complete test coverage
  - TC-01~TC-08 integration tests
  - All modules tested and passing
- **Full Test Script** (`test_full.py`): Automated 8-test suite
- **Test Plan** (`TEST_PLAN.md`): Detailed test cases for agent integration

### Changed
- Restructured from shell scripts to Python package
- Extensible dimension registry (supports future dimensions)
- Emotion state machine expanded to 10 states with intensity

### Fixed
- Module import issues resolved (relative import fix)
- UTF-8 encoding in all tests

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
