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
    def tab_widget(self):
        return self.main_window.tab_widget
    
    @property
    def editor(self):
        return self.main_window.editor
    
    @property
    def document(self):
        return self.main_window.document
    
    def _check_unsaved_changes(self):
        """Prompt user if there are unsaved changes. Returns True if safe to proceed."""
        doc = self.document
        if not doc or not doc.is_modified:
            return True
        
        reply = QMessageBox.question(
            self.main_window,
            "Unsaved Changes",
            f"Save changes to {doc.display_name}?",
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
        """Create a new tab."""
        self.tab_widget.new_tab()
        self.main_window.update_title()
        return True
    
    def open_file(self, file_path=None):
        """Open a file in a new tab."""
        if file_path is None:
            start_dir = get_default_directory()
            doc = self.document
            if doc and doc.file_path:
                start_dir = os.path.dirname(doc.file_path)
            
            file_path, _ = QFileDialog.getOpenFileName(
                self.main_window,
                "Open File",
                start_dir,
                "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
            )
        
        if not file_path:
            return False
        
        result = self.tab_widget.open_file(file_path)
        self.main_window.update_title()
        return result
    
    def save_file(self):
        """Save current file, or Save As if untitled."""
        doc = self.document
        if not doc:
            return False
        
        if doc.file_path is None:
            return self.save_file_as()
        
        result = self.tab_widget.save_current()
        self.main_window.update_title()
        return result
    
    def save_file_as(self):
        """Save file with a new name."""
        doc = self.document
        editor = self.editor
        if not doc or not editor:
            return False
        
        if doc.file_path:
            default_path = doc.file_path
        else:
            default_path = os.path.join(get_default_directory(), doc.display_name)
        
        file_path, _ = QFileDialog.getSaveFileName(
            self.main_window,
            "Save File As",
            default_path,
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        
        if not file_path:
            return False
        
        try:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(editor.toPlainText())
            
            self.tab_widget.mark_current_saved(file_path)
            self.main_window.update_title()
            return True
        except Exception as e:
            QMessageBox.critical(
                self.main_window,
                "Error",
                f"Could not save file:\n{e}"
            )
            return False
