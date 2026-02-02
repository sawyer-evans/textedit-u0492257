"""Syntax highlighter using QSyntaxHighlighter."""

import re

from PyQt6.QtGui import QSyntaxHighlighter, QTextCharFormat, QColor
from PyQt6.QtCore import Qt

from editor.language_definitions import LANGUAGES, TOKEN_COLORS, TokenType


class SyntaxHighlighter(QSyntaxHighlighter):
    """Multi-language syntax highlighter."""

    def __init__(self, document):
        super().__init__(document)
        self._language = None
        self._patterns = []  # compiled (TokenType, regex) pairs
        self._multiline_patterns = []  # (TokenType, start_re, end_re) compiled
        self._formats = {}
        self._build_formats()

    def _build_formats(self):
        """Build QTextCharFormat for each token type."""
        for token_type, color in TOKEN_COLORS.items():
            fmt = QTextCharFormat()
            fmt.setForeground(QColor(color))
            if token_type == TokenType.KEYWORD:
                fmt.setFontWeight(700)
            if token_type == TokenType.COMMENT:
                fmt.setFontItalic(True)
            self._formats[token_type] = fmt

    def set_language(self, language_name):
        """Set the language for highlighting."""
        if language_name == self._language:
            return
        self._language = language_name
        self._patterns = []
        self._multiline_patterns = []

        if language_name and language_name in LANGUAGES:
            lang_def = LANGUAGES[language_name]
            for token_type, pattern in lang_def.patterns:
                self._patterns.append((token_type, re.compile(pattern)))
            for i, (token_type, start, end) in enumerate(lang_def.multiline_patterns):
                self._multiline_patterns.append(
                    (token_type, re.compile(start), re.compile(end))
                )

        self.rehighlight()

    @property
    def language(self):
        return self._language

    def highlightBlock(self, text):
        """Highlight a single block of text."""
        if not self._language:
            return

        # Track which character positions are already highlighted
        highlighted = set()

        # Handle multi-line patterns first
        for i, (token_type, start_re, end_re) in enumerate(self._multiline_patterns):
            state_bit = i + 1
            self._apply_multiline(text, token_type, start_re, end_re, state_bit, highlighted)

        # Apply single-line patterns (skip already-highlighted regions)
        for token_type, regex in self._patterns:
            for match in regex.finditer(text):
                start = match.start()
                length = match.end() - match.start()
                # Skip if any character in this range is already highlighted
                if any(pos in highlighted for pos in range(start, start + length)):
                    continue
                self.setFormat(start, length, self._formats[token_type])
                highlighted.update(range(start, start + length))

    def _apply_multiline(self, text, token_type, start_re, end_re, state_bit, highlighted):
        """Handle multi-line constructs like triple-quoted strings and block comments."""
        fmt = self._formats[token_type]
        prev_state = self.previousBlockState()
        in_multiline = (prev_state & state_bit) != 0 if prev_state != -1 else False

        start = 0
        text_len = len(text)

        if in_multiline:
            # Continue from previous block - look for end
            match = end_re.search(text, start)
            if match:
                end_pos = match.end()
                self.setFormat(0, end_pos, fmt)
                highlighted.update(range(0, end_pos))
                start = end_pos
                in_multiline = False
            else:
                self.setFormat(0, text_len, fmt)
                highlighted.update(range(0, text_len))
                self._set_state_bit(state_bit, True)
                return

        # Look for new multi-line starts
        while start < text_len:
            match = start_re.search(text, start)
            if not match:
                break
            ms = match.start()
            if any(pos in highlighted for pos in range(ms, ms + len(match.group()))):
                start = match.end()
                continue
            # Look for end on same line
            end_match = end_re.search(text, match.end())
            if end_match:
                end_pos = end_match.end()
                self.setFormat(ms, end_pos - ms, fmt)
                highlighted.update(range(ms, end_pos))
                start = end_pos
            else:
                self.setFormat(ms, text_len - ms, fmt)
                highlighted.update(range(ms, text_len))
                in_multiline = True
                break

        self._set_state_bit(state_bit, in_multiline)

    def _set_state_bit(self, bit, value):
        """Set or clear a bit in the current block state."""
        state = self.currentBlockState()
        if state == -1:
            state = 0
        if value:
            state |= bit
        else:
            state &= ~bit
        self.setCurrentBlockState(state)
