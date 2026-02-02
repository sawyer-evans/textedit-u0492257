"""Tab widget for managing multiple editor tabs."""

from PyQt6.QtWidgets import QTabWidget, QTabBar, QPushButton, QApplication
from PyQt6.QtCore import pyqtSignal, Qt, QMimeData, QPoint
from PyQt6.QtGui import QDrag

from editor.text_editor import TextEditor
from editor.document import Document
from editor.language_detector import LanguageDetector


TAB_STYLE = """
    QTabWidget::pane {
        border: none;
        background-color: #1e1e1e;
    }
    QTabWidget::tab-bar {
        alignment: left;
    }
    QTabBar::tab {
        background-color: #2d2d2d;
        color: #888;
        border: 1px solid #444;
        border-bottom: none;
        padding: 6px 24px;
        min-width: 120px;
        font-family: monospace;
        font-size: 11px;
        margin-right: 2px;
    }
    QTabBar::tab:selected {
        background-color: #1e1e1e;
        color: #00aaaa;
        border-bottom: 1px solid #1e1e1e;
    }
    QTabBar::tab:hover:!selected {
        background-color: #3d3d3d;
        color: #aaa;
    }
    QTabBar::close-button {
        subcontrol-position: right;
        border: none;
        background: transparent;
        padding: 2px;
        margin-left: 4px;
        width: 12px;
        height: 12px;
    }
    QTabBar::close-button:hover {
        background-color: #555;
        border-radius: 2px;
    }
"""


class EditorTab:
    """Container for an editor and its associated document."""
    
    def __init__(self):
        self.editor = TextEditor()
        self.document = Document()


CLOSE_BTN_STYLE = """
    QPushButton {
        background: transparent;
        color: #888;
        border: none;
        font-family: monospace;
        font-size: 14px;
        font-weight: bold;
        padding: 0px 4px;
        margin: 0px;
    }
    QPushButton:hover {
        color: #fff;
        background-color: #555;
        border-radius: 2px;
    }
"""


class DraggableTabBar(QTabBar):
    """Tab bar that supports dragging tabs out to create splits."""
    
    tab_drag_started = pyqtSignal(int, QPoint)  # tab index, global position
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start_pos = None
        self._dragging = False
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        if self._drag_start_pos is None:
            super().mouseMoveEvent(event)
            return
        
        if self._dragging:
            return
        
        distance = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
        if distance < QApplication.startDragDistance():
            super().mouseMoveEvent(event)
            return
        
        tab_index = self.tabAt(self._drag_start_pos)
        if tab_index < 0:
            super().mouseMoveEvent(event)
            return
        
        self._dragging = True
        
        drag = QDrag(self)
        mime_data = QMimeData()
        mime_data.setData("application/x-tab-index", str(tab_index).encode())
        drag.setMimeData(mime_data)
        
        drag.exec(Qt.DropAction.MoveAction)
        
        self._dragging = False
        self._drag_start_pos = None
    
    def mouseReleaseEvent(self, event):
        self._drag_start_pos = None
        self._dragging = False
        super().mouseReleaseEvent(event)


class TabWidget(QTabWidget):
    """Tab widget managing multiple editor tabs."""
    
    current_document_changed = pyqtSignal()
    tab_dragged_out = pyqtSignal(int)  # tab index being dragged
    last_tab_closed = pyqtSignal()  # emitted when trying to close the last tab
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Use custom draggable tab bar
        self._tab_bar = DraggableTabBar(self)
        self.setTabBar(self._tab_bar)
        
        self.setStyleSheet(TAB_STYLE)
        self.setTabsClosable(False)
        self.setMovable(True)
        
        self._tabs = []
        
        self.currentChanged.connect(self._on_current_changed)
        
        # Create initial tab
        self.new_tab()
    
    def new_tab(self, file_path=None):
        """Create a new editor tab."""
        tab = EditorTab()
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                tab.editor.setPlainText(content)
                tab.document.file_path = file_path
                tab.document.is_modified = False
                language = LanguageDetector.detect_language(file_path)
                tab.editor.set_syntax_language(language)
            except Exception:
                pass
        
        self._tabs.append(tab)
        index = self.addTab(tab.editor, tab.document.display_name)
        self.setCurrentIndex(index)
        
        # Add custom close button
        close_btn = QPushButton("×")
        close_btn.setStyleSheet(CLOSE_BTN_STYLE)
        close_btn.setFixedSize(18, 18)
        close_btn.clicked.connect(lambda _, t=tab: self._close_tab(t))
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, close_btn)
        
        # Connect text changed to update tab title
        tab.editor.textChanged.connect(lambda: self._on_text_changed(tab))
        
        return tab
    
    def _on_text_changed(self, tab):
        """Update tab title when content changes."""
        if tab not in self._tabs:
            return
        if not tab.document.is_modified:
            tab.document.is_modified = True
            self._update_tab_title(tab)
            self.current_document_changed.emit()
    
    def _update_tab_title(self, tab):
        """Update the tab title to reflect document state."""
        if tab not in self._tabs:
            return
        index = self._tabs.index(tab)
        title = tab.document.display_name
        if tab.document.is_modified:
            title += " *"
        self.setTabText(index, title)
    
    def _close_tab(self, tab):
        """Close a specific tab safely."""
        if tab not in self._tabs:
            return
        
        if self.count() <= 1:
            # Signal that the last tab is being closed (for split view handling)
            self.last_tab_closed.emit()
            return
        
        index = self._tabs.index(tab)
        self._tabs.pop(index)
        self.removeTab(index)
    
    def _on_current_changed(self, index):
        """Handle tab change."""
        self.current_document_changed.emit()
    
    def current_tab(self):
        """Get the current tab."""
        index = self.currentIndex()
        if 0 <= index < len(self._tabs):
            return self._tabs[index]
        return None
    
    @property
    def current_editor(self):
        """Get the current editor."""
        tab = self.current_tab()
        return tab.editor if tab else None
    
    @property
    def current_document(self):
        """Get the current document."""
        tab = self.current_tab()
        return tab.document if tab else None
    
    def open_file(self, file_path):
        """Open a file in a new tab (or current if empty and unmodified)."""
        current = self.current_tab()
        
        # If current tab is empty and unmodified, reuse it
        if (current and 
            not current.document.is_modified and 
            current.document.file_path is None and
            not current.editor.toPlainText()):
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                current.editor.setPlainText(content)
                current.document.file_path = file_path
                current.document.is_modified = False
                language = LanguageDetector.detect_language(file_path)
                current.editor.set_syntax_language(language)
                self._update_tab_title(current)
                self.current_document_changed.emit()
                return True
            except Exception:
                return False
        
        # Otherwise create new tab
        tab = self.new_tab(file_path)
        return tab is not None
    
    def save_current(self):
        """Save the current tab's file."""
        tab = self.current_tab()
        if not tab:
            return False
        
        if tab.document.file_path is None:
            return False
        
        try:
            with open(tab.document.file_path, "w", encoding="utf-8") as f:
                f.write(tab.editor.toPlainText())
            tab.document.is_modified = False
            self._update_tab_title(tab)
            self.current_document_changed.emit()
            return True
        except Exception:
            return False
    
    def mark_current_saved(self, file_path):
        """Mark current tab as saved with given path."""
        tab = self.current_tab()
        if tab:
            tab.document.file_path = file_path
            tab.document.is_modified = False
            language = LanguageDetector.detect_language(file_path)
            tab.editor.set_syntax_language(language)
            self._update_tab_title(tab)
            self.current_document_changed.emit()
