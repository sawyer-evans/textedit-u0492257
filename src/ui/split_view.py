"""Split view container for drag-and-drop tab splitting."""

from enum import Enum, auto

from PyQt6.QtWidgets import QWidget, QSplitter, QVBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal, QRect
from PyQt6.QtGui import QPainter, QColor


class DropZone(Enum):
    """Drop zones for split view."""
    LEFT = auto()
    RIGHT = auto()
    TOP = auto()
    BOTTOM = auto()


# Global reference to track the current drag operation
_current_drag_tab = None
_current_drag_source = None


class DropOverlay(QWidget):
    """Overlay that shows drop zone highlights during drag."""
    
    dropped = pyqtSignal(object)  # Emits the drop zone
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, False)
        self.setAcceptDrops(True)
        self._active_zone = None
        self._zones = {}
        self.hide()
    
    def showOverlay(self):
        """Show the overlay and calculate zones."""
        self.setGeometry(self.parent().rect())
        self._calculate_zones()
        self.show()
        self.raise_()
    
    def hideOverlay(self):
        """Hide the overlay."""
        self._active_zone = None
        self.hide()
    
    def _calculate_zones(self):
        """Calculate the drop zone rectangles - simple halves."""
        w, h = self.width(), self.height()
        half_w = w // 2
        half_h = h // 2
        
        self._zones = {
            DropZone.LEFT: QRect(0, 0, half_w, h),
            DropZone.RIGHT: QRect(half_w, 0, w - half_w, h),
            DropZone.TOP: QRect(0, 0, w, half_h),
            DropZone.BOTTOM: QRect(0, half_h, w, h - half_h),
        }
    
    def zoneAt(self, pos):
        """Get the drop zone at the given position based on which half the cursor is in."""
        w, h = self.width(), self.height()
        x, y = pos.x(), pos.y()
        
        # Determine if horizontal or vertical split based on position
        # Use distance from center to determine primary axis
        dx = abs(x - w / 2) / (w / 2)  # 0 at center, 1 at edge
        dy = abs(y - h / 2) / (h / 2)  # 0 at center, 1 at edge
        
        if dx > dy:
            # Closer to left/right edge - horizontal split
            return DropZone.LEFT if x < w / 2 else DropZone.RIGHT
        else:
            # Closer to top/bottom edge - vertical split
            return DropZone.TOP if y < h / 2 else DropZone.BOTTOM
    
    def setActiveZone(self, zone):
        """Set the active (highlighted) zone."""
        if self._active_zone != zone:
            self._active_zone = zone
            self.update()
    
    def paintEvent(self, event):
        """Paint the drop zone highlights."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        w, h = self.width(), self.height()
        half_w, half_h = w // 2, h // 2
        
        # Calculate the highlight rect based on active zone
        if self._active_zone == DropZone.LEFT:
            highlight_rect = QRect(0, 0, half_w, h)
        elif self._active_zone == DropZone.RIGHT:
            highlight_rect = QRect(half_w, 0, w - half_w, h)
        elif self._active_zone == DropZone.TOP:
            highlight_rect = QRect(0, 0, w, half_h)
        elif self._active_zone == DropZone.BOTTOM:
            highlight_rect = QRect(0, half_h, w, h - half_h)
        else:
            highlight_rect = None
        
        # Draw dim overlay on the non-highlighted half
        dim_color = QColor(0, 0, 0, 100)
        if highlight_rect:
            painter.fillRect(self.rect(), dim_color)
            
            # Highlight the active zone
            highlight_color = QColor(0, 170, 170, 80)
            painter.fillRect(highlight_rect, highlight_color)
            
            # Draw border
            border_color = QColor(0, 200, 200)
            painter.setPen(border_color)
            painter.drawRect(highlight_rect.adjusted(2, 2, -2, -2))
        else:
            painter.fillRect(self.rect(), dim_color)
    
    def dragEnterEvent(self, event):
        if event.mimeData().hasFormat("application/x-tab-drag"):
            event.acceptProposedAction()
    
    def dragMoveEvent(self, event):
        zone = self.zoneAt(event.position().toPoint())
        self.setActiveZone(zone)
        event.acceptProposedAction()
    
    def dragLeaveEvent(self, event):
        self.setActiveZone(None)
    
    def dropEvent(self, event):
        zone = self.zoneAt(event.position().toPoint())
        if zone:
            self.dropped.emit(zone)
            event.acceptProposedAction()
        self.hideOverlay()


class SplitContainer(QWidget):
    """Container that can hold a TabWidget or be split into multiple containers."""
    
    def __init__(self, tab_widget_factory, parent=None, create_initial=True):
        super().__init__(parent)
        self._tab_widget_factory = tab_widget_factory
        self._layout = QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(0)
        
        self._splitter = None
        self._tab_widget = None
        self._children = []
        
        # Create initial tab widget only if requested
        if create_initial:
            self._create_tab_widget()
        
        # Drop overlay
        self._overlay = DropOverlay(self)
        self._overlay.dropped.connect(self._on_drop)
        self._overlay.hide()
    
    def _create_tab_widget(self):
        """Create a new tab widget for this container."""
        self._tab_widget = self._tab_widget_factory()
        self._tab_widget.tab_drag_started.connect(self._on_tab_drag_started)
        self._tab_widget.tab_drag_ended.connect(self._on_tab_drag_ended)
        self._layout.addWidget(self._tab_widget)
    
    def _on_tab_drag_started(self, tab):
        """Show overlay when tab drag starts."""
        global _current_drag_tab, _current_drag_source
        try:
            _current_drag_tab = tab
            _current_drag_source = self._tab_widget
            self._show_all_overlays()
        except RuntimeError:
            pass
    
    def _on_tab_drag_ended(self):
        """Hide overlay when tab drag ends."""
        global _current_drag_tab, _current_drag_source
        try:
            _current_drag_tab = None
            _current_drag_source = None
            self._hide_all_overlays()
        except RuntimeError:
            pass
    
    def _show_all_overlays(self):
        """Show overlays on this and all child containers."""
        try:
            if self._tab_widget:
                self._overlay.showOverlay()
            for child in self._children:
                child._show_all_overlays()
            # Also notify parent to show sibling overlays
            parent = self.parent()
            if isinstance(parent, QSplitter):
                grandparent = parent.parent()
                if isinstance(grandparent, SplitContainer):
                    grandparent._show_sibling_overlays(self)
        except RuntimeError:
            pass
    
    def _show_sibling_overlays(self, exclude):
        """Show overlays on children except the excluded one."""
        try:
            for child in self._children:
                if child != exclude:
                    child._show_all_overlays()
        except RuntimeError:
            pass
    
    def _hide_all_overlays(self):
        """Hide overlays on this and all child containers."""
        try:
            self._overlay.hideOverlay()
            for child in self._children:
                child._hide_all_overlays()
        except RuntimeError:
            pass
    
    def get_tab_widget(self):
        """Get the tab widget (for the main/first container)."""
        if self._tab_widget:
            return self._tab_widget
        if self._children:
            return self._children[0].get_tab_widget()
        return None
    
    def _on_drop(self, zone):
        """Handle a drop on this container."""
        global _current_drag_tab, _current_drag_source
        
        if not _current_drag_tab:
            return
        
        tab = _current_drag_tab
        source = _current_drag_source
        
        # Create split
        source.remove_tab_for_drag(tab)
        self._split_with_tab(zone, tab)
    
    def _split_with_tab(self, zone, tab):
        """Split this container and add tab to new section."""
        if not self._tab_widget:
            return
        
        # Determine orientation
        if zone in (DropZone.LEFT, DropZone.RIGHT):
            orientation = Qt.Orientation.Horizontal
        else:
            orientation = Qt.Orientation.Vertical
        
        # Remove current tab widget from layout
        self._layout.removeWidget(self._tab_widget)
        self._overlay.hide()
        
        # Create splitter
        self._splitter = QSplitter(orientation)
        self._splitter.setHandleWidth(4)
        self._splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #333;
            }
            QSplitter::handle:hover {
                background-color: #00aaaa;
            }
        """)
        
        # Create two child containers without initial tab widgets (they'll be replaced)
        child1 = SplitContainer(self._tab_widget_factory, self, create_initial=False)
        child2 = SplitContainer(self._tab_widget_factory, self, create_initial=False)
        
        # Create new tab widget WITHOUT initial tab, then add the dragged tab
        from ui.tab_widget import TabWidget
        new_tw = TabWidget(create_initial_tab=False)
        new_tw.add_tab_from_drag(tab)
        
        # Disconnect signals from the old tab widget before transferring
        old_tw = self._tab_widget
        self._disconnect_tab_widget(old_tw)
        self._tab_widget = None
        
        # Transfer widgets to appropriate children
        if zone in (DropZone.RIGHT, DropZone.BOTTOM):
            child1._replace_tab_widget(old_tw)
            child2._replace_tab_widget(new_tw)
        else:
            child1._replace_tab_widget(new_tw)
            child2._replace_tab_widget(old_tw)
        self._children = [child1, child2]
        
        self._splitter.addWidget(child1)
        self._splitter.addWidget(child2)
        self._splitter.setSizes([1, 1])  # Equal sizes
        
        self._layout.addWidget(self._splitter)
    
    def _disconnect_tab_widget(self, tab_widget):
        """Safely disconnect all signals from a tab widget."""
        if not tab_widget:
            return
        try:
            tab_widget.tab_drag_started.disconnect(self._on_tab_drag_started)
        except (TypeError, RuntimeError):
            pass
        try:
            tab_widget.tab_drag_ended.disconnect(self._on_tab_drag_ended)
        except (TypeError, RuntimeError):
            pass
        try:
            tab_widget.all_tabs_closed.disconnect(self._on_all_tabs_closed)
        except (TypeError, RuntimeError):
            pass
        tab_widget._is_in_split = False
    
    def _replace_tab_widget(self, tab_widget):
        """Replace the tab widget with an existing one."""
        if self._tab_widget:
            self._layout.removeWidget(self._tab_widget)
            self._disconnect_tab_widget(self._tab_widget)
        
        self._tab_widget = tab_widget
        self._tab_widget.setParent(self)
        self._tab_widget._is_in_split = True
        self._tab_widget.tab_drag_started.connect(self._on_tab_drag_started)
        self._tab_widget.tab_drag_ended.connect(self._on_tab_drag_ended)
        self._tab_widget.all_tabs_closed.connect(self._on_all_tabs_closed)
        self._layout.addWidget(self._tab_widget)
    
    def _on_all_tabs_closed(self):
        """Handle when all tabs in this container are closed - collapse the split."""
        parent = self.parent()
        if isinstance(parent, QSplitter):
            grandparent = parent.parent()
            if isinstance(grandparent, SplitContainer):
                grandparent._collapse_split(self)
    
    def _collapse_split(self, empty_child):
        """Collapse the split, keeping the non-empty child's content."""
        if not self._splitter or len(self._children) != 2:
            return
        
        # Find the surviving child (the one that's not empty)
        surviving_child = None
        for child in self._children:
            if child != empty_child:
                surviving_child = child
                break
        
        if not surviving_child:
            return
        
        # Get the tab widget from the surviving child
        surviving_tw = surviving_child._tab_widget
        if not surviving_tw:
            return
        
        # Remove the splitter
        self._layout.removeWidget(self._splitter)
        
        # Clean up children
        for child in self._children:
            child.setParent(None)
            child.deleteLater()
        self._children = []
        
        # Delete splitter
        self._splitter.deleteLater()
        self._splitter = None
        
        # Disconnect signals from the surviving child before taking ownership
        surviving_child._disconnect_tab_widget(surviving_tw)
        
        # Take ownership of the surviving tab widget
        self._tab_widget = surviving_tw
        self._tab_widget.setParent(self)
        self._tab_widget.tab_drag_started.connect(self._on_tab_drag_started)
        self._tab_widget.tab_drag_ended.connect(self._on_tab_drag_ended)
        self._layout.addWidget(self._tab_widget)
