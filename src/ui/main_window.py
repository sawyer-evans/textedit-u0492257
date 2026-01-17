"""Main application window."""

from PyQt6.QtWidgets import QMainWindow, QSplitter
from PyQt6.QtCore import Qt

from actions.file_actions import FileActions
from ui.menu_bar import setup_menu_bar
from ui.file_explorer import FileExplorer
from ui.split_view import SplitContainer


class MainWindow(QMainWindow):
    """Main window with vintage terminal styling."""
    
    def __init__(self):
        super().__init__()
        
        # Create split container with tab widget factory
        self.split_container = SplitContainer(self._create_tab_widget, self)
        self.file_explorer = FileExplorer(self)
        self.file_actions = FileActions(self)
        
        self._setup_ui()
        self._connect_signals()
    
    def _create_tab_widget(self):
        """Factory function to create new tab widgets."""
        from ui.tab_widget import TabWidget
        tw = TabWidget(create_initial_tab=True)
        tw.current_document_changed.connect(self.update_title)
        return tw
    
    def _setup_ui(self):
        """Initialize the user interface."""
        # Create splitter for file explorer and split container
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.addWidget(self.file_explorer)
        self.splitter.addWidget(self.split_container)
        
        # Set initial sizes (200px for explorer, rest for editor)
        self.splitter.setSizes([200, 600])
        self.splitter.setCollapsible(0, True)
        self.splitter.setCollapsible(1, False)
        
        self.setCentralWidget(self.splitter)
        self.resize(1000, 600)
        
        self.actions = setup_menu_bar(self, self.file_actions)
        self.update_title()
    
    def _connect_signals(self):
        """Connect signals to update window state."""
        self.file_explorer.file_selected.connect(self._on_file_selected)
    
    @property
    def tab_widget(self):
        """Get the current/main tab widget."""
        return self.split_container.get_tab_widget()
    
    def _on_file_selected(self, file_path):
        """Open file selected from file explorer in a new tab."""
        tw = self.tab_widget
        if tw:
            tw.new_tab(file_path)
    
    @property
    def editor(self):
        """Get the current editor (for compatibility)."""
        tw = self.tab_widget
        return tw.current_editor if tw else None
    
    @property
    def document(self):
        """Get the current document (for compatibility)."""
        tw = self.tab_widget
        return tw.current_document if tw else None
    
    def toggle_file_explorer(self):
        """Toggle visibility of the file explorer."""
        if self.file_explorer.isVisible():
            self._explorer_width = self.splitter.sizes()[0]
            self.file_explorer.hide()
        else:
            self.file_explorer.show()
            width = getattr(self, '_explorer_width', 200)
            self.splitter.setSizes([width, self.splitter.sizes()[1]])
    
    def update_title(self):
        """Update window title with filename and modified indicator."""
        doc = self.document
        if doc:
            title = f"PyNano - {doc.display_name}"
            if doc.is_modified:
                title += " *"
        else:
            title = "PyNano"
        self.setWindowTitle(title)
    
    def closeEvent(self, event):
        """Handle window close with unsaved changes check."""
        if self.file_actions._check_unsaved_changes():
            event.accept()
        else:
            event.ignore()
