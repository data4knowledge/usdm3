import pytest
from unittest.mock import Mock, patch
from usdm3.ct.cdisc.library_api import LibraryAPI


@pytest.fixture
def api():
    """Fixture to create a LibraryAPI instance"""
    return LibraryAPI()


@pytest.fixture
def mock_response():
    """Fixture to create a mock response"""
    mock = Mock()
    mock.json.return_value = {"data": "test"}
    mock.status_code = 200
    return mock


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
def test_code_list(mock_get, api, mock_response):
    """Test the code_list method"""
    mock_response.json.return_value = {"conceptId": "C123", "terms": [{"term": "test"}]}
    mock_get.return_value = mock_response
    api._packages = {"sdtmct": [{"effective": "2024-01-01"}]}

    result = api.code_list("C123")

    # Verify request was made correctly
    mock_get.assert_called_once_with(
        "https://api.library.cdisc.org/api/mdr/ct/packages/sdtmct-2024-01-01/codelists/C123",
        headers=api._headers,
    )

    # Verify response processing
    assert result["conceptId"] == "C123"
    assert result["terms"] == [{"term": "test"}]


@patch("requests.get")
def test_code_list_error(mock_get, api):
    """Test code_list method error handling"""
    mock_response = Mock()
    mock_response.status_code = 404
    mock_response.text = "Not Found"
    mock_get.return_value = mock_response

    api._packages = {"sdtmct": [{"effective": "2024-01-01"}]}
    with pytest.raises(LibraryAPI.APIError) as exc_info:
        api.code_list("invalid-id")
    assert "failed to obtain code list from library for invalid-id" in str(exc_info.value)


@patch("requests.get")
def test_refresh(mock_get, api):
    """Test the refresh method"""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"_links": {"packages": []}}
    mock_get.return_value = mock_response

    api.refresh()

    # Verify request was made correctly
    mock_get.assert_called_once_with(
        "https://api.library.cdisc.org/api/mdr/ct/packages",
        headers={"Content-Type": "application/json", "api-key": "api_key"},
    )


@patch("requests.get")
def test_packages_malformed_response(mock_get, api):
    """Test packages method with malformed response"""
    mock_response = Mock()
    mock_response.status_code = 401
    mock_response.text = "Unauthorized"
    mock_get.return_value = mock_response

    with pytest.raises(Exception) as exc_info:
        list(api.refresh())
    assert "failed to get packages" in str(exc_info.value)
