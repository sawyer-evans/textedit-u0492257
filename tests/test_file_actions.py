"""Tests for file operations."""

import tempfile
import os


class TestNewFile:
    def test_new_file_clears_editor(self, main_window):
        main_window.editor.setPlainText("some content")
        main_window.document.is_modified = False
        
        main_window.file_actions.new_file()
        
        assert main_window.editor.toPlainText() == ""
    
    def test_new_file_resets_document(self, main_window):
        main_window.document.file_path = "/some/path.txt"
        main_window.document.is_modified = False
        
        main_window.file_actions.new_file()
        
        assert main_window.document.file_path is None
        assert main_window.document.is_modified is False


class TestOpenFile:
    def test_open_file_loads_content(self, main_window):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("test content")
            temp_path = f.name
        
        try:
            main_window.file_actions.open_file(temp_path)
            
            assert main_window.editor.toPlainText() == "test content"
            assert main_window.document.file_path == temp_path
            assert main_window.document.is_modified is False
        finally:
            os.unlink(temp_path)
    
    def test_open_nonexistent_file_returns_false(self, main_window):
        result = main_window.file_actions.open_file("/nonexistent/path.txt")
        assert result is False


class TestSaveFile:
    def test_save_file_writes_content(self, main_window):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name
        
        try:
            main_window.editor.setPlainText("saved content")
            main_window.document.file_path = temp_path
            main_window.document.is_modified = True
            
            result = main_window.file_actions.save_file()
            
            assert result is True
            assert main_window.document.is_modified is False
            
            with open(temp_path, "r") as f:
                assert f.read() == "saved content"
        finally:
            os.unlink(temp_path)
    
    def test_save_preserves_file_path(self, main_window):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            temp_path = f.name
        
        try:
            main_window.editor.setPlainText("content")
            main_window.document.file_path = temp_path
            
            main_window.file_actions.save_file()
            
            assert main_window.document.file_path == temp_path
        finally:
            os.unlink(temp_path)
