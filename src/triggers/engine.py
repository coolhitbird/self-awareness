"""Self-awareness workflow engine."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from ..cognition import CognitionReader, CognitionWriter
from ..models import SevenDimensionalState, StateManager, EmotionState
from ..engines import (
    EngineRegistry,
    register_all_engines,
    EvaluationResult,
)
from .base import TriggerManager, TriggerType, TriggerContext


@dataclass
class AwarenessConfig:
    """Configuration for self-awareness engine."""
    agent_id: str
    cognition_path: Path | None = None
    enable_triggers: bool = True
    enable_engines: bool = True
    enable_hot_reload: bool = True
    emotion_decay_rate: float = 0.1
    check_interval_seconds: int = 60


class SelfAwarenessEngine:
    """Main self-awareness engine coordinating all components."""

    def __init__(self, config: AwarenessConfig):
        self.config = config
        self.agent_id = config.agent_id
        
        self.cognition_reader = CognitionReader(
            config.agent_id,
            config.cognition_path,
        )
        self.cognition_writer = CognitionWriter(
            config.agent_id,
            config.cognition_path,
        )
        
        self.state_manager = StateManager(config.agent_id)
        
        if config.enable_engines:
            register_all_engines()
        
        if config.enable_triggers:
            TriggerManager.register_defaults()
        
        self._initialized = False
        self._last_cognition_mtime: dict[Path, float] = {}

    def initialize(self) -> SevenDimensionalState:
        """Initialize self-awareness on agent startup."""
        context = TriggerContext(
            trigger_type=TriggerType.INIT,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
        )

        if TriggerManager.should_fire(context):
            prompt = TriggerManager.get_prompt(context)
            if prompt:
                self._process_reflection(prompt, context)

        self._initialized = True
        return self.state_manager.current_state

    def on_first_response(self, user_input: str) -> str | None:
        """Process first response to user."""
        context = TriggerContext(
            trigger_type=TriggerType.FIRST_RESPONSE,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
            user_input=user_input,
        )

        if TriggerManager.should_fire(context):
            return TriggerManager.get_prompt(context)
        return None

    def periodic_check(self) -> str | None:
        """Perform periodic self-awareness check."""
        if self.config.enable_hot_reload:
            self._check_cognition_updates()

        context = TriggerContext(
            trigger_type=TriggerType.PERIODIC_5,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
        )

        if TriggerManager.should_fire(context):
            return TriggerManager.get_prompt(context)
        return None

    def idle_check(self) -> str | None:
        """Check on returning from idle."""
        context = TriggerContext(
            trigger_type=TriggerType.IDLE_5MIN,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
        )

        if TriggerManager.should_fire(context):
            return TriggerManager.get_prompt(context)
        return None

    def heartbeat(self) -> str | None:
        """Regular health check heartbeat."""
        context = TriggerContext(
            trigger_type=TriggerType.HEARTBEAT,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
        )

        return TriggerManager.get_prompt(context)

    def emotion_decay(self) -> str | None:
        """Process emotion decay."""
        self.state_manager.decay_emotion(self.config.emotion_decay_rate)
        
        context = TriggerContext(
            trigger_type=TriggerType.EMOTION_DECAY_30MIN,
            agent_id=self.agent_id,
            timestamp=datetime.now(),
            state_snapshot=self.state_manager.current_state.get_snapshot(),
        )

        if TriggerManager.should_fire(context):
            return TriggerManager.get_prompt(context)
        return None

    def evaluate_context(self, context: dict[str, Any]) -> dict[str, EvaluationResult]:
        """Evaluate all dimensions against a context."""
        results = {}
        state = self.state_manager.current_state
        
        for dim_name in EngineRegistry.list_engines():
            engine = EngineRegistry.get(dim_name)
            if engine:
                result = engine.evaluate(state, context)
                results[dim_name] = result
                state.set_score(dim_name, result.score)
        
        return results

    def update_emotion(self, emotion: EmotionState, intensity: float = 0.5):
        """Update current emotional state."""
        self.state_manager.transition_emotion(emotion, intensity)

    def increment_interaction(self):
        """Increment interaction counter."""
        self.state_manager.increment_interaction()

    def process_reflection(self, reflection: str, trigger: TriggerType):
        """Process a self-reflection and optionally store it."""
        if trigger == TriggerType.FIRST_RESPONSE:
            self.cognition_writer.append_learned(
                "communication",
                f"Initial approach: {reflection}",
                source="first_response",
            )

    def _process_reflection(self, prompt: str, context: TriggerContext):
        """Internal method to process reflection."""
        TriggerManager.update_last_fire(context.trigger_type, context.timestamp)

    def _check_cognition_updates(self):
        """Check for hot-reload of cognition files."""
        cognition = self.cognition_reader.read_all()
        
        for file_name, cf in cognition.files.items():
            mtime = cf.path.stat().st_mtime
            if cf.path in self._last_cognition_mtime:
                if mtime > self._last_cognition_mtime[cf.path]:
                    self._on_cognition_updated(cf.path)
            self._last_cognition_mtime[cf.path] = mtime

    def _on_cognition_updated(self, path: Path):
        """Handle cognition file update."""
        print(f"Cognition updated: {path.name}")

    def get_state(self) -> SevenDimensionalState:
        """Get current state."""
        return self.state_manager.current_state

    def get_snapshot(self) -> dict[str, Any]:
        """Get state snapshot."""
        return self.state_manager.current_state.get_snapshot()

    def get_all_recommendations(self) -> list[str]:
        """Get all recommendations from evaluation."""
        results = self.evaluate_context({})
        recommendations = []
        for result in results.values():
            recommendations.extend(result.recommendations)
        return recommendations
