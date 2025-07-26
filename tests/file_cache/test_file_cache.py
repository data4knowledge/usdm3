import pytest
import os
import tempfile
import shutil
import yaml
from unittest.mock import patch
from usdm3.file_cache.file_cache import FileCache


class TestFileCache:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.filename = "test_cache.yaml"
        self.cache = FileCache(self.temp_dir, self.filename)

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test FileCache initialization."""
        assert self.cache.filepath == self.temp_dir
        assert self.cache.filename == self.filename
        assert self.cache._full_filepath() == os.path.join(self.temp_dir, self.filename)

    def test_exists_false_when_no_file(self):
        """Test exists method returns False when file doesn't exist."""
        assert self.cache.exists() is False

    def test_exists_true_when_file_exists(self):
        """Test exists method returns True when file exists."""
        # Create the file
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, "w") as f:
            f.write("test: data")

        assert self.cache.exists() is True

    def test_save_creates_file(self):
        """Test save method creates file with data."""
        test_data = {"key1": "value1", "key2": {"nested": "value2"}}

        # Initially file doesn't exist
        assert self.cache.exists() is False

        # Save data
        self.cache.save(test_data)

        # File should now exist
        assert self.cache.exists() is True

        # Verify file contents
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data == test_data

    def test_save_does_not_overwrite_existing_file(self):
        """Test save method does not overwrite existing file."""
        # Create initial file
        initial_data = {"initial": "data"}
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, "w") as f:
            yaml.dump(initial_data, f)

        # Try to save new data
        new_data = {"new": "data"}
        self.cache.save(new_data)

        # File should still contain initial data
        with open(full_path, "r") as f:
            saved_data = yaml.safe_load(f)

        assert saved_data == initial_data
        assert saved_data != new_data

    def test_read_existing_file(self):
        """Test reading existing file."""
        test_data = {"test_key": "test_value", "nested": {"inner_key": "inner_value"}}

        # Create file with test data
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, "w") as f:
            yaml.dump(test_data, f)

        # Read data using cache
        read_data = self.cache.read()

        assert read_data == test_data

    def test_read_nonexistent_file_raises_exception(self):
        """Test reading non-existent file raises exception."""
        with pytest.raises(Exception) as exc_info:
            self.cache.read()

        assert "Failed to read file" in str(exc_info.value)
        assert "does not exist" in str(exc_info.value)

    def test_delete_existing_file(self):
        """Test deleting existing file."""
        # Create file first
        full_path = os.path.join(self.temp_dir, self.filename)
        with open(full_path, "w") as f:
            f.write("test data")

        assert self.cache.exists() is True

        # Delete file
        self.cache.delete()

        assert self.cache.exists() is False

    def test_delete_nonexistent_file_does_not_raise_exception(self):
        """Test deleting non-existent file does not raise exception."""
        # This should not raise an exception
        self.cache.delete()
        # File still doesn't exist
        assert not self.cache.exists()

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
        with open(full_path, "w") as f:
            f.write("test")

        # Now file exists
        assert self.cache._file_exists() is True

    @patch("builtins.open", side_effect=IOError("Permission denied"))
    def test_save_exception_handling(self, mock_open):
        """Test save method exception handling."""
        test_data = {"test": "data"}

        with pytest.raises(Exception) as exc_info:
            self.cache.save(test_data)

        assert "Failed to save file" in str(exc_info.value)
        assert "Permission denied" in str(exc_info.value)

    @patch("builtins.open", side_effect=IOError("Read error"))
    def test_read_exception_handling(self, mock_open):
        """Test read method exception handling when file exists but can't be read."""
        # Mock file exists to return True
        with patch.object(self.cache, "_file_exists", return_value=True):
            with pytest.raises(Exception) as exc_info:
                self.cache.read()

        assert "Failed to read file" in str(exc_info.value)
        assert "Read error" in str(exc_info.value)

    @patch("os.remove", side_effect=OSError("Delete error"))
    def test_delete_exception_handling(self, mock_remove):
        """Test delete method exception handling - should not raise exception."""
        # The delete method should not raise an exception even if os.remove fails
        self.cache.delete()
        # Test passes if no exception is raised
        assert True

    def test_save_with_complex_data_structure(self):
        """Test saving complex data structure."""
        complex_data = {
            "string": "test",
            "number": 42,
            "float": 3.14,
            "boolean": True,
            "null": None,
            "list": [1, 2, 3, "four"],
            "nested_dict": {
                "inner_list": ["a", "b", "c"],
                "inner_dict": {"deep_value": "deep"},
            },
        }

        self.cache.save(complex_data)
        read_data = self.cache.read()

        assert read_data == complex_data

    def test_save_with_empty_data(self):
        """Test saving empty data."""
        empty_data = {}

        self.cache.save(empty_data)
        read_data = self.cache.read()

        assert read_data == empty_data

    def test_different_filename_and_filepath(self):
        """Test with different filename and filepath."""
        different_dir = tempfile.mkdtemp()
        different_filename = "different.yaml"

        try:
            cache = FileCache(different_dir, different_filename)
            test_data = {"different": "test"}

            cache.save(test_data)
            read_data = cache.read()

            assert read_data == test_data
            assert cache._full_filepath() == os.path.join(
                different_dir, different_filename
            )

        finally:
            if os.path.exists(different_dir):
                shutil.rmtree(different_dir)

    def test_save_and_read_integration(self):
        """Test integration of save and read operations."""
        sample_data = {
            "test_key": "test_value",
            "nested": {"key": "value"},
            "list": [1, 2, 3],
        }

        # Save data
        self.cache.save(sample_data)

        # Verify file exists
        assert self.cache.exists() is True

        # Read data back
        read_data = self.cache.read()

        # Verify data matches
        assert read_data == sample_data
