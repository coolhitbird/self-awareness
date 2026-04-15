"""Extensible dimension registry and base classes."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable


class DimensionType(Enum):
    """Twelve dimensions of self-awareness (7 core + 5 extended)."""
    # Core 7
    EXISTENTIAL = "existential"
    COHERENCE = "coherence"
    MEANING = "meaning"
    AUTONOMY = "autonomy"
    RELATIONAL = "relational"
    EVOLUTION = "evolution"
    NAVIGATION = "navigation"
    # Extended 5
    CREATIVITY = "creativity"
    RESILIENCE = "resilience"
    WISDOM = "wisdom"
    AUTHENTICITY = "authenticity"
    HUMOR = "humor"

    @classmethod
    def core_dimensions(cls) -> list[str]:
        """Get core 7 dimensions"""
        return [
            "existential", "coherence", "meaning", "autonomy",
            "relational", "evolution", "navigation"
        ]

    @classmethod
    def extended_dimensions(cls) -> list[str]:
        """Get extended 5 dimensions"""
        return ["creativity", "resilience", "wisdom", "authenticity", "humor"]

    @classmethod
    def all_dimensions(cls) -> list[str]:
        """Get all 12 dimensions"""
        return cls.core_dimensions() + cls.extended_dimensions()


@dataclass
class DimensionConfig:
    """Configuration for a dimension."""
    name: str
    weight: float = 1.0
    enabled: bool = True
    thresholds: dict[str, float] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseDimension(ABC):
    """Abstract base class for dimensions."""

    DIMENSION_NAME: str = ""

    def __init__(self, config: DimensionConfig | None = None):
        self.config = config or DimensionConfig(name=self.DIMENSION_NAME)

    @abstractmethod
    def evaluate(self, context: dict[str, Any]) -> float:
        """Evaluate this dimension's state. Returns 0.0-1.0."""
        pass

    @abstractmethod
    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        """Get detailed indicators for this dimension."""
        pass

    @property
    def name(self) -> str:
        return self.config.name

    @property
    def weight(self) -> float:
        return self.config.weight


_DIMENSIONS: dict[str, type[BaseDimension]] = {}
_CONFIGS: dict[str, DimensionConfig] = {}


def register_dimension(dim_class: type[BaseDimension]):
    """Decorator to register a dimension class."""
    name = dim_class.DIMENSION_NAME
    _DIMENSIONS[name] = dim_class
    _CONFIGS[name] = DimensionConfig(name=name)
    return dim_class


class DimensionRegistry:
    """Registry for extensible dimensions."""

    _instance: DimensionRegistry | None = None

    def __new__(cls) -> DimensionRegistry:
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def _ensure_initialized(self):
        """Ensure core dimensions are registered."""
        if not getattr(self, '_initialized', False):
            self._register_core_dimensions()
            self._initialized = True

    def _register_core_dimensions(self):
        """Register the seven core dimensions."""
        from .core_dimensions import (
            ExistentialDimension, CoherenceDimension, MeaningDimension,
            AutonomyDimension, RelationalDimension, EvolutionDimension,
            NavigationDimension
        )
        for dim_class in [ExistentialDimension, CoherenceDimension, MeaningDimension,
                          AutonomyDimension, RelationalDimension, EvolutionDimension,
                          NavigationDimension]:
            _DIMENSIONS[dim_class.DIMENSION_NAME] = dim_class
            _CONFIGS[dim_class.DIMENSION_NAME] = DimensionConfig(name=dim_class.DIMENSION_NAME)

    @classmethod
    def register(cls, dimension_class: type[BaseDimension], name: str | None = None):
        """Register a dimension class."""
        cls()._ensure_initialized()
        dim_name = name or dimension_class.DIMENSION_NAME
        _DIMENSIONS[dim_name] = dimension_class
        _CONFIGS[dim_name] = DimensionConfig(name=dim_name)

    @classmethod
    def get(cls, name: str) -> type[BaseDimension] | None:
        """Get a dimension class by name."""
        cls()._ensure_initialized()
        return _DIMENSIONS.get(name)

    @classmethod
    def create(cls, name: str, config: DimensionConfig | None = None) -> BaseDimension | None:
        """Create a dimension instance by name."""
        cls()._ensure_initialized()
        dim_class = cls.get(name)
        if dim_class is None:
            return None
        return dim_class(config or _CONFIGS.get(name))

    @classmethod
    def list_dimensions(cls) -> list[str]:
        """List all registered dimension names."""
        cls()._ensure_initialized()
        return list(_DIMENSIONS.keys())

    @classmethod
    def get_configs(cls) -> dict[str, DimensionConfig]:
        """Get all dimension configurations."""
        cls()._ensure_initialized()
        return _CONFIGS.copy()

    @classmethod
    def update_config(cls, name: str, config: DimensionConfig):
        """Update a dimension's configuration."""
        cls()._ensure_initialized()
        _CONFIGS[name] = config

    @classmethod
    def reset(cls):
        """Reset the registry (mainly for testing)."""
        cls._instance = None
        _DIMENSIONS.clear()
        _CONFIGS.clear()
