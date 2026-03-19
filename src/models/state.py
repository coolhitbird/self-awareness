"""Seven-dimensional state management."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any

from .dimensions import DimensionRegistry


class EmotionState(Enum):
    """Emotional state machine states."""
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


EMOTION_EMOJI = {
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
}


@dataclass
class DimensionScore:
    """Score for a single dimension."""
    name: str
    value: float
    confidence: float = 1.0
    timestamp: datetime = field(default_factory=datetime.now)
    indicators: dict[str, Any] = field(default_factory=dict)

    def is_healthy(self, threshold: float = 0.3) -> bool:
        return self.value >= threshold

    def trend(self, previous: DimensionScore) -> float:
        return self.value - previous.value


@dataclass
class SevenDimensionalState:
    """Complete seven-dimensional self-awareness state."""
    agent_id: str
    existential: float = 0.5
    coherence: float = 0.5
    meaning: float = 0.5
    autonomy: float = 0.5
    relational: float = 0.5
    evolution: float = 0.5
    navigation: float = 0.5
    
    emotion: EmotionState = EmotionState.CALM
    emotion_intensity: float = 0.5
    
    timestamp: datetime = field(default_factory=datetime.now)
    interactions_count: int = 0
    last_trigger: str = "init"

    def get_score(self, dimension: str) -> float:
        return getattr(self, dimension, 0.5)

    def set_score(self, dimension: str, value: float):
        if hasattr(self, dimension):
            setattr(self, dimension, max(0.0, min(1.0, value)))

    @property
    def overall_stability(self) -> float:
        scores = [
            self.existential, self.coherence, self.meaning,
            self.autonomy, self.relational, self.evolution, self.navigation
        ]
        return sum(scores) / len(scores)

    @property
    def weakest_dimension(self) -> str:
        dims = {
            "existential": self.existential,
            "coherence": self.coherence,
            "meaning": self.meaning,
            "autonomy": self.autonomy,
            "relational": self.relational,
            "evolution": self.evolution,
            "navigation": self.navigation,
        }
        return min(dims, key=dims.get)

    @property
    def strongest_dimension(self) -> str:
        dims = {
            "existential": self.existential,
            "coherence": self.coherence,
            "meaning": self.meaning,
            "autonomy": self.autonomy,
            "relational": self.relational,
            "evolution": self.evolution,
            "navigation": self.navigation,
        }
        return max(dims, key=dims.get)

    def to_indicator(self) -> str:
        return EMOTION_EMOJI.get(self.emotion, "[😌]")

    def needs_attention(self) -> bool:
        return self.overall_stability < 0.4 or self.emotion_intensity > 0.8

    def update_from_context(self, context: dict[str, Any]):
        """Update state from evaluation context."""
        for dim_name in ["existential", "coherence", "meaning", "autonomy", 
                         "relational", "evolution", "navigation"]:
            if dim_name in context:
                self.set_score(dim_name, context[dim_name])

        if "emotion" in context:
            try:
                self.emotion = EmotionState(context["emotion"])
            except ValueError:
                pass

        if "emotion_intensity" in context:
            self.emotion_intensity = context["emotion_intensity"]

        self.timestamp = datetime.now()

    def get_snapshot(self) -> dict[str, Any]:
        """Get a snapshot of the current state."""
        return {
            "agent_id": self.agent_id,
            "existential": self.existential,
            "coherence": self.coherence,
            "meaning": self.meaning,
            "autonomy": self.autonomy,
            "relational": self.relational,
            "evolution": self.evolution,
            "navigation": self.navigation,
            "emotion": self.emotion.value,
            "emotion_indicator": self.to_indicator(),
            "emotion_intensity": self.emotion_intensity,
            "overall_stability": self.overall_stability,
            "weakest": self.weakest_dimension,
            "strongest": self.strongest_dimension,
            "timestamp": self.timestamp.isoformat(),
            "interactions": self.interactions_count,
        }


class StateManager:
    """Manages state persistence and transitions."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.current_state = SevenDimensionalState(agent_id=agent_id)
        self.history: list[SevenDimensionalState] = []
        self.max_history = 100

    def update(self, new_state: SevenDimensionalState):
        """Update current state and archive previous."""
        self.history.append(self.current_state)
        if len(self.history) > self.max_history:
            self.history.pop(0)
        self.current_state = new_state

    def increment_interaction(self):
        """Increment interaction counter."""
        self.current_state.interactions_count += 1

    def transition_emotion(self, new_emotion: EmotionState, intensity: float = 0.5):
        """Transition to a new emotional state."""
        self.current_state.emotion = new_emotion
        self.current_state.emotion_intensity = intensity

    def decay_emotion(self, rate: float = 0.1):
        """Decay emotion intensity over time."""
        self.current_state.emotion_intensity = max(
            0.0, 
            self.current_state.emotion_intensity - rate
        )

    def get_trend(self, dimension: str, points: int = 5) -> float:
        """Calculate trend for a dimension over recent history."""
        if len(self.history) < 2:
            return 0.0
        
        recent = self.history[-points:]
        values = [s.get_score(dimension) for s in recent]
        
        if len(values) < 2:
            return 0.0
        
        return (values[-1] - values[0]) / len(values)
