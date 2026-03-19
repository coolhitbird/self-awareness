"""Base engine and engine registry."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from ..models.dimensions import BaseDimension
    from ..models.state import SevenDimensionalState


@dataclass
class EvaluationResult:
    """Result from an evaluation engine."""
    dimension: str
    score: float
    confidence: float
    indicators: dict[str, Any]
    recommendations: list[str]
    raw_data: dict[str, Any]


class BaseEngine(ABC):
    """Abstract base for evaluation engines."""

    def __init__(self, dimension: BaseDimension):
        self.dimension = dimension
        self.name = dimension.DIMENSION_NAME

    @abstractmethod
    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        """Evaluate this dimension's state."""
        pass

    def preprocess(self, context: dict[str, Any]) -> dict[str, Any]:
        """Preprocess context before evaluation."""
        return context

    def postprocess(self, result: EvaluationResult) -> EvaluationResult:
        """Postprocess evaluation result."""
        return result


class EngineRegistry:
    """Registry for evaluation engines."""

    _engines: dict[str, BaseEngine] = {}

    @classmethod
    def register(cls, engine: BaseEngine):
        """Register an engine."""
        cls._engines[engine.name] = engine

    @classmethod
    def get(cls, name: str) -> BaseEngine | None:
        """Get an engine by name."""
        return cls._engines.get(name)

    @classmethod
    def list_engines(cls) -> list[str]:
        """List all registered engines."""
        return list(cls._engines.keys())

    @classmethod
    def get_all(cls) -> dict[str, BaseEngine]:
        """Get all registered engines."""
        return cls._engines.copy()
