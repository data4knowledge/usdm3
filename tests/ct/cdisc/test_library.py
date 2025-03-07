import os
import pytest
from unittest.mock import Mock, patch
from usdm3.ct.cdisc.library import Library


@pytest.fixture
def sample_codelist():
    """Sample codelist data structure"""
    return {
        "conceptId": "C123",
        "terms": [
            {"conceptId": "T1", "submissionValue": "VAL1", "preferredTerm": "Term 1"},
            {"conceptId": "T2", "submissionValue": "VAL2", "preferredTerm": "Term 2"},
        ],
    }


@pytest.fixture
def mock_config():
    """Mock Config class"""
    mock = Mock()
    mock.required_code_lists.return_value = ["C123"]
    mock.klass_and_attribute.return_value = "C123"
    return mock


@pytest.fixture
def mock_missing():
    """Mock Missing class"""
    mock = Mock()
    mock.code_lists.return_value = []
    return mock


@pytest.fixture
def mock_api():
    """Mock LibraryAPI class"""
    mock = Mock()
    mock.code_list.return_value = {
        "conceptId": "C123",
        "terms": [
            {"conceptId": "T1", "submissionValue": "VAL1", "preferredTerm": "Term 1"}
        ],
    }
    return mock


@pytest.fixture
def mock_cache():
    """Mock LibraryFile class"""
    mock = Mock()
    mock.exists.return_value = False
    return mock


@pytest.fixture
def library(tmp_path):
    filename = "ct_config.yaml"
    config_content = """
    code_lists:
      - "codelist1"
      - "codelist2"
    packages:
      - "package1"
      - "package2"
    klass_attribute_mapping:
      TestClass:
        testAttribute: "test-codelist"
    """
    os.mkdir(tmp_path / "config")
    config_file = tmp_path / "config" / filename
    config_file.write_text(config_content)
    return Library(tmp_path)


def test_library_initialization(library):
    """Test Library initialization"""
    assert hasattr(library, "_config")
    assert hasattr(library, "_missing")
    assert hasattr(library, "_api")
    assert hasattr(library, "_cache")
    assert isinstance(library._by_code_list, dict)
    assert isinstance(library._by_term, dict)
    assert isinstance(library._by_submission, dict)
    assert isinstance(library._by_pt, dict)


@patch("usdm3.ct.cdisc.library.LibraryAPI")
@patch("usdm3.ct.cdisc.library.LibraryCache")
@patch("usdm3.ct.cdisc.library.Config")
def test_load_from_api(
    mock_config_cls,
    mock_cache_cls,
    mock_api_cls,
    sample_codelist,
):
    """Test loading data from API when cache doesn't exist"""
    # Setup mocks
    mock_cache = mock_cache_cls.return_value
    mock_cache.exists.return_value = False
    mock_cache.save.return_value = None

    mock_api = mock_api_cls.return_value
    mock_api.refresh.return_value = None
    mock_api.code_list.return_value = sample_codelist

    mock_config = mock_config_cls.return_value
    mock_config.required_code_lists.return_value = ["C123"]

    # Create library and load data
    library = Library("xxx")
    library.load()

    # Verify API was called
    mock_api.refresh.assert_called_once()
    mock_api.code_list.assert_called_once_with("C123")

    # Verify data was cached
    mock_cache.save.assert_called_once()

    # Verify indexes were built
    assert library._by_code_list["C123"] == sample_codelist
    assert "T1" in library._by_term
    assert "VAL1" in library._by_submission
    assert "Term 1" in library._by_pt

    library._cache.delete()


@patch("usdm3.ct.cdisc.library.LibraryAPI")
@patch("usdm3.ct.cdisc.library.LibraryCache")
def test_load_from_cache(mock_cache_cls, mock_api_cls, sample_codelist, library):
    """Test loading data from cache when it exists"""
    # Setup mocks
    mock_cache = mock_cache_cls.return_value
    mock_cache.exists.return_value = True
    mock_cache.read.return_value = {"C123": sample_codelist}

    # Create library and load data
    library.load()

    # Verify API was not called
    mock_api_cls.return_value.refresh.assert_not_called()
    mock_api_cls.return_value.code_list.assert_not_called()

    # Verify cache was read
    mock_cache.read.assert_called_once()

    # Verify indexes were built
    assert library._by_code_list["C123"] == sample_codelist
    assert "T1" in library._by_term
    assert "VAL1" in library._by_submission
    assert "Term 1" in library._by_pt


@patch("usdm3.ct.cdisc.library.Config")
def test_klass_and_attribute(mock_config_cls):
    """Test klass_and_attribute method"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    # Setup mock config
    mock_config = mock_config_cls.return_value

    # Setup test data
    test_data = {"test": "data"}
    library._by_code_list["C123"] = test_data
    mock_config.klass_and_attribute.return_value = "C123"

    # Test valid lookup
    result = library.klass_and_attribute("TestClass", "testAttr")
    assert result == test_data
    mock_config.klass_and_attribute.assert_called_once_with("TestClass", "testAttr")

    # Test invalid lookup
    mock_config.klass_and_attribute.side_effect = Exception("Not found")
    result = library.klass_and_attribute("InvalidClass", "invalidAttr")
    assert result is None
