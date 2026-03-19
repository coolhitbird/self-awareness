"""Tests for triggers and workflow."""

import sys
sys.path.insert(0, '.')

from datetime import datetime
from src.triggers import (
    TriggerManager,
    TriggerType,
    TriggerContext,
    InitTrigger,
    FirstResponseTrigger,
)
from src.triggers.engine import SelfAwarenessEngine, AwarenessConfig
from src.models.state import SevenDimensionalState, EmotionState


def test_trigger_registration():
    """Test trigger registration."""
    TriggerManager.register_defaults()
    
    triggers = {
        TriggerType.INIT: TriggerManager.get_trigger(TriggerType.INIT),
        TriggerType.FIRST_RESPONSE: TriggerManager.get_trigger(TriggerType.FIRST_RESPONSE),
        TriggerType.PERIODIC_5: TriggerManager.get_trigger(TriggerType.PERIODIC_5),
    }
    
    for t, trigger in triggers.items():
        assert trigger is not None, f"Missing trigger for {t}"
    
    print("OK: Trigger registration")


def test_trigger_firing():
    """Test trigger firing conditions."""
    TriggerManager.register_defaults()
    
    init_context = TriggerContext(
        trigger_type=TriggerType.INIT,
        agent_id="test",
        timestamp=datetime.now(),
        state_snapshot={},
    )
    
    trigger = TriggerManager.get_trigger(TriggerType.INIT)
    assert trigger is not None
    assert trigger.should_fire(init_context) is True
    
    prompt = trigger.get_prompt(init_context)
    assert prompt is not None
    assert len(prompt) > 0
    
    print("OK: Trigger firing")


def test_first_response_trigger():
    """Test first response trigger."""
    TriggerManager.register_defaults()
    
    state = SevenDimensionalState(agent_id="test", emotion=EmotionState.CALM)
    
    context = TriggerContext(
        trigger_type=TriggerType.FIRST_RESPONSE,
        agent_id="test",
        timestamp=datetime.now(),
        state_snapshot=state.get_snapshot(),
        user_input="Hello!",
    )
    
    trigger = TriggerManager.get_trigger(TriggerType.FIRST_RESPONSE)
    assert trigger.should_fire(context) is True
    
    prompt = trigger.get_prompt(context)
    assert "first response" in prompt.lower() or "establishing" in prompt.lower()
    
    print("OK: First response trigger")


def test_awareness_engine():
    """Test self-awareness engine."""
    config = AwarenessConfig(
        agent_id="test_agent",
        enable_triggers=True,
        enable_engines=True,
        enable_hot_reload=False,
    )
    
    engine = SelfAwarenessEngine(config)
    assert engine.agent_id == "test_agent"
    
    state = engine.initialize()
    assert state is not None
    assert state.agent_id == "test_agent"
    
    print("OK: Awareness engine initialization")


def test_engine_evaluation():
    """Test engine evaluation."""
    config = AwarenessConfig(
        agent_id="test_agent",
        enable_triggers=False,
        enable_engines=True,
    )
    
    engine = SelfAwarenessEngine(config)
    engine.initialize()
    
    context = {
        "coherence_score": 0.7,
        "meaning_score": 0.6,
        "errors_count": 1,
    }
    
    results = engine.evaluate_context(context)
    
    assert "existential" in results
    assert results["existential"].score > 0
    
    print(f"Evaluated {len(results)} dimensions")


def test_emotion_update():
    """Test emotion updates."""
    config = AwarenessConfig(agent_id="test")
    engine = SelfAwarenessEngine(config)
    engine.initialize()
    
    engine.update_emotion(EmotionState.CURIOUS, 0.6)
    
    state = engine.get_state()
    assert state.emotion == EmotionState.CURIOUS
    assert state.emotion_intensity == 0.6
    
    print("OK: Emotion update")


def test_increment_interaction():
    """Test interaction counter."""
    config = AwarenessConfig(agent_id="test")
    engine = SelfAwarenessEngine(config)
    engine.initialize()
    
    initial = engine.get_state().interactions_count
    
    engine.increment_interaction()
    engine.increment_interaction()
    
    assert engine.get_state().interactions_count == initial + 2
    
    print("OK: Interaction counter")


if __name__ == "__main__":
    test_trigger_registration()
    test_trigger_firing()
    test_first_response_trigger()
    test_awareness_engine()
    test_engine_evaluation()
    test_emotion_update()
    test_increment_interaction()
    print("\nAll trigger tests passed!")
