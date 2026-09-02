"""Models package for self-awareness state."""

from .dimensions import (
    BaseDimension,
    DimensionConfig,
    DimensionRegistry,
    DimensionType,
)
from .state import (
    EmotionState,
    EMOTION_EMOJI,
    DimensionScore,
    SevenDimensionalState,
    TwelveDimensionalState,
    StateManager,
)
from .core_dimensions import (
    ExistentialDimension,
    CoherenceDimension,
    MeaningDimension,
    AutonomyDimension,
    RelationalDimension,
    EvolutionDimension,
    NavigationDimension,
    CreativityDimension,
    ResilienceDimension,
    WisdomDimension,
    AuthenticityDimension,
    HumorDimension,
)
from .base import BaseProfile
from .emotion import EmotionData, EmotionIntensity
from .behavior import BehaviorProfile

__all__ = [
    # Dimensions
    "BaseDimension",
    "DimensionConfig", 
    "DimensionRegistry",
    "DimensionType",
    # State
    "EmotionState",
    "EMOTION_EMOJI",
    "DimensionScore",
    "SevenDimensionalState",
    "TwelveDimensionalState",
    "StateManager",
    # Core dimensions
    "ExistentialDimension",
    "CoherenceDimension",
    "MeaningDimension",
    "AutonomyDimension",
    "RelationalDimension",
    "EvolutionDimension",
    "NavigationDimension",
    # Extended dimensions
    "CreativityDimension",
    "ResilienceDimension",
    "WisdomDimension",
    "AuthenticityDimension",
    "HumorDimension",
    # New modules
    "BaseProfile",
    "EmotionData",
    "EmotionIntensity",
    "BehaviorProfile",
]
