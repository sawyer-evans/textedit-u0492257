"""Tests for LanguageDetector."""

from editor.language_detector import LanguageDetector


class TestLanguageDetector:
    def test_python_extension(self):
        assert LanguageDetector.detect_language("main.py") == "python"

    def test_pyw_extension(self):
        assert LanguageDetector.detect_language("app.pyw") == "python"

    def test_javascript_extension(self):
        assert LanguageDetector.detect_language("index.js") == "javascript"

    def test_mjs_extension(self):
        assert LanguageDetector.detect_language("module.mjs") == "javascript"

    def test_jsx_extension(self):
        assert LanguageDetector.detect_language("component.jsx") == "javascript"

    def test_html_extension(self):
        assert LanguageDetector.detect_language("page.html") == "html"

    def test_htm_extension(self):
        assert LanguageDetector.detect_language("page.htm") == "html"

    def test_css_extension(self):
        assert LanguageDetector.detect_language("style.css") == "css"

    def test_unknown_extension(self):
        assert LanguageDetector.detect_language("data.txt") is None

    def test_no_extension(self):
        assert LanguageDetector.detect_language("Makefile") is None

    def test_none_path(self):
        assert LanguageDetector.detect_language(None) is None

    def test_empty_string(self):
        assert LanguageDetector.detect_language("") is None

    def test_full_path(self):
        assert LanguageDetector.detect_language("/home/user/project/main.py") == "python"

    def test_case_insensitive(self):
        assert LanguageDetector.detect_language("FILE.PY") == "python"
        assert LanguageDetector.detect_language("style.CSS") == "css"
