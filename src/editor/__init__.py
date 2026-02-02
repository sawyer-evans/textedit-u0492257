"""Core editor components."""

from .text_editor import TextEditor
from .document import Document
from .syntax_highlighter import SyntaxHighlighter
from .language_detector import LanguageDetector
from .language_definitions import TokenType, LanguageDefinition, LANGUAGES

__all__ = ["TextEditor", "Document", "SyntaxHighlighter", "LanguageDetector",
           "TokenType", "LanguageDefinition", "LANGUAGES"]
