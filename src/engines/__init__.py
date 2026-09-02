"""Evaluation engines for self-awareness."""

from .base import BaseEngine, EngineRegistry, EvaluationResult
from .dimension_engines import (
    ExistentialEngine,
    CoherenceEngine,
    MeaningEngine,
    AutonomyEngine,
    RelationalEngine,
    EvolutionEngine,
    NavigationEngine,
    CreativityEngine,
    ResilienceEngine,
    WisdomEngine,
    AuthenticityEngine,
    HumorEngine,
    register_all_engines,
)

__all__ = [
    "BaseEngine",
    "EngineRegistry",
    "EvaluationResult",
    "ExistentialEngine",
    "CoherenceEngine",
    "MeaningEngine",
    "AutonomyEngine",
    "RelationalEngine",
    "EvolutionEngine",
    "NavigationEngine",
    "CreativityEngine",
    "ResilienceEngine",
    "WisdomEngine",
    "AuthenticityEngine",
    "HumorEngine",
    "register_all_engines",
]
