"""Dashboard module for self-awareness state visualization."""

from .renderer import (
    DashboardConfig,
    DashboardRenderer,
    TerminalColors,
    render_dashboard,
)

__all__ = [
    "DashboardConfig",
    "DashboardRenderer",
    "TerminalColors",
    "render_dashboard",
]
