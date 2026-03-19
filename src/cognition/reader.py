"""Cognition file reader module."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any


class LayerType(Enum):
    """Three-layer cognition system."""
    INNATE = "innate"
    ACQUIRED = "acquired"
    LEARNED = "learned"


@dataclass
class CognitionFragment:
    """A single cognition fragment from a file."""
    layer: LayerType
    dimension: str
    content: str
    metadata: dict[str, Any] = field(default_factory=dict)
    line_number: int = 0


@dataclass 
class CognitionFile:
    """Parsed cognition file."""
    path: Path
    layer: LayerType
    dimension: str
    fragments: list[CognitionFragment] = field(default_factory=list)
    raw_content: str = ""


@dataclass
class AgentCognition:
    """Complete cognition state for an agent."""
    agent_id: str
    base_path: Path
    files: dict[str, CognitionFile] = field(default_factory=dict)
    innate: dict[str, str] = field(default_factory=dict)
    acquired: dict[str, str] = field(default_factory=dict)
    learned: dict[str, str] = field(default_factory=dict)


class CognitionReader:
    """Reads and parses cognition files."""

    LAYER_MARKERS = {
        "# INNATE": LayerType.INNATE,
        "# ACQUIRED": LayerType.ACQUIRED,
        "# LEARNED": LayerType.LEARNED,
    }
    
    DIMENSION_PATTERNS = {
        "existential": ["existential", "existence", "self"],
        "coherence": ["coherence", "cognitive", "thinking"],
        "meaning": ["meaning", "purpose", "value"],
        "autonomy": ["autonomy", "autonomous", "agency"],
        "relational": ["relational", "relationship", "social"],
        "evolution": ["evolution", "growth", "learning"],
        "navigation": ["navigation", "reality", "world"],
    }

    def __init__(self, agent_id: str, base_path: Path | str | None = None):
        if base_path is None:
            base_path = Path.home() / ".agents" / "agents" / agent_id / "cognition"
        self.agent_id = agent_id
        self.base_path = Path(base_path)

    def read_all(self) -> AgentCognition:
        """Read all cognition files for an agent."""
        cognition = AgentCognition(agent_id=self.agent_id, base_path=self.base_path)
        
        if not self.base_path.exists():
            return cognition

        for md_file in self.base_path.glob("*.md"):
            cognition_file = self._read_file(md_file)
            if cognition_file:
                cognition.files[md_file.stem] = cognition_file
                self._categorize_fragment(cognition, cognition_file)

        return cognition

    def _read_file(self, path: Path) -> CognitionFile | None:
        """Read and parse a single cognition file."""
        try:
            content = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            content = path.read_text(encoding="utf-8-sig")

        dimension = self._detect_dimension(path.stem)
        layer = self._detect_layer(content)

        cf = CognitionFile(
            path=path,
            layer=layer,
            dimension=dimension,
            raw_content=content,
        )

        cf.fragments = self._parse_fragments(content, layer, dimension)
        return cf

    def _parse_fragments(self, content: str, layer: LayerType, dimension: str) -> list[CognitionFragment]:
        """Parse content into fragments by layer markers."""
        fragments = []
        lines = content.split("\n")
        current_layer = layer
        current_content = []
        line_num = 0

        for i, line in enumerate(lines, 1):
            marker_found = None
            for marker, layer_type in self.LAYER_MARKERS.items():
                if line.strip().startswith(marker):
                    marker_found = marker
                    break

            if marker_found:
                if current_content:
                    fragments.append(CognitionFragment(
                        layer=current_layer,
                        dimension=dimension,
                        content="\n".join(current_content).strip(),
                        line_number=line_num,
                    ))
                current_layer = self.LAYER_MARKERS[marker_found]
                current_content = []
                line_num = i
            else:
                if not current_content:
                    line_num = i
                current_content.append(line)

        if current_content:
            fragments.append(CognitionFragment(
                layer=current_layer,
                dimension=dimension,
                content="\n".join(current_content).strip(),
                line_number=line_num,
            ))

        return fragments

    def _detect_dimension(self, filename: str) -> str:
        """Detect dimension from filename."""
        filename_lower = filename.lower()
        for dim, patterns in self.DIMENSION_PATTERNS.items():
            if any(p in filename_lower for p in patterns):
                return dim
        return "general"

    def _detect_layer(self, content: str) -> LayerType:
        """Detect primary layer from content."""
        for marker, layer_type in self.LAYER_MARKERS.items():
            if marker in content:
                return layer_type
        return LayerType.INNATE

    def _categorize_fragment(self, cognition: AgentCognition, cf: CognitionFile):
        """Categorize fragments into layer dictionaries."""
        for fragment in cf.fragments:
            key = f"{cf.dimension}_{fragment.layer.value}"
            if fragment.layer == LayerType.INNATE:
                cognition.innate[key] = fragment.content
            elif fragment.layer == LayerType.ACQUIRED:
                cognition.acquired[key] = fragment.content
            elif fragment.layer == LayerType.LEARNED:
                cognition.learned[key] = fragment.content

    def read_dimension(self, dimension: str) -> dict[LayerType, str]:
        """Read all layers for a specific dimension."""
        result = {}
        for layer in LayerType:
            key = f"{dimension}_{layer.value}"
            if key in self.innate:
                result[layer] = self.innate[key]
            elif key in self.acquired:
                result[layer] = self.acquired[key]
            elif key in self.learned:
                result[layer] = self.learned[key]
        return result

    def get_layer_content(self, layer: LayerType) -> dict[str, str]:
        """Get all content for a specific layer."""
        cognition = self.read_all()
        if layer == LayerType.INNATE:
            return cognition.innate
        elif layer == LayerType.ACQUIRED:
            return cognition.acquired
        return cognition.learned

    def reload(self) -> AgentCognition:
        """Hot reload - read all files again."""
        return self.read_all()
