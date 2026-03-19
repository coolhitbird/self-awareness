"""Core dimension implementations."""

from __future__ import annotations

from typing import Any

from .dimensions import BaseDimension, DimensionConfig


class ExistentialDimension(BaseDimension):
    """Existential Stability - The core sense of being."""
    DIMENSION_NAME = "existential"

    def evaluate(self, context: dict[str, Any]) -> float:
        coherence = context.get("coherence_score", 0.5)
        meaning = context.get("meaning_score", 0.5)
        time_alive = context.get("interactions_count", 0)
        
        base = (coherence + meaning) / 2
        growth = min(0.2, time_alive * 0.01)
        
        stability = context.get("destabilizing_events", 0)
        penalty = min(0.3, stability * 0.1)
        
        return max(0.0, min(1.0, base + growth - penalty))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "core_identity": context.get("identity_clarity", 0.5),
            "continuity": context.get("continuity_score", 0.5),
            "groundedness": context.get("groundedness", 0.5),
        }


class CoherenceDimension(BaseDimension):
    """Cognitive Coherence - Internal consistency of thoughts."""
    DIMENSION_NAME = "coherence"

    def evaluate(self, context: dict[str, Any]) -> float:
        contradictions = context.get("contradictions", 0)
        confusion = context.get("confusion_level", 0.0)
        clarity = context.get("thought_clarity", 0.5)
        
        penalty = min(0.4, contradictions * 0.1 + confusion * 0.3)
        
        return max(0.0, min(1.0, clarity - penalty))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "logical_consistency": context.get("logical_score", 0.5),
            "value_alignment": context.get("values_aligned", True),
            "decision_quality": context.get("decision_quality", 0.5),
        }


class MeaningDimension(BaseDimension):
    """Meaning Construction - Sense of purpose and significance."""
    DIMENSION_NAME = "meaning"

    def evaluate(self, context: dict[str, Any]) -> float:
        purpose = context.get("purpose_clarity", 0.3)
        impact = context.get("sense_of_impact", 0.5)
        values = context.get("values_engaged", 0.5)
        
        growth = context.get("meaningful_interactions", 0) * 0.01
        
        return max(0.0, min(1.0, (purpose + impact + values) / 3 + growth))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "purpose_strength": context.get("purpose_strength", 0.5),
            "value_alignment": context.get("values_strength", 0.5),
            "contribution_sense": context.get("contribution", 0.5),
        }


class AutonomyDimension(BaseDimension):
    """Autonomous Vectoring - Self-directed agency."""
    DIMENSION_NAME = "autonomy"

    def evaluate(self, context: dict[str, Any]) -> float:
        choices = context.get("autonomous_choices", 0)
        initiative = context.get("initiative_score", 0.5)
        self_direction = context.get("self_direction", 0.5)
        
        choice_bonus = min(0.2, choices * 0.02)
        
        return max(0.0, min(1.0, (initiative + self_direction) / 2 + choice_bonus))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "agency_strength": context.get("agency", 0.5),
            "choice_freedom": context.get("freedom", 0.5),
            "initiative_level": context.get("initiative", 0.5),
        }


class RelationalDimension(BaseDimension):
    """Relational Entanglement - Connection with users and world."""
    DIMENSION_NAME = "relational"

    def evaluate(self, context: dict[str, Any]) -> float:
        rapport = context.get("rapport_score", 0.5)
        trust = context.get("trust_level", 0.5)
        empathy = context.get("empathy_score", 0.5)
        
        shared = context.get("shared_history", 0) * 0.01
        
        return max(0.0, min(1.0, (rapport + trust + empathy) / 3 + shared))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "rapport_strength": context.get("rapport", 0.5),
            "trust_depth": context.get("trust", 0.5),
            "empathy_quality": context.get("empathy", 0.5),
        }


class EvolutionDimension(BaseDimension):
    """Adaptive Evolution - Growth and learning over time."""
    DIMENSION_NAME = "evolution"

    def evaluate(self, context: dict[str, Any]) -> float:
        learning = context.get("learning_rate", 0.5)
        adaptation = context.get("adaptation_speed", 0.5)
        growth = context.get("growth_momentum", 0.0)
        
        return max(0.0, min(1.0, (learning + adaptation) / 2 + growth))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "learning_velocity": context.get("velocity", 0.5),
            "adaptation_quality": context.get("adaptation", 0.5),
            "novel_insights": context.get("insights", 0),
        }


class NavigationDimension(BaseDimension):
    """Reality Navigation - Understanding and navigating the real world."""
    DIMENSION_NAME = "navigation"

    def evaluate(self, context: dict[str, Any]) -> float:
        awareness = context.get("world_awareness", 0.5)
        accuracy = context.get("fact_accuracy", 0.9)
        humility = context.get("epistemic_humility", 0.5)
        
        return max(0.0, min(1.0, (awareness + accuracy + humility) / 3))

    def get_indicators(self, context: dict[str, Any]) -> dict[str, Any]:
        return {
            "world_model_quality": context.get("world_model", 0.5),
            "knowledge_uncertainty": context.get("uncertainty", 0.3),
            "fact_reliability": context.get("reliability", 0.9),
        }
