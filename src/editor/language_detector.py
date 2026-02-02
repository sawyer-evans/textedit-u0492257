"""Detect programming language from file extension."""

import os


class LanguageDetector:
    """Detects language from file path extension."""

    EXTENSION_MAP = {
        ".py": "python",
        ".pyw": "python",
        ".js": "javascript",
        ".mjs": "javascript",
        ".cjs": "javascript",
        ".jsx": "javascript",
        ".html": "html",
        ".htm": "html",
        ".css": "css",
    }

    @staticmethod
    def detect_language(file_path):
        """Return language name for the given file path, or None."""
        if not file_path:
            return None
        _, ext = os.path.splitext(file_path)
        return LanguageDetector.EXTENSION_MAP.get(ext.lower())
