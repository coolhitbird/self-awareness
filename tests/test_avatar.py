"""Tests for avatar system."""

import sys
sys.path.insert(0, '.')

from src.avatar import (
    get_kaomoji,
    get_random_kaomoji,
    format_avatar,
    create_agent_avatar,
    AvatarGenerator,
)
from src.models.state import EmotionState


def test_kaomoji_mapping():
    """Test kaomoji mapping."""
    for emotion in EmotionState:
        kaomoji = get_kaomoji(emotion)
        assert kaomoji is not None
        assert len(kaomoji) > 0
        print(f"{emotion.value}: {kaomoji}")
    
    print("OK: Kaomoji mapping")


def test_random_kaomoji():
    """Test random kaomoji selection."""
    kaomojis = set()
    for _ in range(10):
        kaomojis.add(get_random_kaomoji(EmotionState.CALM))
    
    print(f"Got {len(kaomojis)} unique kaomojis from 10 picks")
    print("OK: Random kaomoji")


def test_format_avatar():
    """Test avatar formatting."""
    avatar = format_avatar(EmotionState.ENGAGED, 0.8)
    print(f"Avatar: {avatar}")
    assert "[😊]" in avatar or "!" in avatar
    
    avatar_calm = format_avatar(EmotionState.CALM, 0.3)
    print(f"Calm avatar: {avatar_calm}")
    assert len(avatar_calm) > 0
    
    print("OK: Format avatar")


def test_create_agent_avatar():
    """Test convenience function."""
    text = create_agent_avatar(EmotionState.CONFIDENT, 0.7, format="text")
    print(f"Text avatar: {text}")
    
    svg = create_agent_avatar(EmotionState.CURIOUS, 0.5, format="svg")
    assert "<svg" in svg
    
    html = create_agent_avatar(EmotionState.TIRED, 0.4, format="html")
    assert "<div" in html
    
    print("OK: Create agent avatar")


def test_avatar_generator():
    """Test avatar generator."""
    gen = AvatarGenerator("default")
    
    svg = gen.generate_svg("(^_^)")
    assert 'xmlns="http://www.w3.org/2000/svg"' in svg
    assert "(^_^)" in svg
    
    css = gen.generate_css("(>_<)")
    assert ".agent-avatar" in css
    
    gen_dark = AvatarGenerator("dark")
    svg_dark = gen_dark.generate_svg("(T_T)")
    assert "#1a1a2e" in svg_dark
    
    print("OK: Avatar generator")


def test_avatar_prompt():
    """Test avatar generation prompt."""
    state = {
        "emotion": "frustrated",
        "emotion_indicator": "[😤]",
    }
    
    prompt = AvatarGenerator.generate_prompt(state)
    assert "frustrated" in prompt
    assert "😤" in prompt
    
    print(f"Prompt: {prompt[:50]}...")
    print("OK: Avatar prompt")


if __name__ == "__main__":
    test_kaomoji_mapping()
    test_random_kaomoji()
    test_format_avatar()
    test_create_agent_avatar()
    test_avatar_generator()
    test_avatar_prompt()
    print("\nAll avatar tests passed!")
