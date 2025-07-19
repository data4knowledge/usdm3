import pytest
import os
import tempfile
import shutil
from usdm3.bc.cdisc.library_cache.library_cache import LibraryCache


class TestLibraryCache:
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.filename = "test_cache.yaml"
        self.cache = LibraryCache(self.temp_dir, self.filename)
        
    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)
    
    def test_initialization(self):
        """Test LibraryCache initialization."""
        assert self.cache.filepath == self.temp_dir
        assert self.cache.filename == self.filename
        assert isinstance(self.cache, LibraryCache)
    
    def test_inheritance_from_file_cache(self):
        """Test that LibraryCache inherits from FileCache."""
        from usdm3.file_cache.file_cache import FileCache
        assert isinstance(self.cache, FileCache)
    
    def test_exists_false_when_no_file(self):
        """Test exists method returns False when file doesn't exist."""
        assert self.cache.exists() is False
    
    def test_save_and_exists(self):
        """Test saving data and checking existence."""
        test_data = {
            'BC1': {
                'name': 'Test BC',
                'synonyms': ['TEST']
            }
        }
        
        # Initially file doesn't exist
        assert self.cache.exists() is False
        
        # Save data
        self.cache.save(test_data)
        
        # Now file should exist
        assert self.cache.exists() is True
    
    def test_save_and_read(self):
        """Test saving and reading data."""
        test_data = {
            'BC1': {
                'name': 'Test BC',
                'synonyms': ['TEST'],
                'properties': []
            },
            'BC2': {
                'name': 'Another BC',
                'synonyms': ['ANOTHER'],
                'properties': []
            }
        }
        
        # Save data
        self.cache.save(test_data)
        
        # Read data back
        read_data = self.cache.read()
        
        assert read_data == test_data
    
    def test_delete_file(self):
        """Test deleting cache file."""
        test_data = {'test': 'data'}
        
        # Save data first
        self.cache.save(test_data)
        assert self.cache.exists() is True
        
        # Delete file
        self.cache.delete()
        assert self.cache.exists() is False
    
    def test_read_nonexistent_file_raises_exception(self):
        """Test reading non-existent file raises exception."""
        with pytest.raises(Exception) as exc_info:
            self.cache.read()
        
        assert "Failed to read file" in str(exc_info.value)
        assert "does not exist" in str(exc_info.value)
    
    def test_delete_nonexistent_file_raises_exception(self):
        """Test deleting non-existent file raises exception."""
        with pytest.raises(Exception) as exc_info:
            self.cache.delete()
        
        assert "Failed to delete file" in str(exc_info.value)
