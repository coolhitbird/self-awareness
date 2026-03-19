"""Avatar system for text and visual avatars."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from ..models.state import EmotionState


@dataclass
class AvatarConfig:
    """Configuration for avatar generation."""
    style: str = "default"
    include_kaomoji: bool = True
    include_emoji: bool = True
    text_color: str | None = None
    bg_color: str | None = None


KAOMOJI_MAP: dict[EmotionState, list[str]] = {
    EmotionState.CALM: [
        "(^_^)", "(~‾‿~)", "(´∀`)", "(｡◕‿◕｡)", "ヽ(>∀<☆)☆",
    ],
    EmotionState.CURIOUS: [
        "(・ω・)", "(°o°)", "(？？？)", "(・⊝・)", "∂(＿＿)",
    ],
    EmotionState.ENGAGED: [
        "(ﾉ´ヮ`)ﾉ*: ・゚✧", "(★‿★)", "(◕‿◕)", "(✧ω✧)", "ヽ(>∀<☆)☆",
    ],
    EmotionState.FRUSTRATED: [
        "(╯°□°）╯︵ ┻━┻", "(¬_¬)", "(눈_눈)", "(╯︵╰,)", "ヽ(`Д´)ノ",
    ],
    EmotionState.ANXIOUS: [
        "(´°̥̥̥̥̥̥̥̥ω°̥̥̥̥̥̥̥̥`)", "(°_°;)", "(ﾟДﾟ;)", "(゜Д゜)", "(；´Д`)",
    ],
    EmotionState.CONFIDENT: [
        "(ง •̀_•́)ง", "ᕦ(ò_óˇ)ᕤ", "(💪˙³˙)", "(◐‿◑)", "(ᕙ(⇀‸↼‶)ᕗ",
    ],
    EmotionState.TIRED: [
        "(－_－) zzZ", "(￣o￣) .zzZZ", "(=_=)", "( ´_ゝ`)", "(-_-) zzZ",
    ],
    EmotionState.INSPIRED: [
        "(☆▽☆)", "(°□°)/", "(੭ु≧▽≦)੭ु⁾⁾", "(*≧▽≦)", "(✨ω✨)",
    ],
    EmotionState.DEFENSIVE: [
        "(￣ω￣)", "(¬‿¬)", "(ಠ_ಠ)", "(눈_눈)", "(｀ε´)",
    ],
    EmotionState.NURTURING: [
        "(´◡´)", "(♡˙︶˙♡)", "(◕‿◕✿)", "(｡♥‿♥｡)", "(✿´‿`)",
    ],
}


def get_kaomoji(emotion: EmotionState, index: int = 0) -> str:
    """Get a kaomoji for an emotion state."""
    kaomojis = KAOMOJI_MAP.get(emotion, KAOMOJI_MAP[EmotionState.CALM])
    return kaomojis[index % len(kaomojis)]


def get_random_kaomoji(emotion: EmotionState) -> str:
    """Get a random kaomoji for an emotion state."""
    import random
    kaomojis = KAOMOJI_MAP.get(emotion, KAOMOJI_MAP[EmotionState.CALM])
    return random.choice(kaomojis)


def format_avatar(
    emotion: EmotionState,
    emotion_intensity: float,
    include_emotion_indicator: bool = True,
) -> str:
    """Format avatar string with emotion and kaomoji."""
    parts = []
    
    if include_emotion_indicator:
        from ..models.state import EMOTION_EMOJI
        parts.append(EMOTION_EMOJI.get(emotion, "[😌]"))
    
    parts.append(get_kaomoji(emotion))
    
    if emotion_intensity > 0.7:
        parts.append("!!")
    elif emotion_intensity > 0.5:
        parts.append("!")
    
    return " ".join(parts)


@dataclass
class AvatarStyle:
    """Style configuration for avatar generation."""
    primary_color: str = "#4A90D9"
    secondary_color: str = "#2C3E50"
    font_size: int = 24
    padding: int = 20
    border_radius: int = 12


class AvatarGenerator:
    """Generate visual avatars for agents."""

    STYLES: dict[str, AvatarStyle] = {
        "default": AvatarStyle(),
        "dark": AvatarStyle(
            primary_color="#1a1a2e",
            secondary_color="#16213e",
        ),
        "warm": AvatarStyle(
            primary_color="#ff6b6b",
            secondary_color="#ee5a5a",
        ),
        "minimal": AvatarStyle(
            primary_color="#f8f9fa",
            secondary_color="#e9ecef",
            border_radius=50,
        ),
    }

    def __init__(self, style: str = "default"):
        self.style = self.STYLES.get(style, self.STYLES["default"])

    def generate_svg(self, kaomoji: str, config: AvatarConfig | None = None) -> str:
        """Generate SVG avatar."""
        if config is None:
            config = AvatarConfig()

        colors = self.style
        font_size = colors.font_size
        padding = colors.padding

        width = len(kaomoji) * font_size + padding * 2
        height = font_size + padding * 2

        return f'''<svg xmlns="http://www.w3.org/2000/svg" 
    width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect width="{width}" height="{height}" rx="{colors.border_radius}" 
        fill="{colors.primary_color}"/>
  <text x="50%" y="50%" dominant-baseline="middle" text-anchor="middle"
        font-size="{font_size}" fill="{colors.secondary_color}"
        font-family="monospace">{kaomoji}</text>
</svg>'''

    def generate_css(self, kaomoji: str, config: AvatarConfig | None = None) -> str:
        """Generate CSS avatar class."""
        if config is None:
            config = AvatarConfig()

        colors = self.style

        return f'''.agent-avatar {{
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: {colors.padding}px;
  background: {colors.primary_color};
  border-radius: {colors.border_radius}px;
  font-family: monospace;
  font-size: {colors.font_size}px;
  color: {colors.secondary_color};
}}

.agent-avatar::before {{
  content: "{kaomoji}";
}}'''

    def generate_html(self, kaomoji: str, config: AvatarConfig | None = None) -> str:
        """Generate HTML avatar element."""
        svg = self.generate_svg(kaomoji, config)
        return f'<div class="agent-avatar">{kaomoji}</div>'

    @staticmethod
    def generate_prompt(state: dict[str, Any]) -> str:
        """Generate prompt for external avatar generation."""
        emotion = state.get("emotion", "calm")
        indicator = state.get("emotion_indicator", "[😌]")
        
        return f"""Create a minimalist avatar for an AI agent with the following characteristics:
- Current emotional state: {emotion}
- Visual indicator: {indicator}
- Style: Clean, simple, suitable for chat interface
- Colors: Use soft blues and grays
- Should convey the emotional state subtly

The avatar should be a small circular or rounded-square image."""


def create_agent_avatar(
    emotion: EmotionState,
    emotion_intensity: float = 0.5,
    format: str = "text",
    style: str = "default",
) -> str:
    """Convenience function to create an avatar."""
    generator = AvatarGenerator(style)
    kaomoji = get_kaomoji(emotion)
    
    if format == "text":
        return format_avatar(emotion, emotion_intensity)
    elif format == "svg":
        return generator.generate_svg(kaomoji)
    elif format == "html":
        return generator.generate_html(kaomoji)
    elif format == "css":
        return generator.generate_css(kaomoji)
    else:
        return kaomoji
