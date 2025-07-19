import pytest
import yaml
import os
import tempfile
import shutil
from usdm3.ct.cdisc.library_cache.library_cache import LibraryCache


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
            'CT1': {
                'name': 'Test CT',
                'terms': ['TEST']
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
            'CT1': {
                'name': 'Test CT',
                'terms': ['TEST'],
                'properties': []
            },
            'CT2': {
                'name': 'Another CT',
                'terms': ['ANOTHER'],
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
    
    def test_delete_nonexistent_file_does_not_raise_exception(self):
        """Test deleting non-existent file does not raise exception."""
        # This should not raise an exception
        self.cache.delete()
        # File still doesn't exist
        assert not self.cache.exists()
    
    def test_save_does_not_overwrite_existing_file(self):
        """Test save method does not overwrite existing file."""
        # Create initial file
        initial_data = {'initial': 'data'}
        self.cache.save(initial_data)
        
        # Try to save new data
        new_data = {'new': 'data'}
        self.cache.save(new_data)
        
        # File should still contain initial data
        read_data = self.cache.read()
        assert read_data == initial_data
        assert read_data != new_data
    
    def test_full_filepath(self):
        """Test _full_filepath method."""
        expected_path = os.path.join(self.temp_dir, self.filename)
        assert self.cache._full_filepath() == expected_path
    
    def test_file_exists_private_method(self):
        """Test _file_exists private method."""
        # Initially file doesn't exist
        assert self.cache._file_exists() is False
        
        # Create file
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, 'w') as f:
            f.write("test")
        
        # Now file exists
        assert self.cache._file_exists() is True
