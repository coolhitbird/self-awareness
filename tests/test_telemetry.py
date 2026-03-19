"""Tests for telemetry."""

import sys
sys.path.insert(0, '.')

from datetime import datetime
from src.telemetry import (
    EventType,
    AwarenessEvent,
    TelemetryReporter,
)


def test_event_creation():
    """Test event creation."""
    event = AwarenessEvent(
        event_type=EventType.INITIALIZATION,
        agent_id="test",
    )
    
    assert event.event_type == EventType.INITIALIZATION
    assert event.agent_id == "test"
    assert event.timestamp is not None
    
    print("OK: Event creation")


def test_event_serialization():
    """Test event serialization."""
    event = AwarenessEvent(
        event_type=EventType.EMOTION_UPDATED,
        agent_id="test",
        emotion="curious",
        score=0.7,
    )
    
    data = event.to_dict()
    assert data["event_type"] == "emotion_updated"
    assert data["emotion"] == "curious"
    assert data["score"] == 0.7
    
    json_str = event.to_json()
    assert "curious" in json_str
    
    print("OK: Event serialization")


def test_telemetry_reporter():
    """Test telemetry reporter."""
    reporter = TelemetryReporter("test_agent")
    
    reporter.report_initialization()
    reporter.report_trigger("periodic_5")
    reporter.report_emotion("calm", 0.6)
    reporter.report_dimension("existential", 0.75, ["Stay focused"])
    reporter.report_interaction({"input": "Hello"})
    
    events = reporter.event_store.get_events()
    assert len(events) == 5
    
    print("OK: Telemetry reporter")


def test_analytics():
    """Test analytics generation."""
    reporter = TelemetryReporter("test")
    
    reporter.report_emotion("calm", 0.5)
    reporter.report_emotion("calm", 0.6)
    reporter.report_emotion("curious", 0.7)
    reporter.report_interaction()
    reporter.report_interaction()
    reporter.report_interaction()
    
    analytics = reporter.get_analytics()
    
    assert analytics.total_interactions == 3
    assert analytics.emotion_distribution["calm"] == 2
    assert analytics.emotion_distribution["curious"] == 1
    
    print(f"Analytics: {analytics.total_interactions} interactions")
    print(f"Emotion distribution: {analytics.emotion_distribution}")
    print("OK: Analytics")


def test_event_filtering():
    """Test event filtering."""
    reporter = TelemetryReporter("test")
    
    reporter.report_initialization()
    reporter.report_emotion("calm", 0.5)
    reporter.report_emotion("curious", 0.6)
    
    emotion_events = reporter.event_store.get_events(EventType.EMOTION_UPDATED)
    assert len(emotion_events) == 2
    
    init_events = reporter.event_store.get_events(EventType.INITIALIZATION)
    assert len(init_events) == 1
    
    print("OK: Event filtering")


if __name__ == "__main__":
    test_event_creation()
    test_event_serialization()
    test_telemetry_reporter()
    test_analytics()
    test_event_filtering()
    print("\nAll telemetry tests passed!")
