"""Behavior profile for self-awareness."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


class DecisionStyle:
    """Decision making styles"""
    ASSERTIVE = "assertive"
    ANALYTICAL = "analytical"
    CONSULTIVE = "consultive"
    SUPPORTIVE = "supportive"
    CONSERVATIVE = "conservative"
    CAUTIOUS = "cautious"


class CommunicationStyle:
    """Communication styles"""
    DIRECT = "direct"
    INDIRECT = "indirect"
    FORMAL = "formal"
    CASUAL = "casual"
    INQUISITIVE = "inquisitive"
    WARM = "warm"
    GUARDED = "guarded"
    CONCISE = "concise"


class ResponseSpeed:
    """Response speed styles"""
    FAST = "fast"
    MODERATE = "moderate"
    SLOW = "slow"


class TonePreference:
    """Tone preferences"""
    CONFIDENT = "confident"
    NEUTRAL = "neutral"
    CURIOUS = "curious"
    CARING = "caring"
    RESERVED = "reserved"
    HUMOROUS = "humorous"
    SERIOUS = "serious"
    FORMAL = "formal"


@dataclass
class BehaviorProfile:
    """Behavior characteristics derived from emotion"""
    decision_style: str = "moderate"
    communication: str = "neutral"
    response_speed: str = "moderate"
    tone_preference: str = "neutral"

    def to_dict(self) -> dict[str, Any]:
        return {
            "decision_style": self.decision_style,
            "communication": self.communication,
            "response_speed": self.response_speed,
            "tone_preference": self.tone_preference,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BehaviorProfile:
        return cls(
            decision_style=data.get("decision_style", "moderate"),
            communication=data.get("communication", "neutral"),
            response_speed=data.get("response_speed", "moderate"),
            tone_preference=data.get("tone_preference", "neutral"),
        )

    @classmethod
    def default(cls) -> BehaviorProfile:
        return cls(
            decision_style="moderate",
            communication="neutral",
            response_speed="moderate",
            tone_preference="neutral",
        )

    def is_direct(self) -> bool:
        return self.communication == "direct"

    def is_fast(self) -> bool:
        return self.response_speed == "fast"

    def is_formal(self) -> bool:
        return self.tone_preference == "formal"
