import pytest
import yaml
import os
from usdm3.ct.cdisc.library_cache.library_cache import LibraryCache


@pytest.fixture
def temp_file():
    """Fixture to create a temporary file path"""
    return str("tests/files/test_library.yaml")


@pytest.fixture
def sample_data():
    """Fixture providing sample data to save/read"""
    return {"test_key": "test_value", "nested": {"key": "value"}, "list": [1, 2, 3]}


def test_initialization():
    """Test LibraryFile initialization"""
    filename = "test.yaml"
    path = "/some/path"
    lib_file = LibraryCache(path, filename)
    assert lib_file._filename == filename
    assert lib_file._path == path


def test_delete_file(temp_file):
    """Test deleting a file"""
    try:
        os.remove(temp_file)  # Make sure file is deleted
    except Exception:
        pass
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    lib_file.save(sample_data)
    lib_file.delete()
    assert not os.path.isfile(temp_file)


def test_save_new_file(temp_file, sample_data):
    """Test saving data to a new file"""
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    lib_file.save(sample_data)

    # Verify file exists
    assert os.path.isfile(temp_file)

    # Verify content
    with open(temp_file) as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == sample_data


def test_save_existing_file(temp_file, sample_data):
    """Test save doesn't overwrite existing file"""
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    lib_file.save(sample_data)

    # Try to save different data
    different_data = {"different": "data"}
    lib_file.save(different_data)

    # Verify original content remains
    with open(temp_file) as f:
        saved_data = yaml.safe_load(f)
    assert saved_data == sample_data


def test_read_existing_file(temp_file, sample_data):
    """Test reading from an existing file"""
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    lib_file.save(sample_data)

    # Read and verify content
    read_data = lib_file.read()
    assert read_data == sample_data


def test_read_nonexistent_file(temp_file):
    """Test reading from a non-existent file raises exception"""
    os.remove(temp_file)  # Make sure file is deleted
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    with pytest.raises(Exception) as exc_info:
        lib_file.read()
    assert "Failed to read CDSIC CT file, does not exist" in str(exc_info.value)


def test_file_exist(temp_file):
    """Test _file_exist method"""
    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)

    # Test non-existent file
    assert not lib_file._file_exist()

    # Create file and test again
    with open(temp_file, "w") as f:
        f.write("")
    assert lib_file._file_exist()


def test_save_with_invalid_permissions(tmp_path):
    """Test save with insufficient permissions"""
    # Create a read-only directory
    readonly_dir = tmp_path / "readonly"
    readonly_dir.mkdir()
    readonly_dir.chmod(0o555)  # Read and execute only

    filename = "test.yaml"
    path = str(readonly_dir)
    lib_file = LibraryCache(path, filename)

    with pytest.raises(Exception) as exc_info:
        lib_file.save({"test": "data"})
    assert "failed to save CDSIC CT file" in str(exc_info.value)


def test_read_with_invalid_yaml(temp_file):
    """Test reading invalid YAML content"""
    # Create file with invalid YAML
    with open(temp_file, "w") as f:
        f.write("invalid: yaml: content: :")

    path = os.path.dirname(temp_file)
    filename = os.path.basename(temp_file)
    lib_file = LibraryCache(path, filename)
    with pytest.raises(Exception) as exc_info:
        lib_file.read()
    assert "failed to read CDSIC CT file" in str(exc_info.value)
