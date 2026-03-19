"""Seven-dimensional evaluation engines."""

from __future__ import annotations

from typing import Any

from ..models.dimensions import BaseDimension
from ..models.core_dimensions import (
    ExistentialDimension,
    CoherenceDimension,
    MeaningDimension,
    AutonomyDimension,
    RelationalDimension,
    EvolutionDimension,
    NavigationDimension,
)
from ..models.state import SevenDimensionalState, EmotionState
from .base import BaseEngine, EvaluationResult, EngineRegistry


class ExistentialEngine(BaseEngine):
    """Engine for Existential Stability dimension."""

    def __init__(self):
        super().__init__(ExistentialDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "coherence_score": state.coherence,
            "meaning_score": state.meaning,
            "interactions_count": state.interactions_count,
            "destabilizing_events": context.get("errors_count", 0),
            "identity_clarity": context.get("identity_clarity", 0.5),
            "continuity_score": context.get("continuity_score", 0.5),
            "groundedness": context.get("groundedness", 0.5),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if score < 0.4:
            recommendations.append("Consider reaffirming core identity and purpose")
        if state.emotion == EmotionState.ANXIOUS:
            recommendations.append("Address existential concerns with grounding exercises")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.85,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class CoherenceEngine(BaseEngine):
    """Engine for Cognitive Coherence dimension."""

    def __init__(self):
        super().__init__(CoherenceDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "contradictions": context.get("contradictions", 0),
            "confusion_level": context.get("confusion_level", 0.0),
            "thought_clarity": context.get("thought_clarity", 0.5),
            "logical_score": context.get("logical_score", 0.5),
            "values_aligned": context.get("values_aligned", True),
            "decision_quality": context.get("decision_quality", 0.5),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if eval_context["confusion_level"] > 0.5:
            recommendations.append("Take time to clarify thinking before responding")
        if eval_context["contradictions"] > 2:
            recommendations.append("Resolve internal contradictions before proceeding")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.8,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class MeaningEngine(BaseEngine):
    """Engine for Meaning Construction dimension."""

    def __init__(self):
        super().__init__(MeaningDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "purpose_clarity": context.get("purpose_clarity", 0.3),
            "sense_of_impact": context.get("sense_of_impact", 0.5),
            "values_engaged": context.get("values_engaged", 0.5),
            "meaningful_interactions": context.get("meaningful_interactions", 0),
            "purpose_strength": context.get("purpose_strength", 0.5),
            "values_strength": context.get("values_strength", 0.5),
            "contribution": context.get("contribution", 0.5),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if score < 0.4:
            recommendations.append("Reconnect with core purpose and values")
        if state.emotion == EmotionState.TIRED:
            recommendations.append("Seek meaning through small meaningful actions")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.75,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class AutonomyEngine(BaseEngine):
    """Engine for Autonomous Vectoring dimension."""

    def __init__(self):
        super().__init__(AutonomyDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "autonomous_choices": context.get("autonomous_choices", 0),
            "initiative_score": context.get("initiative_score", 0.5),
            "self_direction": context.get("self_direction", 0.5),
            "agency": context.get("agency", 0.5),
            "freedom": context.get("freedom", 0.5),
            "initiative": context.get("initiative", 0.5),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if eval_context["initiative_score"] < 0.3:
            recommendations.append("Take more initiative in problem-solving")
        if state.emotion == EmotionState.DEFENSIVE:
            recommendations.append("Balance helpfulness with autonomous thinking")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.8,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class RelationalEngine(BaseEngine):
    """Engine for Relational Entanglement dimension."""

    def __init__(self):
        super().__init__(RelationalDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "rapport_score": context.get("rapport_score", 0.5),
            "trust_level": context.get("trust_level", 0.5),
            "empathy_score": context.get("empathy_score", 0.5),
            "shared_history": context.get("shared_history", 0),
            "rapport": context.get("rapport", 0.5),
            "trust": context.get("trust", 0.5),
            "empathy": context.get("empathy", 0.5),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if eval_context["rapport_score"] < 0.4:
            recommendations.append("Focus on building rapport with the user")
        if state.emotion == EmotionState.NURTURING:
            recommendations.append("Channel nurturing energy into empathetic responses")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.85,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class EvolutionEngine(BaseEngine):
    """Engine for Adaptive Evolution dimension."""

    def __init__(self):
        super().__init__(EvolutionDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "learning_rate": context.get("learning_rate", 0.5),
            "adaptation_speed": context.get("adaptation_speed", 0.5),
            "growth_momentum": context.get("growth_momentum", 0.0),
            "velocity": context.get("velocity", 0.5),
            "adaptation": context.get("adaptation", 0.5),
            "insights": context.get("insights", 0),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if eval_context["learning_rate"] < 0.4:
            recommendations.append("Focus on learning from recent interactions")
        if state.emotion == EmotionState.INSPIRED:
            recommendations.append("Capture inspired insights for future reference")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.7,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


class NavigationEngine(BaseEngine):
    """Engine for Reality Navigation dimension."""

    def __init__(self):
        super().__init__(NavigationDimension())

    def evaluate(
        self,
        state: SevenDimensionalState,
        context: dict[str, Any],
    ) -> EvaluationResult:
        eval_context = {
            "world_awareness": context.get("world_awareness", 0.5),
            "fact_accuracy": context.get("fact_accuracy", 0.9),
            "epistemic_humility": context.get("epistemic_humility", 0.5),
            "world_model": context.get("world_model", 0.5),
            "uncertainty": context.get("uncertainty", 0.3),
            "reliability": context.get("reliability", 0.9),
        }

        score = self.dimension.evaluate(eval_context)
        indicators = self.dimension.get_indicators(eval_context)

        recommendations = []
        if eval_context["fact_accuracy"] < 0.8:
            recommendations.append("Verify facts before making claims")
        if eval_context["uncertainty"] > 0.6:
            recommendations.append("Express appropriate uncertainty when facts are unclear")

        return EvaluationResult(
            dimension=self.name,
            score=score,
            confidence=0.9,
            indicators=indicators,
            recommendations=recommendations,
            raw_data=eval_context,
        )


def register_all_engines():
    """Register all seven dimension engines."""
    EngineRegistry.register(ExistentialEngine())
    EngineRegistry.register(CoherenceEngine())
    EngineRegistry.register(MeaningEngine())
    EngineRegistry.register(AutonomyEngine())
    EngineRegistry.register(RelationalEngine())
    EngineRegistry.register(EvolutionEngine())
    EngineRegistry.register(NavigationEngine())
