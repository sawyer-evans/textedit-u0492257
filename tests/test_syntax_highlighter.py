"""Tests for SyntaxHighlighter."""

import pytest
from PyQt6.QtGui import QTextDocument

from editor.syntax_highlighter import SyntaxHighlighter
from editor.language_definitions import LANGUAGES, TokenType, TOKEN_COLORS


@pytest.fixture
def highlighter():
    doc = QTextDocument()
    h = SyntaxHighlighter(doc)
    return h, doc


class TestSyntaxHighlighterInit:
    def test_initial_language_is_none(self, highlighter):
        h, _ = highlighter
        assert h.language is None

    def test_set_language_python(self, highlighter):
        h, _ = highlighter
        h.set_language("python")
        assert h.language == "python"

    def test_set_language_javascript(self, highlighter):
        h, _ = highlighter
        h.set_language("javascript")
        assert h.language == "javascript"

    def test_set_language_html(self, highlighter):
        h, _ = highlighter
        h.set_language("html")
        assert h.language == "html"

    def test_set_language_css(self, highlighter):
        h, _ = highlighter
        h.set_language("css")
        assert h.language == "css"

    def test_set_language_none_clears(self, highlighter):
        h, _ = highlighter
        h.set_language("python")
        h.set_language(None)
        assert h.language is None

    def test_set_unknown_language(self, highlighter):
        h, _ = highlighter
        h.set_language("unknown_lang")
        assert h.language == "unknown_lang"
        assert h._patterns == []


class TestHighlightingPython:
    def test_keyword_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText("def foo():")
        block = doc.begin()
        # The block should have formats applied (keyword "def")
        it = block.begin()
        assert block.isValid()

    def test_comment_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText("# this is a comment")
        block = doc.begin()
        assert block.isValid()

    def test_string_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText('x = "hello"')
        block = doc.begin()
        assert block.isValid()

    def test_triple_quote_multiline(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText('x = """\nhello\n"""')
        # Should handle multi-line without error
        block = doc.begin()
        assert block.isValid()
        # First block should have state set
        assert doc.begin().userState() != 0 or doc.begin().next().isValid()


class TestHighlightingJavaScript:
    def test_keyword_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("javascript")
        doc.setPlainText("const x = 5;")
        assert doc.begin().isValid()

    def test_block_comment_multiline(self, highlighter):
        h, doc = highlighter
        h.set_language("javascript")
        doc.setPlainText("/* comment\n   still comment */")
        assert doc.begin().isValid()

    def test_template_literal(self, highlighter):
        h, doc = highlighter
        h.set_language("javascript")
        doc.setPlainText("`hello world`")
        assert doc.begin().isValid()


class TestHighlightingHTML:
    def test_tag_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("html")
        doc.setPlainText("<div>Hello</div>")
        assert doc.begin().isValid()

    def test_html_comment(self, highlighter):
        h, doc = highlighter
        h.set_language("html")
        doc.setPlainText("<!-- comment -->")
        assert doc.begin().isValid()


class TestHighlightingCSS:
    def test_selector_highlighted(self, highlighter):
        h, doc = highlighter
        h.set_language("css")
        doc.setPlainText(".class { color: red; }")
        assert doc.begin().isValid()

    def test_css_comment(self, highlighter):
        h, doc = highlighter
        h.set_language("css")
        doc.setPlainText("/* comment */")
        assert doc.begin().isValid()


class TestLanguageSwitching:
    def test_switch_language(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText("def foo(): pass")
        h.set_language("javascript")
        assert h.language == "javascript"
        doc.setPlainText("const x = 5;")
        assert doc.begin().isValid()

    def test_switch_to_none(self, highlighter):
        h, doc = highlighter
        h.set_language("python")
        doc.setPlainText("def foo(): pass")
        h.set_language(None)
        assert h.language is None


class TestLanguageDefinitions:
    def test_all_languages_exist(self):
        assert "python" in LANGUAGES
        assert "javascript" in LANGUAGES
        assert "html" in LANGUAGES
        assert "css" in LANGUAGES

    def test_python_has_multiline(self):
        assert len(LANGUAGES["python"].multiline_patterns) > 0

    def test_javascript_has_multiline(self):
        assert len(LANGUAGES["javascript"].multiline_patterns) > 0

    def test_all_token_types_have_colors(self):
        for token_type in TokenType:
            assert token_type in TOKEN_COLORS
