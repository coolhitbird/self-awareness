"""Cognition file writer module."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any

from .reader import CognitionFile, LayerType


@dataclass
class WriteOptions:
    """Options for writing cognition files."""
    create_backup: bool = True
    timestamp: bool = True
    preserve_metadata: bool = True


class CognitionWriter:
    """Writes and updates cognition files."""

    DEFAULT_TEMPLATE = """# {dimension} Cognition

# INNATE
{innate}

# ACQUIRED
{acquired}

# LEARNED
{learned}
"""

    def __init__(self, agent_id: str, base_path: Path | str | None = None):
        if base_path is None:
            base_path = Path.home() / ".agents" / "agents" / agent_id / "cognition"
        self.agent_id = agent_id
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)

    def write_dimension(
        self,
        dimension: str,
        innate: str = "",
        acquired: str = "",
        learned: str = "",
        options: WriteOptions | None = None,
    ) -> Path:
        """Write a complete dimension file with all three layers."""
        if options is None:
            options = WriteOptions()

        file_path = self.base_path / f"{dimension}.md"
        
        if options.create_backup and file_path.exists():
            self._create_backup(file_path)

        content = self.DEFAULT_TEMPLATE.format(
            dimension=dimension.capitalize(),
            innate=innate or "[Empty]",
            acquired=acquired or "[Empty]", 
            learned=learned or "[Empty]",
        )

        if options.timestamp:
            content = self._add_timestamp(content)

        file_path.write_text(content, encoding="utf-8")
        return file_path

    def update_layer(
        self,
        dimension: str,
        layer: LayerType,
        content: str,
        append: bool = False,
    ) -> Path:
        """Update a specific layer in a dimension file."""
        file_path = self.base_path / f"{dimension}.md"
        
        if file_path.exists():
            existing = file_path.read_text(encoding="utf-8")
        else:
            existing = self.DEFAULT_TEMPLATE.format(
                dimension=dimension.capitalize(),
                innate="",
                acquired="",
                learned="",
            )

        layer_key = f"# {layer.value.upper()}"
        pattern = rf"({re.escape(layer_key)}\n)(.*?)(\n(?=# [A-Z])|\Z)"
        match = re.search(pattern, existing, re.DOTALL)

        if match:
            new_content = content if not append else match.group(2).strip() + "\n\n" + content
            new_section = f"{match.group(1)}{new_content}{match.group(3)}"
            new_existing = existing[:match.start()] + new_section + existing[match.end():]
        else:
            new_existing = existing.rstrip() + f"\n\n{layer_key}\n{content}"

        file_path.write_text(new_existing, encoding="utf-8")
        return file_path

    def append_learned(
        self,
        dimension: str,
        content: str,
        source: str = "session",
    ) -> Path:
        """Append new learned content with source attribution."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        attributed = f"[{timestamp}][{source}]\n{content}"
        return self.update_layer(dimension, LayerType.LEARNED, attributed, append=True)

    def merge_cognition(
        self,
        source_path: Path,
        conflict_resolution: str = "source",
    ) -> dict[str, Path]:
        """Merge cognition from another directory."""
        results = {}
        
        for md_file in source_path.glob("*.md"):
            dest_path = self.base_path / md_file.name
            
            if dest_path.exists() and conflict_resolution == "keep_both":
                self._create_backup(dest_path)
                stem = md_file.stem
                counter = 1
                while dest_path.exists():
                    dest_path = self.base_path / f"{stem}_{counter}.md"
                    counter += 1

            dest_path.write_bytes(md_file.read_bytes())
            results[md_file.stem] = dest_path

        return results

    def create_from_template(
        self,
        dimension: str,
        template_path: Path | str,
    ) -> Path:
        """Create a dimension file from a template."""
        template = Path(template_path).read_text(encoding="utf-8")
        file_path = self.base_path / f"{dimension}.md"
        file_path.write_text(template, encoding="utf-8")
        return file_path

    def delete_dimension(self, dimension: str, create_backup: bool = True) -> bool:
        """Delete a dimension file."""
        file_path = self.base_path / f"{dimension}.md"
        if not file_path.exists():
            return False

        if create_backup:
            self._create_backup(file_path)

        file_path.unlink()
        return True

    def _create_backup(self, path: Path) -> Path:
        """Create a timestamped backup."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path.with_suffix(f".bak.{timestamp}")
        backup_path.write_bytes(path.read_bytes())
        return backup_path

    def _add_timestamp(self, content: str) -> str:
        """Add or update timestamp in content."""
        timestamp = datetime.now().isoformat()
        if "<!-- timestamp:" in content:
            return re.sub(
                r"<!-- timestamp:.*? -->",
                f"<!-- timestamp: {timestamp} -->",
                content,
            )
        return f"<!-- timestamp: {timestamp} -->\n\n{content}"

    def batch_update(
        self,
        updates: dict[str, dict[LayerType, str]],
    ) -> dict[str, Path]:
        """Batch update multiple dimensions."""
        results = {}
        for dimension, layers in updates.items():
            for layer, content in layers.items():
                results[dimension] = self.update_layer(dimension, layer, content)
        return results
