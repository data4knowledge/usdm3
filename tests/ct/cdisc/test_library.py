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
    os.mkdir(tmp_path / "ct")
    os.mkdir(tmp_path / "ct" / "cdisc")
    os.mkdir(tmp_path / "ct" / "cdisc" / "config")
    os.mkdir(tmp_path / "ct" / "cdisc" / "missing")
    config_file = tmp_path / "ct" / "cdisc" / "config" / filename
    config_file.write_text(config_content)
    missing_file = tmp_path / "ct" / "cdisc" / "missing" / "missing_ct.yaml"
    missing_file.write_text("[]")
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
@patch("usdm3.ct.cdisc.library.Missing")
def test_load_from_api(
    mock_missing_cls,
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

    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}


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
    local_library = Library(
        library.root_path
    )  # Borrowing the file path from the fixture, bit naughty.
    local_library.load()

    # Verify API was not called
    mock_api_cls.return_value.refresh.assert_not_called()
    mock_api_cls.return_value.code_list.assert_not_called()

    # Verify cache was read
    mock_cache.read.assert_called_once()

    # Verify indexes were built
    assert local_library._by_code_list["C123"] == sample_codelist
    assert "T1" in local_library._by_term
    assert "VAL1" in local_library._by_submission
    assert "Term 1" in local_library._by_pt

@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_klass_and_attribute(mock_missing_cls, mock_config_cls):
    """Test klass_and_attribute method"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value

    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

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

@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_cl_by_term(mock_missing_cls, mock_config_cls):
    """Test klass_and_attribute method"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value

    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data
    test_data = {"test": "data"}
    library._by_term["C123"] = ["C456"]
    library._by_code_list["C456"] = test_data

    # Test valid lookup
    result = library.cl_by_term("C123")
    assert result == test_data

    # Test invalid lookup
    result = library.cl_by_term("Cxxx")
    assert result is None


@pytest.fixture
def sample_units_codelist():
    """Sample units codelist data structure for testing unit method"""
    return {
        "conceptId": "C71620",
        "terms": [
            {"conceptId": "C48155", "submissionValue": "kg", "preferredTerm": "Kilogram"},
            {"conceptId": "C28253", "submissionValue": "g", "preferredTerm": "Gram"},
            {"conceptId": "C48570", "submissionValue": "mg", "preferredTerm": "Milligram"},
            {"conceptId": "C25613", "submissionValue": "L", "preferredTerm": "Liter"},
            {"conceptId": "C28254", "submissionValue": "mL", "preferredTerm": "Milliliter"},
        ],
    }


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_valid_lookup_by_concept_id(mock_missing_cls, mock_config_cls, sample_units_codelist):
    """Test unit method with valid concept ID lookup"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data - units codelist
    library._by_code_list["C71620"] = sample_units_codelist

    # Test valid lookup by concept ID
    result = library.unit("C48155")
    expected = {"conceptId": "C48155", "submissionValue": "kg", "preferredTerm": "Kilogram"}
    assert result == expected

    # Test case insensitive lookup
    result = library.unit("c48155")
    assert result == expected


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_valid_lookup_by_submission_value(mock_missing_cls, mock_config_cls, sample_units_codelist):
    """Test unit method with valid submission value lookup"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data - units codelist
    library._by_code_list["C71620"] = sample_units_codelist

    # Test valid lookup by submission value
    result = library.unit("kg")
    expected = {"conceptId": "C48155", "submissionValue": "kg", "preferredTerm": "Kilogram"}
    assert result == expected

    # Test case insensitive lookup
    result = library.unit("KG")
    assert result == expected


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_valid_lookup_by_preferred_term(mock_missing_cls, mock_config_cls, sample_units_codelist):
    """Test unit method with valid preferred term lookup"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data - units codelist
    library._by_code_list["C71620"] = sample_units_codelist

    # Test valid lookup by preferred term
    result = library.unit("Kilogram")
    expected = {"conceptId": "C48155", "submissionValue": "kg", "preferredTerm": "Kilogram"}
    assert result == expected

    # Test case insensitive lookup
    result = library.unit("kilogram")
    assert result == expected


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_invalid_lookup(mock_missing_cls, mock_config_cls, sample_units_codelist):
    """Test unit method with invalid value"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data - units codelist
    library._by_code_list["C71620"] = sample_units_codelist

    # Test invalid lookup
    result = library.unit("invalid_unit")
    assert result is None

    # Test with None value
    result = library.unit(None)
    assert result is None

    # Test with empty string
    result = library.unit("")
    assert result is None


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_missing_codelist(mock_missing_cls, mock_config_cls):
    """Test unit method when units codelist is not available"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Don't setup the units codelist (C71620)
    # This simulates the case where the units codelist is not loaded

    # Test lookup when codelist is missing
    result = library.unit("kg")
    assert result is None


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_malformed_codelist(mock_missing_cls, mock_config_cls):
    """Test unit method with malformed codelist data"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup malformed codelist data (missing 'terms' key)
    library._by_code_list["C71620"] = {"conceptId": "C71620"}

    # Test lookup with malformed data
    result = library.unit("kg")
    assert result is None


@patch("usdm3.ct.cdisc.library.Config")
@patch("usdm3.ct.cdisc.library.Missing")
def test_unit_multiple_matches_returns_first(mock_missing_cls, mock_config_cls):
    """Test unit method returns first match when multiple fields could match"""
    # Create library instance with all dependencies mocked
    library = Library("xxx")

    mock_config = mock_config_cls.return_value
    mock_missing = mock_missing_cls.return_value
    mock_missing.code_lists.return_value = {}

    # Setup test data with potential for multiple matches
    # (conceptId takes precedence over submissionValue and preferredTerm)
    library._by_code_list["C71620"] = {
        "conceptId": "C71620",
        "terms": [
            {"conceptId": "TEST", "submissionValue": "other", "preferredTerm": "Other Term"},
            {"conceptId": "other", "submissionValue": "TEST", "preferredTerm": "Test Term"},
        ],
    }

    # Test that conceptId match takes precedence
    result = library.unit("TEST")
    expected = {"conceptId": "TEST", "submissionValue": "other", "preferredTerm": "Other Term"}
    assert result == expected
