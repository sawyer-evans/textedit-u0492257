"""Main application window."""

from PyQt6.QtWidgets import QMainWindow

from editor.text_editor import TextEditor
from editor.document import Document
from actions.file_actions import FileActions
from ui.menu_bar import setup_menu_bar


class MainWindow(QMainWindow):
    """Main window with vintage terminal styling."""
    
    def __init__(self):
        super().__init__()
        self.document = Document()
        self.editor = TextEditor(self)
        self.file_actions = FileActions(self)
        
        self._setup_ui()
        self._connect_signals()
    
    def _setup_ui(self):
        """Initialize the user interface."""
        self.setCentralWidget(self.editor)
        self.resize(800, 600)
        
        self.actions = setup_menu_bar(self, self.file_actions)
        self.update_title()
    
    def _connect_signals(self):
        """Connect editor signals to update document state."""
        self.editor.textChanged.connect(self._on_text_changed)
    
    def _on_text_changed(self):
        """Mark document as modified when text changes."""
        if not self.document.is_modified:
            self.document.is_modified = True
            self.update_title()
    
    def update_title(self):
        """Update window title with filename and modified indicator."""
        title = f"PyNano - {self.document.display_name}"
        if self.document.is_modified:
            title += " *"
        self.setWindowTitle(title)
    
    def closeEvent(self, event):
        """Handle window close with unsaved changes check."""
        if self.file_actions._check_unsaved_changes():
            event.accept()
        else:
            event.ignore()
