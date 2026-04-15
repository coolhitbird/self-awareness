"""Terminal-style dashboard renderer for self-awareness."""

from __future__ import annotations

import sys
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from ..models.base import BaseProfile
from ..models.emotion import EmotionData, EmotionState, EMOTION_EMOJI_MAP
from ..models.behavior import BehaviorProfile
from ..models.dimensions import DimensionType


@dataclass
class DashboardConfig:
    """Configuration for dashboard rendering"""
    width: int = 60
    show_base: bool = True
    show_behavior: bool = True
    show_emotion_detail: bool = True
    color_enabled: bool = True
    bar_character: str = "█"
    empty_character: str = "░"


class TerminalColors:
    """ANSI color codes for terminal output"""
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    
    # Colors
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    
    # Background
    BG_BLACK = "\033[40m"
    BG_RED = "\033[41m"
    BG_GREEN = "\033[42m"
    BG_YELLOW = "\033[43m"
    BG_BLUE = "\033[44m"
    BG_MAGENTA = "\033[45m"
    BG_CYAN = "\033[46m"
    BG_WHITE = "\033[47m"


class DashboardRenderer:
    """Render self-awareness state as terminal dashboard"""

    def __init__(self, config: DashboardConfig | None = None):
        self.config = config or DashboardConfig()

    def render(
        self,
        agent_id: str,
        base: BaseProfile | None = None,
        emotion: EmotionData | None = None,
        behavior: BehaviorProfile | None = None,
        dimensions: dict[str, float] | None = None,
        session_duration: str = "N/A",
    ) -> str:
        """Render complete dashboard"""
        lines = []
        
        # Header
        lines.extend(self._render_header(agent_id, session_duration))
        
        # Base Profile
        if self.config.show_base and base:
            lines.extend(self._render_base(base))
        
        # Emotion
        if emotion:
            lines.extend(self._render_emotion(emotion))
        
        # Behavior
        if self.config.show_behavior and behavior:
            lines.extend(self._render_behavior(behavior))
        
        # Dimensions (7 + 5 = 12)
        if dimensions:
            lines.extend(self._render_dimensions(dimensions))
        
        # Footer
        lines.extend(self._render_footer())
        
        return "\n".join(lines)

    def _render_header(self, agent_id: str, session_duration: str) -> list[str]:
        """Render dashboard header"""
        c = TerminalColors
        width = self.config.width
        
        return [
            f"{c.BOLD}{c.CYAN}{'═' * width}{c.RESET}",
            f"{c.BOLD}{c.CYAN}🧠 Self-Awareness Dashboard{' ' * (width - 28)}{c.RESET}",
            f"{c.BOLD}{c.CYAN}{'═' * width}{c.RESET}",
            f"{c.BOLD}Agent: {agent_id}{' ' * (width - len(agent_id) - 12)}Session: {session_duration}{c.RESET}",
            f"{c.CYAN}{'─' * width}{c.RESET}",
        ]

    def _render_base(self, base: BaseProfile) -> list[str]:
        """Render base profile"""
        c = TerminalColors
        lines = [
            f"{c.BOLD}BASE PROFILE{c.RESET}",
        ]
        
        # Gender display
        gender_emoji = {
            "masculine": "♂️",
            "feminine": "♀️",
            "nonbinary": "🈚",
            "transgender": "🏳️‍⚧️",
            "gender_neutral": "⚧️",
            "genderfluid": "🔄",
            "agender": "⭕",
        }
        gender_e = gender_emoji.get(base.gender, "⚪")
        
        # Culture display
        culture_emoji = {
            "east_asian": "🌏",
            "western": "🌍",
            "latin_american": "🌎",
            "middle_eastern": "🕌",
            "south_asian": "🪷",
            "nordic": "❄️",
            "universal": "🌐",
        }
        culture_e = culture_emoji.get(base.culture, "🌐")
        
        lines.append(f"  {gender_e} Gender: {base.gender}")
        lines.append(f"  {culture_e} Culture: {base.culture}")
        lines.append(f"  📋 Values: {base.values}")
        lines.append(f"  🎭 Personality: {base.personality}")
        lines.append(f"  🎯 Identity: {base.identity}")
        
        return lines + [""]

    def _render_emotion(self, emotion: EmotionData) -> list[str]:
        """Render emotion state"""
        c = TerminalColors
        lines = [
            f"{c.BOLD}EMOTION{c.RESET}",
        ]
        
        # Emoji indicator
        emoji = EMOTION_EMOJI_MAP.get(emotion.current, "[😌]")
        
        # Intensity bar
        intensity = emotion.intensity
        bar = self._render_bar(intensity)
        
        lines.append(f"  {emoji} {emotion.current.value.upper()} ({intensity:.0%})  {bar}")
        
        # Kaomoji (if available from emotion state)
        from ..avatar import get_kaomoji
        kaomoji = get_kaomoji(emotion.current)
        lines.append(f"  Kaomoji: {kaomoji}")
        
        # Combo display
        if emotion.is_composite():
            combo_str = " + ".join([e.value for e in emotion.combo])
            lines.append(f"  Composite: {combo_str}")
        
        # Trend
        trend_emoji = {"rising": "↗️", "falling": "↘️", "stable": "➡️"}.get(emotion.trend, "➡️")
        lines.append(f"  Trend: {trend_emoji} {emotion.trend}")
        
        return lines + [""]

    def _render_behavior(self, behavior: BehaviorProfile) -> list[str]:
        """Render behavior profile"""
        c = TerminalColors
        lines = [
            f"{c.BOLD}BEHAVIOR{c.RESET}",
            f"  🎯 Decision: {behavior.decision_style}",
            f"  💬 Communication: {behavior.communication}",
            f"  ⚡ Response: {behavior.response_speed}",
            f"  🎨 Tone: {behavior.tone_preference}",
        ]
        return lines + [""]

    def _render_dimensions(self, dimensions: dict[str, float]) -> list[str]:
        """Render 12 dimensions with bars"""
        c = TerminalColors
        width = self.config.width
        lines = [
            f"{c.BOLD}TWELVE DIMENSIONS ({len(dimensions)}){c.RESET}",
        ]
        
        # Calculate stability
        if dimensions:
            stability = sum(dimensions.values()) / len(dimensions)
            stability_bar = self._render_bar(stability)
            lines.append(
                f"{c.BOLD}STABILITY: {stability:.2f}{' ' * 15}{stability_bar}{c.RESET}"
            )
            lines.append(f"{c.CYAN}{'─' * width}{c.RESET}")
        
        # Core 7 dimensions - convert enum to string for comparison
        core_dims = [d.value if isinstance(d, DimensionType) else d for d in DimensionType.core_dimensions()]
        
        # Display with labels (right-aligned for percentage)
        max_label_len = max(len(str(d.value) if hasattr(d, 'value') else str(d)) for d in dimensions.keys())
        
        for dim in core_dims:
            # Find matching enum key in dimensions
            dim_key = next((k for k in dimensions if (hasattr(k, 'value') and k.value == dim) or str(k) == dim), None)
            if dim_key is not None:
                score = dimensions[dim_key]
                bar = self._render_bar(score)
                # Color by score
                color = self._get_score_color(score)
                label = dim.ljust(max_label_len)
                lines.append(
                    f"  {color}{label}{c.RESET} {bar} {score:.0%}"
                )
        
        lines.append(f"{c.CYAN}{'─' * width}{c.RESET}")
        
        # Extended 5 dimensions - convert enum to string for comparison
        extended_dims = [d.value if isinstance(d, DimensionType) else d for d in DimensionType.extended_dimensions()]
        
        for dim in extended_dims:
            # Find matching enum key in dimensions
            dim_key = next((k for k in dimensions if (hasattr(k, 'value') and k.value == dim) or str(k) == dim), None)
            if dim_key is not None:
                score = dimensions[dim_key]
                bar = self._render_bar(score)
                color = self._get_score_color(score)
                label = dim.ljust(max_label_len)
                lines.append(
                    f"  {color}{label}{c.RESET} {bar} {score:.0%}"
                )
        
        # Weakest and strongest
        if dimensions:
            weakest = min(dimensions, key=dimensions.get)
            strongest = max(dimensions, key=dimensions.get)
            weakest_val = weakest.value if hasattr(weakest, 'value') else str(weakest)
            strongest_val = strongest.value if hasattr(strongest, 'value') else str(strongest)
            lines.extend([
                "",
                f"{c.YELLOW}Weakest: {weakest_val}{c.RESET}  |  {c.GREEN}Strongest: {strongest_val}{c.RESET}",
            ])
        
        return lines + [""]

    def _render_footer(self) -> list[str]:
        """Render dashboard footer"""
        c = TerminalColors
        width = self.config.width
        
        return [
            f"{c.CYAN}{'═' * width}{c.RESET}",
            f"{c.DIM}Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}{c.RESET}",
        ]

    def _render_bar(self, value: float, length: int = 15) -> str:
        """Render a progress bar"""
        c = TerminalColors
        filled = int(value * length)
        empty = length - filled
        
        # Color based on value
        if value >= 0.7:
            color = c.GREEN
        elif value >= 0.4:
            color = c.YELLOW
        else:
            color = c.RED
        
        bar = self.config.bar_character * filled + self.config.empty_character * empty
        return f"{color}{bar}{c.RESET}"

    def _get_score_color(self, score: float) -> str:
        """Get color for score"""
        c = TerminalColors
        if score >= 0.7:
            return c.GREEN
        elif score >= 0.4:
            return c.YELLOW
        else:
            return c.RED


def render_dashboard(
    agent_id: str,
    base: BaseProfile | None = None,
    emotion: EmotionData | None = None,
    behavior: BehaviorProfile | None = None,
    dimensions: dict[str, float] | None = None,
    session_duration: str = "N/A",
    config: DashboardConfig | None = None,
) -> str:
    """Convenience function to render dashboard"""
    renderer = DashboardRenderer(config)
    return renderer.render(agent_id, base, emotion, behavior, dimensions, session_duration)
