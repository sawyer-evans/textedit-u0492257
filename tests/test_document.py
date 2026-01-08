"""Tests for Document model."""


class TestDocument:
    def test_initial_state(self, document):
        assert document.file_path is None
        assert document.is_modified is False
    
    def test_display_name_untitled(self, document):
        assert document.display_name == "Untitled"
    
    def test_display_name_with_path(self, document):
        document.file_path = "/home/user/test.txt"
        assert document.display_name == "test.txt"
    
    def test_modified_state(self, document):
        document.is_modified = True
        assert document.is_modified is True
    
    def test_reset(self, document):
        document.file_path = "/some/path.txt"
        document.is_modified = True
        
        document.reset()
        
        assert document.file_path is None
        assert document.is_modified is False
