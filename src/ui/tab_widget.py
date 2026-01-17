"""Tab widget for managing multiple editor tabs."""

from PyQt6.QtWidgets import QTabWidget, QTabBar, QPushButton, QApplication
from PyQt6.QtCore import pyqtSignal, Qt, QPoint, QMimeData
from PyQt6.QtGui import QDrag, QPixmap, QPainter, QColor

from editor.text_editor import TextEditor
from editor.document import Document


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
    """Tab bar that supports dragging tabs out for split view."""
    
    drag_started = pyqtSignal(object)  # Emits the tab being dragged
    drag_ended = pyqtSignal()
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self._drag_start_pos = None
        self._dragging = False
        self._drag_tab_index = -1
    
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.position().toPoint()
            self._drag_start_pos = pos
            self._drag_tab_index = self.tabAt(pos)
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        try:
            if self._dragging:
                return
            
            if not self._drag_start_pos or self._drag_tab_index < 0:
                super().mouseMoveEvent(event)
                return
            
            # Check if we've moved far enough to start a drag
            distance = (event.position().toPoint() - self._drag_start_pos).manhattanLength()
            if distance < QApplication.startDragDistance() * 3:
                super().mouseMoveEvent(event)
                return
            
            # Verify tab still exists
            tab_widget = self.parent()
            if not tab_widget or not hasattr(tab_widget, '_tabs'):
                self._reset_drag_state()
                return
            
            if self._drag_tab_index >= len(tab_widget._tabs):
                self._reset_drag_state()
                return
            
            # Only allow drag if there's more than one tab
            if len(tab_widget._tabs) <= 1:
                self._reset_drag_state()
                super().mouseMoveEvent(event)
                return
            
            # Start drag
            self._dragging = True
            tab = tab_widget._tabs[self._drag_tab_index]
            
            try:
                self.drag_started.emit(tab)
                
                # Create drag object
                drag = QDrag(self)
                mime_data = QMimeData()
                mime_data.setData("application/x-tab-drag", b"tab")
                drag.setMimeData(mime_data)
                
                # Create drag pixmap
                pixmap = QPixmap(150, 30)
                pixmap.fill(QColor(45, 45, 45))
                painter = QPainter(pixmap)
                painter.setPen(QColor(0, 170, 170))
                painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, 
                               tab.document.display_name)
                painter.end()
                drag.setPixmap(pixmap)
                
                drag.exec(Qt.DropAction.MoveAction)
            finally:
                try:
                    self.drag_ended.emit()
                except RuntimeError:
                    pass
                self._reset_drag_state()
        except RuntimeError:
            self._reset_drag_state()
    
    def _reset_drag_state(self):
        """Reset all drag-related state."""
        self._drag_start_pos = None
        self._dragging = False
        self._drag_tab_index = -1
    
    def mouseReleaseEvent(self, event):
        self._reset_drag_state()
        super().mouseReleaseEvent(event)


class TabWidget(QTabWidget):
    """Tab widget managing multiple editor tabs."""
    
    current_document_changed = pyqtSignal()
    tab_drag_started = pyqtSignal(object)  # Emits the tab being dragged
    tab_drag_ended = pyqtSignal()
    all_tabs_closed = pyqtSignal()  # Emitted when last tab is closed in split mode
    
    def __init__(self, parent=None, create_initial_tab=True):
        super().__init__(parent)
        
        # Use custom draggable tab bar
        self._tab_bar = DraggableTabBar(self)
        self.setTabBar(self._tab_bar)
        self._tab_bar.drag_started.connect(self._on_drag_started)
        self._tab_bar.drag_ended.connect(self._on_drag_ended)
        
        self.setStyleSheet(TAB_STYLE)
        self.setTabsClosable(False)
        self.setMovable(True)
        
        self._tabs = []
        self._is_in_split = False  # Track if this widget is part of a split view
        
        self.currentChanged.connect(self._on_current_changed)
        
        # Create initial tab
        if create_initial_tab:
            self.new_tab()
    
    def _on_drag_started(self, tab):
        """Forward drag started signal."""
        self.tab_drag_started.emit(tab)
    
    def _on_drag_ended(self):
        """Forward drag ended signal."""
        self.tab_drag_ended.emit()
    
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
            if self._is_in_split:
                # In split mode, close the last tab and signal for collapse
                index = self._tabs.index(tab)
                self._tabs.pop(index)
                self.removeTab(index)
                self.all_tabs_closed.emit()
            else:
                # Don't close the last tab, just clear it
                tab.editor.clear()
                tab.document.reset()
                self._update_tab_title(tab)
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
            self._update_tab_title(tab)
            self.current_document_changed.emit()
    
    def add_tab_from_drag(self, tab):
        """Add an existing tab from a drag operation."""
        self._tabs.append(tab)
        tab.editor.setParent(None)  # Detach from old parent
        index = self.addTab(tab.editor, tab.document.display_name)
        self.setCurrentIndex(index)
        
        # Add close button
        close_btn = QPushButton("×")
        close_btn.setStyleSheet(CLOSE_BTN_STYLE)
        close_btn.setFixedSize(18, 18)
        close_btn.clicked.connect(lambda _, t=tab: self._close_tab(t))
        self.tabBar().setTabButton(index, QTabBar.ButtonPosition.RightSide, close_btn)
        
        # Reconnect text changed
        tab.editor.textChanged.connect(lambda: self._on_text_changed(tab))
        
        self._update_tab_title(tab)
        self.current_document_changed.emit()
    
    def remove_tab_for_drag(self, tab):
        """Remove a tab for dragging to another widget."""
        if tab not in self._tabs:
            return
        
        index = self._tabs.index(tab)
        self._tabs.pop(index)
        self.removeTab(index)
        
        # If this was the last tab, create a new empty one
        if len(self._tabs) == 0:
            self.new_tab()
