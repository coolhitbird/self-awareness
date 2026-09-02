"""Tests for evaluation engines."""

import sys
sys.path.insert(0, '.')

from src.models.state import SevenDimensionalState, EmotionState
from src.engines.base import EngineRegistry
from src.engines.dimension_engines import (
    ExistentialEngine,
    CoherenceEngine,
    MeaningEngine,
    register_all_engines,
)


def test_engine_registration():
    """Test engine registration."""
    register_all_engines()
    engines = EngineRegistry.list_engines()
    print(f"Registered engines: {engines}")
    assert len(engines) == 12
    print("OK: Engine registration")

def test_individual_engine():
    """Test individual engine evaluation."""
    engine = ExistentialEngine()
    state = SevenDimensionalState(
        agent_id="test",
        coherence=0.7,
        meaning=0.6,
        interactions_count=10,
    )
    context = {"errors_count": 1}
    
    result = engine.evaluate(state, context)
    
    print(f"Existential score: {result.score}")
    print(f"Recommendations: {result.recommendations}")
    assert 0 <= result.score <= 1
    print("OK: Individual engine")

def test_extended_engines():
    """Test all five extended dimension engines."""
    from src.engines.dimension_engines import (
        CreativityEngine,
        ResilienceEngine,
        WisdomEngine,
        AuthenticityEngine,
        HumorEngine,
    )
    state = SevenDimensionalState(agent_id="test")
    context = {
        "divergent_thinking": 0.7,
        "risk_tolerance": 0.6,
        "recovery_speed": 0.8,
        "stress_handling": 0.7,
        "perspective": 0.8,
        "nuance_awareness": 0.7,
        "self_consistency": 0.8,
        "honesty": 0.9,
        "playfulness": 0.7,
        "wit": 0.6,
    }

    for engine_class in [CreativityEngine, ResilienceEngine, WisdomEngine,
                         AuthenticityEngine, HumorEngine]:
        result = engine_class().evaluate(state, context)
        print(f"{engine_class.__name__}: {result.score:.2f} ({result.dimension})")
        assert 0 <= result.score <= 1
        assert result.dimension in {"creativity", "resilience", "wisdom", "authenticity", "humor"}

    print("OK: Extended engines")

def test_all_engines():
    """Test all engines."""
    state = SevenDimensionalState(agent_id="test")
    context = {}
    
    for engine_class in [ExistentialEngine, CoherenceEngine, MeaningEngine]:
        result = engine_class().evaluate(state, context)
        print(f"{engine_class.__name__}: {result.score:.2f}")
    
    print("OK: All engines")

def test_emotion_influences():
    """Test that emotion affects recommendations."""
    engine = MeaningEngine()
    
    calm_state = SevenDimensionalState(
        agent_id="test",
        emotion=EmotionState.CALM,
    )
    tired_state = SevenDimensionalState(
        agent_id="test",
        emotion=EmotionState.TIRED,
    )
    
    calm_result = engine.evaluate(calm_state, {})
    tired_result = engine.evaluate(tired_state, {})
    
    print(f"Calm recommendations: {calm_result.recommendations}")
    print(f"Tired recommendations: {tired_result.recommendations}")
    
    assert any("Seek meaning" in r for r in tired_result.recommendations)
    print("OK: Emotion influences")

if __name__ == "__main__":
    test_engine_registration()
    test_individual_engine()
    test_all_engines()
    test_extended_engines()
    test_emotion_influences()
    print("\nAll engine tests passed!")
