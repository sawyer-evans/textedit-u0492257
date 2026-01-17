"""File explorer sidebar with tree view."""

from pathlib import Path

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QTreeView, QPushButton, QHBoxLayout, QLabel,
    QFileDialog, QStackedWidget
)
from PyQt6.QtGui import QFileSystemModel
from PyQt6.QtCore import Qt, pyqtSignal


BUTTON_STYLE = """
    QPushButton {
        background-color: #2d2d2d;
        color: #00aaaa;
        border: 1px solid #444;
        padding: 8px 16px;
        font-family: monospace;
        font-size: 12px;
    }
    QPushButton:hover {
        background-color: #3d3d3d;
        border-color: #00aaaa;
    }
    QPushButton:pressed {
        background-color: #1d1d1d;
    }
"""


class FileExplorer(QWidget):
    """Collapsible file explorer sidebar."""
    
    file_selected = pyqtSignal(str)
    folder_opened = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._root_path = None
        self._setup_ui()
    
    def _setup_ui(self):
        """Initialize the file explorer UI."""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Header with title and folder name
        header = QWidget()
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(8, 4, 8, 4)
        header_layout.setSpacing(2)
        
        title = QLabel("File Explorer")
        title.setStyleSheet("font-weight: bold;")
        header_layout.addWidget(title)
        
        self.folder_label = QLabel("")
        self.folder_label.setStyleSheet("color: gray; font-size: 11px;")
        self.folder_label.hide()
        header_layout.addWidget(self.folder_label)
        
        layout.addWidget(header)
        
        # Stacked widget to switch between empty state and tree view
        self.stack = QStackedWidget()
        
        # Empty state with Open buttons
        empty_widget = QWidget()
        empty_layout = QVBoxLayout(empty_widget)
        empty_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.open_file_btn = QPushButton("Open File")
        self.open_file_btn.setStyleSheet(BUTTON_STYLE)
        self.open_file_btn.clicked.connect(self._open_file_dialog)
        empty_layout.addWidget(self.open_file_btn)
        
        self.open_folder_btn = QPushButton("Open Folder")
        self.open_folder_btn.setStyleSheet(BUTTON_STYLE)
        self.open_folder_btn.clicked.connect(self._open_folder_dialog)
        empty_layout.addWidget(self.open_folder_btn)
        
        self.stack.addWidget(empty_widget)
        
        # Tree view widget
        tree_widget = QWidget()
        tree_layout = QVBoxLayout(tree_widget)
        tree_layout.setContentsMargins(0, 0, 0, 0)
        tree_layout.setSpacing(0)
        
        # File system model
        self.model = QFileSystemModel()
        
        # Tree view
        self.tree = QTreeView()
        self.tree.setModel(self.model)
        
        # Hide size, type, date columns - show only name
        self.tree.setHeaderHidden(True)
        for i in range(1, 4):
            self.tree.hideColumn(i)
        
        # Configure appearance
        self.tree.setAnimated(True)
        self.tree.setIndentation(16)
        self.tree.setSortingEnabled(True)
        self.tree.sortByColumn(0, Qt.SortOrder.AscendingOrder)
        
        # Connect double-click to open file
        self.tree.doubleClicked.connect(self._on_item_double_clicked)
        
        tree_layout.addWidget(self.tree)
        
        # Close folder button
        close_btn = QPushButton("Close Folder")
        close_btn.setStyleSheet(BUTTON_STYLE)
        close_btn.clicked.connect(self.close_folder)
        tree_layout.addWidget(close_btn)
        
        self.stack.addWidget(tree_widget)
        
        layout.addWidget(self.stack)
        
        # Start with empty state
        self.stack.setCurrentIndex(0)
    
    def _open_file_dialog(self):
        """Open a dialog to select a file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            str(Path.home()),
            "All Files (*);;Text Files (*.txt);;Python Files (*.py)"
        )
        if file_path:
            parent_folder = str(Path(file_path).parent)
            self.set_root_path(parent_folder)
            self.file_selected.emit(file_path)
    
    def _open_folder_dialog(self):
        """Open a dialog to select a folder."""
        folder = QFileDialog.getExistingDirectory(
            self,
            "Open Folder",
            str(Path.home()),
            QFileDialog.Option.ShowDirsOnly
        )
        if folder:
            self.set_root_path(folder)
    
    def _on_item_double_clicked(self, index):
        """Handle double-click on a file."""
        file_path = self.model.filePath(index)
        if Path(file_path).is_file():
            self.file_selected.emit(file_path)
    
    def set_root_path(self, path):
        """Set the root directory for the file explorer."""
        self._root_path = path
        self.model.setRootPath(path)
        self.tree.setRootIndex(self.model.index(path))
        self.stack.setCurrentIndex(1)
        
        folder_name = Path(path).name
        self.folder_label.setText(folder_name)
        self.folder_label.show()
        
        self.folder_opened.emit(path)
    
    def close_folder(self):
        """Close the current folder and return to empty state."""
        self._root_path = None
        self.stack.setCurrentIndex(0)
        self.folder_label.hide()
    
    def root_path(self):
        """Get the current root path."""
        return self._root_path
