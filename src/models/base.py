"""Base profile for self-awareness."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class Gender(Enum):
    """Gender types"""
    MASCULINE = "masculine"
    FEMININE = "feminine"
    NONBINARY = "nonbinary"
    TRANSGENDER = "transgender"
    GENDER_NEUTRAL = "gender_neutral"
    GENDERFLUID = "genderfluid"
    AGENDER = "agender"


class Culture(Enum):
    """Cultural backgrounds"""
    EAST_ASIAN = "east_asian"
    WESTERN = "western"
    LATIN_AMERICAN = "latin_american"
    MIDDLE_EASTERN = "middle_eastern"
    SOUTH_ASIAN = "south_asian"
    NORDIC = "nordic"
    UNIVERSAL = "universal"


class Values(Enum):
    """Value orientations"""
    BALANCED = "balanced"
    ACHIEVEMENT = "achievement"
    BENEVOLENCE = "benevolence"
    TRADITION = "tradition"
    SECURITY = "security"
    SELF_DIRECTION = "self_direction"
    STIMULATION = "stimulation"
    HEDONISM = "hedonism"


class Personality(Enum):
    """Personality types"""
    INTROVERT = "introvert"
    EXTROVERT = "extrovert"
    THINKING = "thinking"
    FEELING = "feeling"
    SENSING = "sensing"
    INTUITIVE = "intuitive"
    JUDGING = "judging"
    PERCEIVING = "perceiving"


class Identity(Enum):
    """Identity types"""
    ASSISTANT = "assistant"
    PARTNER = "partner"
    MENTOR = "mentor"
    COLLABORATOR = "collaborator"
    EXPERT = "expert"
    FRIEND = "friend"
    CREATOR = "creator"
    LEARNER = "learner"


@dataclass
class BaseProfile:
    """Base profile containing fundamental attributes"""
    gender: str = "universal"
    culture: str = "universal"
    values: str = "balanced"
    personality: str = "balanced"
    identity: str = "assistant"
    
    # Additional metadata
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "gender": self.gender,
            "culture": self.culture,
            "values": self.values,
            "personality": self.personality,
            "identity": self.identity,
            "metadata": self.metadata,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> BaseProfile:
        return cls(
            gender=data.get("gender", "universal"),
            culture=data.get("culture", "universal"),
            values=data.get("values", "balanced"),
            personality=data.get("personality", "balanced"),
            identity=data.get("identity", "assistant"),
            metadata=data.get("metadata", {}),
        )

    @classmethod
    def default(cls) -> BaseProfile:
        """Create default profile"""
        return cls(
            gender="universal",
            culture="universal",
            values="balanced",
            personality="balanced",
            identity="assistant",
        )

    def get_primary(self) -> str:
        """Get primary identity"""
        return self.identity

    def get_emotion_tendency(self) -> dict[str, list[str]]:
        """Get emotion tendency based on profile (for rule engine)"""
        return {
            "gender": self.gender,
            "culture": self.culture,
            "values": self.values,
            "personality": self.personality,
            "identity": self.identity,
        }
