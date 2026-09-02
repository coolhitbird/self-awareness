"""Tests for models package."""

import sys
sys.path.insert(0, 'src')

from models import (
    DimensionRegistry,
    SevenDimensionalState,
    TwelveDimensionalState,
    StateManager,
    EmotionState,
    EMOTION_EMOJI,
    DimensionType,
)


def test_dimension_registry():
    """Test dimension registry."""
    dims = DimensionRegistry.list_dimensions()
    print(f"Registered dimensions: {dims}")
    assert len(dims) >= 12
    print("OK: Dimension registry")

def test_twelve_dimensions():
    """Test that all twelve dimensions exist."""
    state = TwelveDimensionalState(agent_id="test")
    names = DimensionType.all_dimensions()
    assert len(names) == 12
    for name in names:
        assert state.get_score(name) == 0.5
    print(f"OK: Twelve dimensions: {names}")

    from models import CreativityDimension, ResilienceDimension, \
        WisdomDimension, AuthenticityDimension, HumorDimension
    assert CreativityDimension().DIMENSION_NAME == "creativity"
    assert HumorDimension().DIMENSION_NAME == "humor"
    print("OK: Extended dimension classes")

def test_state_creation():
    """Test state creation."""
    state = SevenDimensionalState(agent_id="test")
    assert state.agent_id == "test"
    assert state.overall_stability == 0.5
    assert state.emotion == EmotionState.CALM
    print("OK: State creation")

def test_state_update():
    """Test state updates."""
    state = SevenDimensionalState(agent_id="test")
    state.set_score("existential", 0.8)
    assert state.get_score("existential") == 0.8
    
    state.update_from_context({
        "coherence": 0.6,
        "emotion": "curious",
        "emotion_intensity": 0.7,
    })
    assert state.get_score("coherence") == 0.6
    assert state.emotion == EmotionState.CURIOUS
    assert state.emotion_intensity == 0.7
    print("OK: State updates")

def test_emotion_indicator():
    """Test emotion indicators."""
    state = SevenDimensionalState(agent_id="test")
    
    for emotion, emoji in EMOTION_EMOJI.items():
        state.emotion = emotion
        indicator = state.to_indicator()
        assert indicator == emoji
    print("OK: Emotion indicators")

def test_state_manager():
    """Test state manager."""
    manager = StateManager("test")
    
    manager.increment_interaction()
    manager.increment_interaction()
    assert manager.current_state.interactions_count == 2
    
    manager.transition_emotion(EmotionState.ANXIOUS, 0.8)
    assert manager.current_state.emotion == EmotionState.ANXIOUS
    
    manager.decay_emotion(0.3)
    assert manager.current_state.emotion_intensity == 0.5
    
    print("OK: State manager")

def test_weakest_strongest():
    """Test dimension weakest/strongest."""
    state = SevenDimensionalState(agent_id="test")
    state.existential = 0.3
    state.coherence = 0.9
    
    assert state.weakest_dimension == "existential"
    assert state.strongest_dimension == "coherence"
    print("OK: Weakest/strongest")

def test_snapshot():
    """Test state snapshot."""
    state = SevenDimensionalState(agent_id="test", emotion=EmotionState.ENGAGED)
    snapshot = state.get_snapshot()
    
    assert snapshot["agent_id"] == "test"
    assert snapshot["emotion"] == "engaged"
    assert snapshot["emotion_indicator"] == "[😊]"
    print("OK: State snapshot")

if __name__ == "__main__":
    test_dimension_registry()
    test_twelve_dimensions()
    test_state_creation()
    test_state_update()
    test_emotion_indicator()
    test_state_manager()
    test_weakest_strongest()
    test_snapshot()
    print("\nAll model tests passed!")
