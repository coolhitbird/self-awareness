"""Observability and telemetry for self-awareness."""

from __future__ import annotations

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any


class EventType(Enum):
    """Types of self-awareness events."""
    INITIALIZATION = "initialization"
    TRIGGER_FIRED = "trigger_fired"
    STATE_CHANGED = "state_changed"
    EMOTION_UPDATED = "emotion_updated"
    DIMENSION_EVALUATED = "dimension_evaluated"
    INTERACTION = "interaction"
    COGNITION_UPDATED = "cognition_updated"
    ERROR = "error"


@dataclass
class AwarenessEvent:
    """A single awareness event."""
    event_type: EventType
    timestamp: datetime = field(default_factory=datetime.now)
    agent_id: str = ""
    trigger_type: str | None = None
    dimension: str | None = None
    emotion: str | None = None
    score: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    recommendations: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["timestamp"] = self.timestamp.isoformat()
        data["event_type"] = self.event_type.value
        return data

    def to_json(self) -> str:
        """Convert to JSON string."""
        return json.dumps(self.to_dict(), ensure_ascii=False)


@dataclass
class Analytics:
    """Analytics data."""
    agent_id: str
    total_interactions: int = 0
    total_triggers_fired: int = 0
    emotion_distribution: dict[str, int] = field(default_factory=dict)
    dimension_averages: dict[str, float] = field(default_factory=dict)
    stability_trend: list[float] = field(default_factory=list)
    last_updated: datetime = field(default_factory=datetime.now)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        data = asdict(self)
        data["last_updated"] = self.last_updated.isoformat()
        return data


class EventStore:
    """Storage for awareness events."""

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path
        self._events: list[AwarenessEvent] = []
        self._max_events = 1000

    def record(self, event: AwarenessEvent):
        """Record an event."""
        self._events.append(event)
        
        if len(self._events) > self._max_events:
            self._events.pop(0)
        
        if self.storage_path:
            self._persist()

    def get_events(
        self,
        event_type: EventType | None = None,
        limit: int = 100,
    ) -> list[AwarenessEvent]:
        """Get recorded events."""
        events = self._events
        
        if event_type:
            events = [e for e in events if e.event_type == event_type]
        
        return events[-limit:]

    def get_recent(self, count: int = 10) -> list[AwarenessEvent]:
        """Get most recent events."""
        return self._events[-count:]

    def clear(self):
        """Clear all events."""
        self._events.clear()

    def _persist(self):
        """Persist events to storage."""
        if not self.storage_path:
            return
        
        self.storage_path.parent.mkdir(parents=True, exist_ok=True)
        
        data = [e.to_dict() for e in self._events]
        self.storage_path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self):
        """Load events from storage."""
        if not self.storage_path or not self.storage_path.exists():
            return
        
        try:
            data = json.loads(self.storage_path.read_text(encoding="utf-8"))
            self._events = [
                self._dict_to_event(d) for d in data
            ]
        except (json.JSONDecodeError, KeyError):
            pass

    def _dict_to_event(self, data: dict[str, Any]) -> AwarenessEvent:
        """Convert dictionary to event."""
        data["event_type"] = EventType(data["event_type"])
        data["timestamp"] = datetime.fromisoformat(data["timestamp"])
        return AwarenessEvent(**data)


class TelemetryReporter:
    """Reports telemetry data."""

    def __init__(self, agent_id: str):
        self.agent_id = agent_id
        self.event_store = EventStore()

    def report_initialization(self):
        """Report agent initialization."""
        event = AwarenessEvent(
            event_type=EventType.INITIALIZATION,
            agent_id=self.agent_id,
            metadata={"version": "0.5.4"},  # 与 src/__init__.py __version__ 保持一致
        )
        self.event_store.record(event)

    def report_trigger(self, trigger_type: str, prompt: str | None = None):
        """Report trigger fired."""
        event = AwarenessEvent(
            event_type=EventType.TRIGGER_FIRED,
            agent_id=self.agent_id,
            trigger_type=trigger_type,
            metadata={"prompt_length": len(prompt) if prompt else 0},
        )
        self.event_store.record(event)

    def report_state_change(self, old_state: dict, new_state: dict):
        """Report state change."""
        changes = {}
        for key in new_state:
            if key in old_state and old_state[key] != new_state[key]:
                changes[key] = {"from": old_state[key], "to": new_state[key]}

        event = AwarenessEvent(
            event_type=EventType.STATE_CHANGED,
            agent_id=self.agent_id,
            metadata={"changes": changes},
        )
        self.event_store.record(event)

    def report_emotion(self, emotion: str, intensity: float):
        """Report emotion update."""
        event = AwarenessEvent(
            event_type=EventType.EMOTION_UPDATED,
            agent_id=self.agent_id,
            emotion=emotion,
            metadata={"intensity": intensity},
        )
        self.event_store.record(event)

    def report_dimension(
        self,
        dimension: str,
        score: float,
        recommendations: list[str] | None = None,
    ):
        """Report dimension evaluation."""
        event = AwarenessEvent(
            event_type=EventType.DIMENSION_EVALUATED,
            agent_id=self.agent_id,
            dimension=dimension,
            score=score,
            recommendations=recommendations or [],
        )
        self.event_store.record(event)

    def report_interaction(self, context: dict[str, Any] | None = None):
        """Report an interaction."""
        event = AwarenessEvent(
            event_type=EventType.INTERACTION,
            agent_id=self.agent_id,
            metadata=context or {},
        )
        self.event_store.record(event)

    def get_analytics(self) -> Analytics:
        """Generate analytics from events."""
        analytics = Analytics(agent_id=self.agent_id)
        
        events = self.event_store.get_events(limit=10000)
        
        for event in events:
            if event.event_type == EventType.INTERACTION:
                analytics.total_interactions += 1
            elif event.event_type == EventType.TRIGGER_FIRED:
                analytics.total_triggers_fired += 1
            elif event.event_type == EventType.EMOTION_UPDATED:
                emotion = event.emotion or "unknown"
                analytics.emotion_distribution[emotion] = \
                    analytics.emotion_distribution.get(emotion, 0) + 1
            elif event.event_type == EventType.DIMENSION_EVALUATED:
                dim = event.dimension or "unknown"
                if dim not in analytics.dimension_averages:
                    analytics.dimension_averages[dim] = []
                if event.score is not None:
                    analytics.dimension_averages[dim].append(event.score)
        
        for dim, scores in analytics.dimension_averages.items():
            if scores:
                analytics.dimension_averages[dim] = sum(scores) / len(scores)
            else:
                analytics.dimension_averages[dim] = 0.0

        analytics.last_updated = datetime.now()
        return analytics

    def export_events(self, path: Path):
        """Export events to file."""
        events = self.event_store.get_events(limit=10000)
        data = [e.to_dict() for e in events]
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
