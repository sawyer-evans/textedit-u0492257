"""Pytest fixtures for text editor tests."""

import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def document():
    """Create a fresh Document instance."""
    from editor.document import Document
    return Document()


@pytest.fixture
def editor(qtbot):
    """Create a TextEditor widget."""
    from editor.text_editor import TextEditor
    widget = TextEditor()
    qtbot.addWidget(widget)
    return widget


@pytest.fixture
def main_window(qtbot):
    """Create a MainWindow instance."""
    from ui.main_window import MainWindow
    window = MainWindow()
    qtbot.addWidget(window)
    return window
