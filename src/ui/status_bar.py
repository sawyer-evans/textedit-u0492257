"""Status bar with nano-style shortcuts display."""

from PyQt6.QtWidgets import QWidget


class StatusBar(QWidget):
    """Bottom status bar showing file info and keyboard shortcuts."""
    
    def __init__(self, parent=None):
        super().__init__(parent)
