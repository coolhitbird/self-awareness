"""Propagation engine for multi-layer dimension system."""

from __future__ import annotations

from ..models.base import BaseProfile
from ..models.emotion import EmotionState, EmotionData
from ..models.behavior import BehaviorProfile
from ..models.dimensions import DimensionType
from .rules import (
    BASE_EMOTION_RULES,
    EMOTION_BEHAVIOR_RULES,
    EMOTION_DIMENSION_INFLUENCE,
    get_behavior_from_emotion,
    get_dimension_influence,
    combine_emotions,
)


class PropagationEngine:
    """Multi-layer propagation engine: Base → Emotion → Behavior → Cognition"""

    def __init__(self):
        self.base_emotion_rules = BASE_EMOTION_RULES
        self.emotion_behavior_rules = EMOTION_BEHAVIOR_RULES
        self.emotion_dimension_rules = EMOTION_DIMENSION_INFLUENCE

    def propagate(self, base: BaseProfile) -> tuple[EmotionData, BehaviorProfile, dict[str, float]]:
        """
        Complete propagation: Base → Emotion → Behavior → Cognition
        
        Returns:
            tuple: (emotion_state, behavior_profile, dimension_scores)
        """
        # Step 1: Base → Emotion
        emotion_state = self._calculate_emotion(base)

        # Step 2: Emotion → Behavior
        behavior = self._calculate_behavior(emotion_state)

        # Step 3: Emotion → Cognition (12 dimensions)
        dimensions = self._calculate_dimensions(base, emotion_state)

        return emotion_state, behavior, dimensions

    def _calculate_emotion(self, base: BaseProfile) -> EmotionData:
        """Calculate emotion state from base profile"""
        # Collect all emotion modifiers from base attributes
        increases = []
        decreases = []

        for attr in ["gender", "culture", "values", "personality", "identity"]:
            value = getattr(base, attr, "universal")
            rules = self.base_emotion_rules.get(attr, {}).get(value, {})
            
            increases.extend(rules.get("increases", []))
            decreases.extend(rules.get("decreases", []))

        # Calculate base emotion (simplified: use first increase or default to calm)
        if increases:
            base_emotion = increases[0]
        else:
            base_emotion = EmotionState.CALM

        # Calculate intensity based on modifier count
        intensity = 0.5 + (len(increases) * 0.05) - (len(decreases) * 0.03)
        intensity = max(0.1, min(1.0, intensity))

        # Detect combo (simplified: if multiple increases, could be combo)
        combo = []
        if len(increases) >= 2:
            combo = list(increases[:3])

        return EmotionData(
            current=base_emotion,
            intensity=intensity,
            combo=combo,
            trend="stable"
        )

    def _calculate_behavior(self, emotion: EmotionData) -> BehaviorProfile:
        """Calculate behavior from emotion state"""
        behavior_rules = self.emotion_behavior_rules.get(
            emotion.current.value,
            EMOTION_BEHAVIOR_RULES["calm"]
        )

        # Adjust based on intensity
        if emotion.is_intense():
            # Intense emotions amplify certain behaviors
            if behavior_rules.get("response_speed") == "moderate":
                behavior_rules["response_speed"] = "fast"

        return BehaviorProfile(
            decision_style=behavior_rules.get("decision_style", "moderate"),
            communication=behavior_rules.get("communication", "neutral"),
            response_speed=behavior_rules.get("response_speed", "moderate"),
            tone_preference=behavior_rules.get("tone_preference", "neutral")
        )

    def _calculate_dimensions(self, base: BaseProfile, emotion: EmotionData) -> dict[str, float]:
        """Calculate 12 dimension scores"""
        # Start with base scores
        dimensions = {dim: 0.5 for dim in DimensionType.all_dimensions()}

        # Apply emotion influence
        emotion_influence = self.emotion_dimension_rules.get(
            emotion.current.value, 
            {}
        )

        for dim_name, influence in emotion_influence.items():
            if dim_name in dimensions:
                dimensions[dim_name] = max(0.0, min(1.0, dimensions[dim_name] + influence))

        # Apply subtle adjustments based on base profile
        # (This could be expanded with more rules)

        return dimensions

    def update_emotion(self, current: EmotionState, new: EmotionState) -> EmotionData:
        """Update emotion when new emotion is detected"""
        combo = []
        
        # Detect if this creates a combo
        if current != new:
            combo_emotion = combine_emotions(current, new)
            if combo_emotion != new and combo_emotion != current:
                combo = [current, new]
                return EmotionData(
                    current=combo_emotion,
                    intensity=0.7,
                    combo=combo,
                    trend="rising"
                )

        # Simple transition
        return EmotionData(
            current=new,
            intensity=0.5,
            combo=[],
            trend="stable"
        )

    def apply_dimension_changes(
        self, 
        current_dims: dict[str, float], 
        emotion: EmotionData
    ) -> dict[str, float]:
        """Apply emotion-based dimension changes to existing state"""
        dimensions = current_dims.copy()
        
        influences = get_dimension_influence(emotion.current)
        
        for dim_name, influence in influences.items():
            if dim_name in dimensions:
                dimensions[dim_name] = max(0.0, min(1.0, dimensions[dim_name] + influence))
        
        return dimensions

    def get_emotion_tendency(self, base: BaseProfile) -> dict[str, float]:
        """Get tendency scores for each emotion based on base profile"""
        tendency = {e.value: 0.5 for e in EmotionState}

        # Accumulate influences
        for attr in ["gender", "culture", "values", "personality", "identity"]:
            value = getattr(base, attr, "universal")
            rules = self.base_emotion_rules.get(attr, {}).get(value, {})
            
            for e in rules.get("increases", []):
                tendency[e.value] += 0.15
            
            for e in rules.get("decreases", []):
                tendency[e.value] -= 0.1

        # Normalize
        for key in tendency:
            tendency[key] = max(0.1, min(0.9, tendency[key]))

        return tendency


# Singleton instance
_engine: PropagationEngine | None = None


def get_engine() -> PropagationEngine:
    """Get propagation engine singleton"""
    global _engine
    if _engine is None:
        _engine = PropagationEngine()
    return _engine
