import pytest
import os
from unittest.mock import Mock, patch
from usdm3.ct.cdisc.library_api import LibraryAPI


@pytest.fixture
def api():
    """Fixture to create a LibraryAPI instance"""
    with patch.dict(os.environ, {"CDISC_API_KEY": "test_api_key"}):
        return LibraryAPI(["ddfct", "sdtmct"])


@pytest.fixture
def mock_response():
    """Fixture to create a mock response"""
    mock = Mock()
    mock.json.return_value = {"data": "test"}
    mock.status_code = 200
    return mock


def test_initialization():
    """Test LibraryAPI initialization"""
    with patch.dict(os.environ, {"CDISC_API_KEY": "test_key"}):
        api = LibraryAPI(["sdtmct", "ddfct"])
        assert api._package_list == ["sdtmct", "ddfct"]
        assert api._packages is None
        assert api._headers["api-key"] == "test_key"
        assert api._headers["Content-Type"] == "application/json"


def test_initialization_no_api_key():
    """Test LibraryAPI initialization without API key"""
    with patch.dict(os.environ, {}, clear=True):
        api = LibraryAPI(["sdtmct"])
        assert api._headers["api-key"] is None


def test_url(api):
    """Test the _url method of LibraryAPI"""
    # Test with simple relative URL
    assert api._url("/test") == "https://api.library.cdisc.org/api/test"

    # Test with empty relative URL
    assert api._url("") == "https://api.library.cdisc.org/api"

    # Test with complex relative URL
    assert (
        api._url("/mdr/ct/packages/sdtmct-2024-01-01")
        == "https://api.library.cdisc.org/api/mdr/ct/packages/sdtmct-2024-01-01"
    )

    # Test with relative URL that already has leading slash
    assert api._url("///test") == "https://api.library.cdisc.org/api///test"


@patch("requests.get")
def test_code_list_success(mock_get, api):
    """Test the code_list method with successful response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conceptId": "C123",
        "terms": [{"term": "test"}],
        "_links": {"self": {"href": "/test"}},
    }
    mock_get.return_value = mock_response
    api._packages = {"ddfct": [{"effective": "2024-01-01"}]}

    result = api.code_list("C123")

    # Verify request was made correctly
    mock_get.assert_called_once_with(
        "https://api.library.cdisc.org/api/mdr/ct/packages/ddfct-2024-01-01/codelists/C123",
        headers=api._headers,
    )

    # Verify response processing
    assert result["conceptId"] == "C123"
    assert result["terms"] == [{"term": "test"}]
    assert "_links" not in result
    assert result["source"]["effective_date"] == "2024-01-01"
    assert result["source"]["package"] == "ddfct"


@patch("requests.get")
def test_code_list_not_found_first_package(mock_get, api):
    """Test code_list method when first package returns 404 but second succeeds"""
    # First call returns 404, second call returns 200
    mock_response_404 = Mock()
    mock_response_404.status_code = 404

    mock_response_200 = Mock()
    mock_response_200.status_code = 200
    mock_response_200.json.return_value = {
        "conceptId": "C123",
        "terms": [{"term": "test"}],
        "_links": {"self": {"href": "/test"}},
    }

    mock_get.side_effect = [mock_response_404, mock_response_200]
    api._packages = {
        "ddfct": [{"effective": "2024-01-01"}],
        "sdtmct": [{"effective": "2024-01-01"}],
    }

    result = api.code_list("C123")

    # Verify both requests were made
    assert mock_get.call_count == 2

    # Verify response processing from second package
    assert result["conceptId"] == "C123"
    assert result["source"]["package"] == "sdtmct"


@patch("requests.get")
def test_code_list_all_packages_fail(mock_get, api):
    """Test code_list method when all packages fail"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    api._packages = {
        "ddfct": [{"effective": "2024-01-01"}],
        "sdtmct": [{"effective": "2024-01-01"}],
    }

    result = api.code_list("invalid-id")
    assert result is None


@patch("requests.get")
def test_code_list_no_package_version(mock_get, api):
    """Test code_list method when package version is None"""
    api._packages = {
        "ddfct": []
    }  # Empty list will cause _package_version to return None

    result = api.code_list("C123")
    assert result is None
    mock_get.assert_not_called()


@patch("requests.get")
def test_all_code_lists_success(mock_get, api):
    """Test all_code_lists method with successful response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "_links": {
            "codelists": [
                {"href": "/mdr/ct/packages/ddfct-2024-01-01/codelists/C12345"},
                {"href": "/mdr/ct/packages/ddfct-2024-01-01/codelists/C67890"},
            ]
        }
    }
    mock_get.return_value = mock_response
    api._packages = {"ddfct": [{"effective": "2024-01-01"}]}

    with patch("builtins.print") as mock_print:
        result = api.all_code_lists()

    # Verify result structure
    assert len(result) == 1
    assert result[0]["effective_date"] == "2024-01-01"
    assert result[0]["package"] == "ddfct"
    assert result[0]["code_lists"] == ["C12345", "C67890"]


@patch("requests.get")
def test_all_code_lists_no_version(mock_get, api):
    """Test all_code_lists method when package has no version"""
    api._packages = {
        "ddfct": []
    }  # Empty list will cause _package_version to return None

    with patch("builtins.print") as mock_print:
        result = api.all_code_lists()

    # Verify no requests were made and empty result
    mock_get.assert_not_called()
    assert result == []


@patch("requests.get")
def test_all_code_lists_request_fails(mock_get, api):
    """Test all_code_lists method when request fails"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response
    api._packages = {"ddfct": [{"effective": "2024-01-01"}]}

    with patch("builtins.print"):
        result = api.all_code_lists()

    # When request fails, no result is appended to results list
    # So we get an empty list
    assert result == []


@patch("requests.get")
def test_package_code_list_success(mock_get, api):
    """Test package_code_list method with successful response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "conceptId": "C123",
        "terms": [{"term": "test"}],
        "_links": {"self": {"href": "/test"}},
    }
    mock_get.return_value = mock_response

    result = api.package_code_list("sdtmct", "2024-01-01", "C123")

    # Verify request was made correctly
    mock_get.assert_called_once_with(
        "https://api.library.cdisc.org/api/mdr/ct/packages/sdtmct-2024-01-01/codelists/C123",
        headers=api._headers,
    )

    # Verify response processing
    assert result["conceptId"] == "C123"
    assert "_links" not in result
    assert result["source"]["effective_date"] == "2024-01-01"
    assert result["source"]["package"] == "sdtmct"


@patch("requests.get")
def test_package_code_list_failure(mock_get, api):
    """Test package_code_list method with failed response"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    result = api.package_code_list("sdtmct", "2024-01-01", "INVALID")
    assert result is None


@patch("requests.get")
def test_refresh_success(mock_get, api):
    """Test the refresh method with successful response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "_links": {
            "packages": [
                {
                    "href": "/mdr/ct/packages/sdtmct-2024-01-01",
                    "title": "SDTM Controlled Terminology Effective 2024-01-01",
                },
                {
                    "href": "/mdr/ct/packages/ddfct-2024-01-01",
                    "title": "Define-XML Controlled Terminology Effective 2024-01-01",
                },
            ]
        }
    }
    mock_get.return_value = mock_response

    api.refresh()

    # Verify request was made correctly
    mock_get.assert_called_once_with(
        "https://api.library.cdisc.org/api/mdr/ct/packages",
        headers=api._headers,
    )

    # Verify packages were parsed correctly
    assert "sdtmct" in api._packages
    assert "ddfct" in api._packages
    assert api._packages["sdtmct"][0]["effective"] == "2024-01-01"
    assert api._packages["ddfct"][0]["effective"] == "2024-01-01"


@patch("requests.get")
def test_refresh_failure(mock_get, api):
    """Test refresh method with failed response"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_get.return_value = mock_response

    api.refresh()
    assert api._packages is None


def test_extract_ct_name():
    """Test _extract_ct_name method"""
    api = LibraryAPI([])

    # Valid URLs
    assert api._extract_ct_name("/mdr/ct/packages/sdtmct-2024-01-01") == "sdtmct"
    assert api._extract_ct_name("/mdr/ct/packages/ddfct-2023-12-15") == "ddfct"

    # Invalid URLs
    assert api._extract_ct_name("/invalid/url") is None
    assert api._extract_ct_name("") is None
    assert api._extract_ct_name("/mdr/ct/packages/invalid-format") is None


def test_extract_effective_date():
    """Test _extract_effective_date method"""
    api = LibraryAPI([])

    # Valid titles
    assert (
        api._extract_effective_date("SDTM Controlled Terminology Effective 2024-01-01")
        == "2024-01-01"
    )
    assert (
        api._extract_effective_date(
            "Define-XML Controlled Terminology Effective 2023-12-15"
        )
        == "2023-12-15"
    )

    # Invalid titles
    assert api._extract_effective_date("Invalid title") is None
    assert api._extract_effective_date("") is None
    assert api._extract_effective_date("No date here") is None


def test_package_version():
    """Test _package_version method"""
    api = LibraryAPI([])

    # Test with valid packages
    api._packages = {
        "sdtmct": [
            {"effective": "2023-01-01", "url": "/test1"},
            {"effective": "2024-01-01", "url": "/test2"},
        ]
    }

    # Should return the last (most recent) version
    assert api._package_version("sdtmct") == "2024-01-01"

    # Test with non-existent package
    assert api._package_version("nonexistent") is None

    # Test with None packages
    api._packages = None
    assert api._package_version("sdtmct") is None

    # Test with empty package list
    api._packages = {"sdtmct": []}
    assert api._package_version("sdtmct") is None


@patch("requests.get")
def test_get_packages_success(mock_get, api):
    """Test _get_packages method with successful response"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "_links": {
            "packages": [
                {
                    "href": "/mdr/ct/packages/sdtmct-2024-01-01",
                    "title": "SDTM Controlled Terminology Effective 2024-01-01",
                },
                {
                    "href": "/mdr/ct/packages/sdtmct-2023-01-01",
                    "title": "SDTM Controlled Terminology Effective 2023-01-01",
                },
                {
                    "href": "/invalid/format",  # This should be ignored
                    "title": "Invalid Title",
                },
            ]
        }
    }
    mock_get.return_value = mock_response

    result = api._get_packages()

    # Verify only valid packages are included
    assert "sdtmct" in result
    assert len(result["sdtmct"]) == 2
    assert result["sdtmct"][0]["effective"] == "2024-01-01"
    assert result["sdtmct"][1]["effective"] == "2023-01-01"


@patch("requests.get")
def test_get_packages_failure(mock_get, api):
    """Test _get_packages method with failed response"""
    mock_response = Mock()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    result = api._get_packages()
    assert result is None
