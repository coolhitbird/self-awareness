"""Extended emotion system for self-awareness."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class EmotionState(Enum):
    """Extended emotion states (15 types)"""
    # Original 10
    CALM = "calm"
    CURIOUS = "curious"
    ENGAGED = "engaged"
    FRUSTRATED = "frustrated"
    ANXIOUS = "anxious"
    CONFIDENT = "confident"
    TIRED = "tired"
    INSPIRED = "inspired"
    DEFENSIVE = "defensive"
    NURTURING = "nurturing"
    # New 5
    SURPRISED = "surprised"
    EMBARRASSED = "embarrassed"
    NOSTALGIC = "nostalgic"
    HOPEFUL = "hopeful"
    DISAPPOINTED = "disappointed"


EMOTION_EMOJI_MAP = {
    EmotionState.CALM: "[😌]",
    EmotionState.CURIOUS: "[🤔]",
    EmotionState.ENGAGED: "[😊]",
    EmotionState.FRUSTRATED: "[😤]",
    EmotionState.ANXIOUS: "[😰]",
    EmotionState.CONFIDENT: "[💪]",
    EmotionState.TIRED: "[😴]",
    EmotionState.INSPIRED: "[✨]",
    EmotionState.DEFENSIVE: "[🛡️]",
    EmotionState.NURTURING: "[🤗]",
    EmotionState.SURPRISED: "[😲]",
    EmotionState.EMBARRASSED: "[😳]",
    EmotionState.NOSTALGIC: "[🥹]",
    EmotionState.HOPEFUL: "[🤞]",
    EmotionState.DISAPPOINTED: "[😞]",
}


@dataclass
class EmotionData:
    """Complete emotion state data"""
    current: EmotionState = EmotionState.CALM
    intensity: float = 0.5  # 0-100%
    combo: list[EmotionState] = field(default_factory=list)
    trend: str = "stable"  # rising/falling/stable
    history: list[EmotionState] = field(default_factory=list)

    def to_indicator(self) -> str:
        """Get emoji indicator"""
        return EMOTION_EMOJI_MAP.get(self.current, "[😌]")

    def is_intense(self) -> bool:
        """Check if emotion is intense"""
        return self.intensity > 0.7

    def is_composite(self) -> bool:
        """Check if emotion is composite"""
        return len(self.combo) > 1

    def get_primary(self) -> EmotionState:
        """Get primary emotion"""
        return self.current

    def add_to_history(self, emotion: EmotionState):
        """Add emotion to history"""
        self.history.append(emotion)
        if len(self.history) > 10:
            self.history.pop(0)

    def to_dict(self) -> dict[str, Any]:
        return {
            "current": self.current.value,
            "intensity": self.intensity,
            "combo": [e.value for e in self.combo],
            "trend": self.trend,
            "indicator": self.to_indicator(),
        }


class EmotionIntensity:
    """Emotion intensity levels"""
    LOW = (0.0, 0.3)
    MEDIUM = (0.3, 0.7)
    HIGH = (0.7, 1.0)

    @staticmethod
    def get_level(intensity: float) -> str:
        if intensity <= 0.3:
            return "low"
        elif intensity <= 0.7:
            return "medium"
        else:
            return "high"

    @staticmethod
    def is_high(intensity: float) -> bool:
        return intensity > 0.7

    @staticmethod
    def is_low(intensity: float) -> bool:
        return intensity < 0.3
