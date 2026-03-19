"""Trigger system for self-awareness."""

from .base import (
    TriggerType,
    TriggerContext,
    BaseTrigger,
    InitTrigger,
    FirstResponseTrigger,
    PeriodicTrigger,
    IdleTrigger,
    EmotionDecayTrigger,
    HeartbeatTrigger,
    TriggerManager,
)
from .engine import SelfAwarenessEngine, AwarenessConfig

__all__ = [
    "TriggerType",
    "TriggerContext",
    "BaseTrigger",
    "InitTrigger",
    "FirstResponseTrigger",
    "PeriodicTrigger",
    "IdleTrigger",
    "EmotionDecayTrigger",
    "HeartbeatTrigger",
    "TriggerManager",
    "SelfAwarenessEngine",
    "AwarenessConfig",
]
