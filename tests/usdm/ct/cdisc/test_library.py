import pytest
from unittest.mock import Mock, patch
from usdm3.ct.cdisc.library import Library

@pytest.fixture
def sample_codelist():
    """Sample codelist data structure"""
    return {
        "conceptId": "C123",
        "terms": [
            {
                "conceptId": "T1",
                "submissionValue": "VAL1",
                "preferredTerm": "Term 1"
            },
            {
                "conceptId": "T2",
                "submissionValue": "VAL2",
                "preferredTerm": "Term 2"
            }
        ]
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
            {
                "conceptId": "T1",
                "submissionValue": "VAL1",
                "preferredTerm": "Term 1"
            }
        ]
    }
    return mock

@pytest.fixture
def mock_file():
    """Mock LibraryFile class"""
    mock = Mock()
    mock.file_exist.return_value = False
    return mock

@pytest.fixture
def library(tmp_path):
    """Create a Library instance with default path"""
    return Library(str(tmp_path), "test.yaml")

def test_library_initialization(library):
    """Test Library initialization"""
    assert hasattr(library, '_config')
    assert hasattr(library, '_missing')
    assert hasattr(library, '_api')
    assert hasattr(library, '_file')
    assert isinstance(library._by_code_list, dict)
    assert isinstance(library._by_term, dict)
    assert isinstance(library._by_submission, dict)
    assert isinstance(library._by_pt, dict)

@patch('usdm3.ct.cdisc.library.LibraryAPI')
@patch('usdm3.ct.cdisc.library.LibraryFile')
@patch('usdm3.ct.cdisc.library.Config')
@patch('usdm3.ct.cdisc.library.Missing')
def test_load_from_api(mock_missing_cls, mock_config_cls, mock_file_cls, mock_api_cls, 
                      sample_codelist, tmp_path):
    """Test loading data from API when cache doesn't exist"""
    # Setup mocks
    mock_file = mock_file_cls.return_value
    mock_file.file_exist.return_value = False
    
    mock_api = mock_api_cls.return_value
    mock_api.code_list.return_value = sample_codelist
    
    mock_config = mock_config_cls.return_value
    mock_config.required_code_lists.return_value = ["C123"]
    
    # Create library and load data
    library = Library(str(tmp_path), "test.yaml")
    library.load()
    
    # Verify API was called
    mock_api.refresh.assert_called_once()
    mock_api.code_list.assert_called_once_with("C123")
    
    # Verify data was cached
    mock_file.save.assert_called_once()
    
    # Verify indexes were built
    assert library._by_code_list["C123"] == sample_codelist
    assert "T1" in library._by_term
    assert "VAL1" in library._by_submission
    assert "Term 1" in library._by_pt

@patch('usdm3.ct.cdisc.library.LibraryAPI')
@patch('usdm3.ct.cdisc.library.LibraryFile')
@patch('usdm3.ct.cdisc.library.Config')
@patch('usdm3.ct.cdisc.library.Missing')
def test_load_from_cache(mock_missing_cls, mock_config_cls, mock_file_cls, mock_api_cls,
                        sample_codelist, tmp_path):
    """Test loading data from cache when it exists"""
    # Setup mocks
    mock_file = mock_file_cls.return_value
    mock_file.file_exist.return_value = True
    mock_file.read.return_value = {"C123": sample_codelist}
    
    # Create library and load data
    library = Library(str(tmp_path), "test.yaml")
    library.load()
    
    # Verify API was not called
    mock_api_cls.return_value.refresh.assert_not_called()
    mock_api_cls.return_value.code_list.assert_not_called()
    
    # Verify cache was read
    mock_file.read.assert_called_once()
    
    # Verify indexes were built
    assert library._by_code_list["C123"] == sample_codelist
    assert "T1" in library._by_term
    assert "VAL1" in library._by_submission
    assert "Term 1" in library._by_pt

def test_refresh(library):
    """Test refresh method"""
    library.refresh()
    # Verify API refresh was called
    assert library._api.refresh.called

def test_klass_and_attribute(library):
    """Test klass_and_attribute method"""
    # Setup test data
    library._by_code_list["C123"] = {"test": "data"}
    library._config.klass_and_attribute.return_value = "C123"
    
    # Test valid lookup
    result = library.klass_and_attribute("TestClass", "testAttr")
    assert result == {"test": "data"}
    
    # Test invalid lookup
    library._config.klass_and_attribute.side_effect = Exception("Not found")
    result = library.klass_and_attribute("InvalidClass", "invalidAttr")
    assert result is None

def test_check_in_and_add(library):
    """Test _check_in_and_add helper method"""
    collection = {}
    
    # Test adding new item
    library._check_in_and_add(collection, "key1", "value1")
    assert collection["key1"] == ["value1"]
    
    # Test adding to existing key
    library._check_in_and_add(collection, "key1", "value2")
    assert collection["key1"] == ["value1", "value2"]

@patch('usdm3.ct.cdisc.library.LibraryAPI')
@patch('usdm3.ct.cdisc.library.LibraryFile')
@patch('usdm3.ct.cdisc.library.Config')
@patch('usdm3.ct.cdisc.library.Missing')
def test_add_missing_ct(mock_missing_cls, mock_config_cls, mock_file_cls, mock_api_cls,
                       sample_codelist, tmp_path):
    """Test adding missing controlled terminology"""
    # Setup mock
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = [sample_codelist]
    
    # Create library and add missing CT
    library = Library(str(tmp_path), "test.yaml")
    library._add_missing_ct()
    
    # Verify indexes were built for missing CT
    assert library._by_code_list["C123"] == sample_codelist
    assert "T1" in library._by_term
    assert "VAL1" in library._by_submission
    assert "Term 1" in library._by_pt