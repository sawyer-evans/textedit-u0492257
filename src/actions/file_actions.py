"""File operations: New, Open, Save, Save As."""

import os
from pathlib import Path

from PyQt6.QtWidgets import QFileDialog, QMessageBox


def get_default_directory():
    """Get a sensible default directory for file dialogs."""
    documents = Path.home() / "Documents"
    if documents.exists():
        return str(documents)
    return str(Path.home())


class FileActions:
    """Handles file operations for the editor."""
    
    def __init__(self, main_window):
        self.main_window = main_window
    
    @property
    def editor(self):
        return self.main_window.editor
    
    @property
    def document(self):
        return self.main_window.document
    
    def _check_unsaved_changes(self):
        """Prompt user if there are unsaved changes. Returns True if safe to proceed."""
        if not self.document.is_modified:
            return True
        
        reply = QMessageBox.question(
            self.main_window,
            "Unsaved Changes",
            f"Save changes to {self.document.display_name}?",
            QMessageBox.StandardButton.Save |
            QMessageBox.StandardButton.Discard |
            QMessageBox.StandardButton.Cancel
        )
        
        if reply == QMessageBox.StandardButton.Save:
            return self.save_file()
        elif reply == QMessageBox.StandardButton.Discard:
            return True
        else:
            return False
    
    def new_file(self):
        """Create a new empty file."""
        if not self._check_unsaved_changes():
            return False
        
        self.editor.clear()
        self.document.reset()
        self.main_window.update_title()
        return True
    
    def open_file(self, file_path=None):
        """Open a file dialog and load selected file."""
        if not self._check_unsaved_changes():
            return False
        
        if file_path is None:
            start_dir = get_default_directory()
            if self.document.file_path:
                start_dir = os.path.dirname(self.document.file_path)
            
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Open File",
                start_dir,
                "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
            )
        
        if not file_path:
            return False
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
            
            self.editor.setPlainText(content)
            self.document.file_path = file_path
            self.document.is_modified = False
            self.main_window.update_title()
            return True
        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Could not open file:\n{e}"
            )
            return False
    
    def save_file(self):
        """Save current file, or Save As if untitled."""
        if self.document.file_path is None:
            return self.save_file_as()
        
        return self._write_file(self.document.file_path)
    
    def save_file_as(self):
        """Save file with a new name."""
        if self.document.file_path:
            default_path = self.document.file_path
        else:
            default_path = os.path.join(get_default_directory(), self.document.display_name)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Save File As",
            default_path,
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        
        if not file_path:
            return False
        
        return self._write_file(file_path)
    
    def _write_file(self, file_path):
        """Write editor content to file."""
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
            
            self.document.file_path = file_path
            self.document.is_modified = False
            self.main_window.update_title()
            return True
        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Could not save file:\n{e}"
            )
            return False
