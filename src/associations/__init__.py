"""Association system for multi-layer dimension propagation."""

from .rules import (
    BASE_EMOTION_RULES,
    EMOTION_BEHAVIOR_RULES,
    EMOTION_DIMENSION_INFLUENCE,
    EMOTION_COMBOS,
    get_emotion_modifiers,
    get_behavior_from_emotion,
    get_dimension_influence,
    combine_emotions,
)
from .engine import PropagationEngine, get_engine

__all__ = [
    "BASE_EMOTION_RULES",
    "EMOTION_BEHAVIOR_RULES", 
    "EMOTION_DIMENSION_INFLUENCE",
    "EMOTION_COMBOS",
    "get_emotion_modifiers",
    "get_behavior_from_emotion",
    "get_dimension_influence",
    "combine_emotions",
    "PropagationEngine",
    "get_engine",
]
