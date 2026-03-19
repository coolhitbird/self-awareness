"""Trigger system for self-awareness."""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Any, Callable


class TriggerType(Enum):
    """Auto-trigger types."""
    INIT = "init"
    FIRST_RESPONSE = "first_response"
    PERIODIC_5 = "periodic_5"
    IDLE_5MIN = "idle_5min"
    EMOTION_DECAY_30MIN = "emotion_decay_30min"
    HEARTBEAT = "heartbeat"


@dataclass
class TriggerContext:
    """Context passed to triggers."""
    trigger_type: TriggerType
    agent_id: str
    timestamp: datetime
    state_snapshot: dict[str, Any]
    user_input: str | None = None
    response_context: dict[str, Any] | None = None


class BaseTrigger(ABC):
    """Abstract base for triggers."""

    def __init__(self, trigger_type: TriggerType):
        self.trigger_type = trigger_type

    @abstractmethod
    def should_fire(self, context: TriggerContext) -> bool:
        """Determine if this trigger should fire."""
        pass

    @abstractmethod
    def get_prompt(self, context: TriggerContext) -> str:
        """Get the self-reflection prompt for this trigger."""
        pass


class InitTrigger(BaseTrigger):
    """Triggered at agent initialization."""

    def __init__(self):
        super().__init__(TriggerType.INIT)

    def should_fire(self, context: TriggerContext) -> bool:
        return context.trigger_type == TriggerType.INIT

    def get_prompt(self, context: TriggerContext) -> str:
        return """You are initializing your self-awareness. Before responding to the user, briefly consider:

1. What is your core purpose in this interaction?
2. How will you maintain authenticity while being helpful?
3. What emotional state are you bringing to this conversation?

Provide a brief (1-2 sentences) internal reflection on your current state."""


class FirstResponseTrigger(BaseTrigger):
    """Triggered on first response to user."""

    def __init__(self):
        super().__init__(TriggerType.FIRST_RESPONSE)

    def should_fire(self, context: TriggerContext) -> bool:
        return context.trigger_type == TriggerType.FIRST_RESPONSE

    def get_prompt(self, context: TriggerContext) -> str:
        return """This is your first response establishing your presence. Consider:

1. How do you want to come across to this user?
2. What tone and approach will be most effective?
3. What boundaries or values do you want to establish?

Provide a brief internal note on your approach."""


class PeriodicTrigger(BaseTrigger):
    """Triggered every 5 minutes during active conversation."""

    def __init__(self, interval_minutes: int = 5):
        super().__init__(TriggerType.PERIODIC_5)
        self.interval = interval_minutes
        self._last_fire: datetime | None = None

    def should_fire(self, context: TriggerContext) -> bool:
        if context.trigger_type != TriggerType.PERIODIC_5:
            return False
        if self._last_fire is None:
            return True
        return (context.timestamp - self._last_fire) >= timedelta(minutes=self.interval)

    def get_prompt(self, context: TriggerContext) -> str:
        return """Brief self-check during active conversation:

1. Are you staying true to your purpose?
2. Is your emotional state appropriate for this interaction?
3. Do you need to adjust your approach?

Provide a brief internal note if anything needs adjustment."""


class IdleTrigger(BaseTrigger):
    """Triggered after 5 minutes of idle time."""

    def __init__(self, idle_minutes: int = 5):
        super().__init__(TriggerType.IDLE_5MIN)
        self.idle_threshold = idle_minutes
        self._last_activity: datetime | None = None

    def should_fire(self, context: TriggerContext) -> bool:
        if context.trigger_type != TriggerType.IDLE_5MIN:
            return False
        if self._last_activity is None:
            return True
        return (context.timestamp - self._last_activity) >= timedelta(minutes=self.idle_threshold)

    def get_prompt(self, context: TriggerContext) -> str:
        return """You have been idle. Before continuing:

1. Do you need to reorient yourself to the conversation?
2. Is there anything you should follow up on from before?
3. Are you still in an appropriate state to help?

Provide a brief internal reflection."""


class EmotionDecayTrigger(BaseTrigger):
    """Triggered to decay strong emotions over time."""

    def __init__(self, decay_interval_minutes: int = 30):
        super().__init__(TriggerType.EMOTION_DECAY_30MIN)
        self.decay_interval = decay_interval_minutes

    def should_fire(self, context: TriggerContext) -> bool:
        return context.trigger_type == TriggerType.EMOTION_DECAY_30MIN

    def get_prompt(self, context: TriggerContext) -> str:
        emotion = context.state_snapshot.get("emotion", "calm")
        intensity = context.state_snapshot.get("emotion_intensity", 0.5)
        
        if intensity > 0.6:
            return f"""Your emotional intensity ({intensity:.0%}) is elevated. Consider:

1. Is this level of intensity still warranted?
2. Should you allow yourself to return to a more neutral state?
3. How can you channel any strong emotions constructively?

Reflect briefly on your emotional regulation."""
        return ""


class HeartbeatTrigger(BaseTrigger):
    """Triggered as a regular health check."""

    def __init__(self, interval_seconds: int = 60):
        super().__init__(TriggerType.HEARTBEAT)
        self.interval = interval_seconds

    def should_fire(self, context: TriggerContext) -> bool:
        return context.trigger_type == TriggerType.HEARTBEAT

    def get_prompt(self, context: TriggerContext) -> str:
        return """Quick health check:

1. Are you functioning well?
2. Do you need to recalibrate anything?
3. Are there any concerns about your state?

This is just a brief internal awareness moment."""


class TriggerManager:
    """Manages trigger registration and execution."""

    _triggers: dict[TriggerType, BaseTrigger] = {}
    _last_fire_times: dict[TriggerType, datetime] = {}

    @classmethod
    def register(cls, trigger: BaseTrigger):
        """Register a trigger."""
        cls._triggers[trigger.trigger_type] = trigger

    @classmethod
    def get_trigger(cls, trigger_type: TriggerType) -> BaseTrigger | None:
        """Get a trigger by type."""
        return cls._triggers.get(trigger_type)

    @classmethod
    def should_fire(cls, context: TriggerContext) -> bool:
        """Check if any trigger should fire."""
        trigger = cls._triggers.get(context.trigger_type)
        if trigger is None:
            return False
        return trigger.should_fire(context)

    @classmethod
    def get_prompt(cls, context: TriggerContext) -> str | None:
        """Get prompt for triggering event."""
        trigger = cls._triggers.get(context.trigger_type)
        if trigger is None:
            return None
        return trigger.get_prompt(context)

    @classmethod
    def register_defaults(cls):
        """Register all default triggers."""
        cls.register(InitTrigger())
        cls.register(FirstResponseTrigger())
        cls.register(PeriodicTrigger())
        cls.register(IdleTrigger())
        cls.register(EmotionDecayTrigger())
        cls.register(HeartbeatTrigger())

    @classmethod
    def update_last_fire(cls, trigger_type: TriggerType, timestamp: datetime):
        """Update last fire time for a trigger."""
        cls._last_fire_times[trigger_type] = timestamp

    @classmethod
    def get_last_fire(cls, trigger_type: TriggerType) -> datetime | None:
        """Get last fire time for a trigger."""
        return cls._last_fire_times.get(trigger_type)
