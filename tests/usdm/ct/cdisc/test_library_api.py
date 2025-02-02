from usdm3.ct.cdisc.library_api import LibraryAPI

def test_url():
    """Test the _url method of LibraryAPI"""
    api = LibraryAPI()
    
    # Test with simple relative URL
    assert api._url("/test") == "https://api.library.cdisc.org/api/test"
    
    # Test with empty relative URL
    assert api._url("") == "https://api.library.cdisc.org/api"
    
    # Test with complex relative URL
    assert api._url("/mdr/ct/packages/sdtmct-2024-01-01") == "https://api.library.cdisc.org/api/mdr/ct/packages/sdtmct-2024-01-01"
    
    # Test with relative URL that already has leading slash
    assert api._url("///test") == "https://api.library.cdisc.org/api///test"