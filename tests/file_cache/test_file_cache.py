import pytest
import yaml
import os
import pathlib
from usdm3.ct.cdisc.library_cache.library_cache import LibraryCache


@pytest.fixture
def temp_dir():
    return pathlib.Path(__file__).parent.resolve()


@pytest.fixture
def temp_file():
    return str("test_library.yaml")


@pytest.fixture
def sample_data():
    """Fixture providing sample data to save/read"""
    return {"test_key": "test_value", "nested": {"key": "value"}, "list": [1, 2, 3]}


def test_initialization(temp_dir, temp_file):
    """Test LibraryFile initialization"""
    lib_file = LibraryCache(temp_dir, temp_file)
    assert lib_file.filename == "test_library.yaml"
    assert lib_file.filepath == temp_dir
    assert lib_file._full_filepath() == os.path.join(temp_dir, temp_file)


def test_delete_file(temp_dir, temp_file):
    """Test deleting a file"""
    try:
        os.remove(temp_file)  # Make sure file is deleted
    except Exception:
        pass
    lib_file = LibraryCache(temp_dir, temp_file)
    lib_file.save(sample_data)
    lib_file.delete()
    assert not os.path.isfile(temp_file)


def test_save_new_file(temp_dir, sample_data):
    """Test saving data to a new file"""
    lib_file = LibraryCache(temp_dir, "new.yaml")
    lib_file.save(sample_data)
    path = lib_file._full_filepath()

    # Verify file exists
    assert os.path.isfile(path)
    with open(path) as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == sample_data
    lib_file.delete()


def test_read_existing_file(temp_dir, temp_file, sample_data):
    """Test reading from an existing file"""
    lib_file = LibraryCache(temp_dir, temp_file)
    lib_file.save(sample_data)

    # Read and verify content
    read_data = lib_file.read()
    assert read_data == sample_data


def test_read_nonexistent_file(
    temp_dir,
):
    """Test reading from a non-existent file raises exception"""
    lib_file = LibraryCache(temp_dir, "test_library_cache.yaml")
    with pytest.raises(Exception) as exc_info:
        lib_file.read()
    assert "Failed to read CDSIC CT file, does not exist" in str(exc_info.value)


def test_file_exist(temp_dir, temp_file):
    """Test _file_exist method"""
    lib_file = LibraryCache(temp_dir, temp_file)
    assert lib_file.exists()
    lib_file.delete()
    assert not lib_file.exists()
