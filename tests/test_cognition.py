"""Tests for cognition reader and writer."""

import sys
sys.path.insert(0, 'src')

import tempfile
from pathlib import Path

from cognition import CognitionReader, CognitionWriter, LayerType


def test_read_empty_directory():
    """Test reading from non-existent directory."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        reader = CognitionReader("test_agent", tmp_path)
        cognition = reader.read_all()
        
        assert cognition.agent_id == "test_agent"
        assert len(cognition.files) == 0


def test_read_single_file():
    """Test reading a single cognition file."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        test_file = tmp_path / "existential.md"
        test_file.write_text("""# Existential

# INNATE
I am a thinking entity.

# ACQUIRED
I exist in a digital space.

# LEARNED
[2024-01-01] I discovered I can reason.
""", encoding="utf-8")

        reader = CognitionReader("test_agent", tmp_path)
        cognition = reader.read_all()

        assert "existential" in cognition.files
        assert len(cognition.files["existential"].fragments) >= 2


def test_layer_detection():
    """Test layer detection from content."""
    reader = CognitionReader("test")
    
    content_innate = "# INNATE\nSomething"
    content_acquired = "# ACQUIRED\nSomething"
    content_learned = "# LEARNED\nSomething"

    assert reader._detect_layer(content_innate) == LayerType.INNATE
    assert reader._detect_layer(content_acquired) == LayerType.ACQUIRED
    assert reader._detect_layer(content_learned) == LayerType.LEARNED


def test_write_dimension():
    """Test writing a new dimension file."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        writer = CognitionWriter("test_agent", tmp_path)
        path = writer.write_dimension(
            "existential",
            innate="I am.",
            acquired="I think.",
            learned="I learn.",
        )

        assert path.exists()
        content = path.read_text(encoding="utf-8")
        assert "I am." in content
        assert "I think." in content
        assert "I learn." in content


def test_update_layer():
    """Test updating a specific layer."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        writer = CognitionWriter("test_agent", tmp_path)
        writer.write_dimension("test", innate="Original")

        writer.update_layer("test", LayerType.LEARNED, "New learned content")
        
        content = (tmp_path / "test.md").read_text(encoding="utf-8")
        assert "New learned content" in content


def test_append_learned():
    """Test appending learned content."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        writer = CognitionWriter("test_agent", tmp_path)
        writer.write_dimension("test")

        writer.append_learned("test", "First insight", source="test")
        writer.append_learned("test", "Second insight", source="test")

        content = (tmp_path / "test.md").read_text(encoding="utf-8")
        assert "First insight" in content
        assert "Second insight" in content


def test_backup_creation():
    """Test backup creation on overwrite."""
    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        writer = CognitionWriter("test_agent", tmp_path)
        path = writer.write_dimension("test", innate="Original")
        
        path.write_text("Updated", encoding="utf-8")
        writer.write_dimension("test", innate="New")

        backups = list(tmp_path.glob("*.bak*"))
        assert len(backups) == 1


if __name__ == "__main__":
    test_read_empty_directory()
    test_read_single_file()
    test_layer_detection()
    test_write_dimension()
    test_update_layer()
    test_append_learned()
    test_backup_creation()
    print("All cognition tests passed!")
