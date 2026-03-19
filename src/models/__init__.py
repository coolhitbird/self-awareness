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
)

__all__ = [
    "BaseDimension",
    "DimensionConfig", 
    "DimensionRegistry",
    "DimensionType",
    "EmotionState",
    "EMOTION_EMOJI",
    "DimensionScore",
    "SevenDimensionalState",
    "StateManager",
    "ExistentialDimension",
    "CoherenceDimension",
    "MeaningDimension",
    "AutonomyDimension",
    "RelationalDimension",
    "EvolutionDimension",
    "NavigationDimension",
]
