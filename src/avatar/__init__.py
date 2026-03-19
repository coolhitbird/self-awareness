"""Avatar system for self-awareness."""

from .generator import (
    AvatarConfig,
    AvatarStyle,
    AvatarGenerator,
    KAOMOJI_MAP,
    get_kaomoji,
    get_random_kaomoji,
    format_avatar,
    create_agent_avatar,
)

__all__ = [
    "AvatarConfig",
    "AvatarStyle",
    "AvatarGenerator",
    "KAOMOJI_MAP",
    "get_kaomoji",
    "get_random_kaomoji",
    "format_avatar",
    "create_agent_avatar",
]
