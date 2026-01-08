"""Document model for tracking file state."""


class Document:
    """Tracks file path and modification state."""
    
    def __init__(self):
        self._file_path = None
        self._is_modified = False
    
    @property
    def file_path(self):
        """Current file path, or None if untitled."""
        return self._file_path
    
    @file_path.setter
    def file_path(self, path):
        self._file_path = path
    
    @property
    def is_modified(self):
        """Whether the document has unsaved changes."""
        return self._is_modified
    
    @is_modified.setter
    def is_modified(self, value):
        self._is_modified = value
    
    @property
    def display_name(self):
        """Filename for display, or 'Untitled' if no path."""
        if self._file_path:
            return self._file_path.split("/")[-1]
        return "Untitled"
    
    def reset(self):
        """Reset to initial state for new file."""
        self._file_path = None
        self._is_modified = False
