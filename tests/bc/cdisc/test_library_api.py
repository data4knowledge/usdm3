import pytest
import os
from unittest.mock import Mock, patch, MagicMock
from usdm3.bc.cdisc.library_api import LibraryAPI
from usdm3.ct.cdisc.library import Library as CtLibrary


class TestLibraryAPI:
    
    def setup_method(self):
        """Set up test fixtures before each test method."""
        # Mock CT library
        self.mock_ct_library = Mock(spec=CtLibrary)
        self.mock_ct_library.system = "CDISC CT"
        self.mock_ct_library.version = "2023-12-15"
        
        # Mock environment variable for API key
        with patch.dict(os.environ, {'CDISC_API_KEY': 'test_api_key'}):
            self.api = LibraryAPI(self.mock_ct_library)
    
    def test_initialization_with_api_key(self):
        """Test LibraryAPI initialization with valid API key."""
        with patch.dict(os.environ, {'CDISC_API_KEY': 'test_key'}):
            api = LibraryAPI(self.mock_ct_library)
            
            assert api._ct_library == self.mock_ct_library
            assert api._api_key == 'test_key'
            assert api._headers == {"Content-Type": "application/json", "api-key": "test_key"}
            assert api._package_metadata == {}
            assert api._package_items == {}
            assert api._bc_responses == {}
            assert api._bcs_raw == {}
            assert api._map == {}
    
    def test_initialization_without_api_key(self):
        """Test LibraryAPI initialization without API key."""
        with patch.dict(os.environ, {}, clear=True):
            api = LibraryAPI(self.mock_ct_library)
            
            assert api._api_key is None
            assert api.errors.error_count() > 0
    
    def test_errors_property(self):
        """Test errors property."""
        assert self.api.errors is not None
        assert hasattr(self.api.errors, 'error_count')
    
    def test_valid_property(self):
        """Test valid property."""
        # Should return the error count (0 means valid)
        result = self.api.valid
        assert isinstance(result, int)
    
    def test_url_method(self):
        """Test _url method."""
        relative_url = "/test/path"
        expected = f"{LibraryAPI.API_ROOT}/test/path"
        result = self.api._url(relative_url)
        assert result == expected
    
    def test_code_object(self):
        """Test _code_object method."""
        code = "C12345"
        decode = "Test Code"
        
        result = self.api._code_object(code, decode)
        
        expected = {
            "id": "tbd",
            "code": code,
            "codeSystem": self.mock_ct_library.system,
            "codeSystemVersion": self.mock_ct_library.version,
            "decode": decode,
            "instanceType": "Code"
        }
        assert result == expected
    
    def test_alias_code_object_with_standard_code(self):
        """Test _alias_code_object method with standard code."""
        standard_code = {"code": "C12345", "decode": "Test"}
        aliases = ["alias1", "alias2"]
        
        result = self.api._alias_code_object(standard_code, aliases)
        
        expected = {
            "id": "tbd",
            "standardCode": standard_code,
            "standardCodeAliases": aliases,
            "instanceType": "AliasCode"
        }
        assert result == expected
    
    def test_alias_code_object_without_standard_code(self):
        """Test _alias_code_object method without standard code."""
        result = self.api._alias_code_object(None, [])
        assert result is None
    
    def test_response_code_object(self):
        """Test _response_code_object method."""
        code = {"code": "C12345", "decode": "Test Code"}
        
        result = self.api._response_code_object(code)
        
        expected = {
            "id": "tbd",
            "name": "RC_C12345",
            "label": "",
            "isEnabled": True,
            "code": code,
            "instanceType": "ResponseCode"
        }
        assert result == expected
    
    def test_biomedical_concept_property_object(self):
        """Test _biomedical_concept_property_object method."""
        name = "TEST_PROPERTY"
        label = "Test Property"
        datatype = "text"
        responses = [{"code": "C12345"}]
        code = {"code": "C67890", "decode": "Property Code"}
        
        result = self.api._biomedical_concept_property_object(name, label, datatype, responses, code)
        
        assert result["name"] == name
        assert result["label"] == label
        assert result["datatype"] == datatype
        assert result["responseCodes"] == responses
        assert result["instanceType"] == "BiomedicalConceptProperty"
        assert result["isRequired"] is True
        assert result["isEnabled"] is True
    
    def test_biomedical_concept_object(self):
        """Test _biomedical_concept_object method."""
        name = "TEST_BC"
        label = "Test Biomedical Concept"
        synonyms = ["synonym1", "synonym2"]
        reference = "http://test.com/bc/123"
        code = {"code": "C12345", "decode": "BC Code"}
        
        result = self.api._biomedical_concept_object(name, label, synonyms, reference, code)
        
        assert result["name"] == name
        assert result["label"] == label
        assert result["synonyms"] == synonyms
        assert result["reference"] == reference
        assert result["properties"] == []
        assert result["instanceType"] == "BiomedicalConcept"
    
    def test_process_sdtm_bc_excluded(self):
        """Test _process_sdtm_bc method with excluded BC."""
        excluded_name = "Exclusion Criteria 01"
        result = self.api._process_sdtm_bc(excluded_name)
        assert result is False
    
    def test_process_sdtm_bc_included(self):
        """Test _process_sdtm_bc method with included BC."""
        included_name = "Valid BC Name"
        result = self.api._process_sdtm_bc(included_name)
        assert result is True
    
    def test_process_generic_bc_included(self):
        """Test _process_genric_bc method with included BC."""
        included_names = ["SUBJECT AGE", "RACE", "SEX"]
        for name in included_names:
            result = self.api._process_genric_bc(name)
            assert result is True
    
    def test_process_generic_bc_excluded(self):
        """Test _process_genric_bc method with excluded BC."""
        excluded_name = "OTHER BC"
        result = self.api._process_genric_bc(excluded_name)
        assert result is False
    
    def test_process_property_excluded(self):
        """Test _process_property method with excluded properties."""
        excluded_properties = ["XXTEST", "XXSTRESN", "XXSTRESU", "EPOCH"]
        for prop in excluded_properties:
            result = self.api._process_property(prop)
            assert result is False
    
    def test_process_property_included(self):
        """Test _process_property method with included properties."""
        included_property = "XXVALID"
        result = self.api._process_property(included_property)
        assert result is True
    
    def test_get_role_variable_found(self):
        """Test _get_role_variable method when role variable is found."""
        data = {
            "variables": [
                {"role": "Identifier", "name": "ID"},
                {"role": "Topic", "name": "TOPIC_VAR"},
                {"role": "Qualifier", "name": "QUAL"}
            ]
        }
        
        result = self.api._get_role_variable(data)
        assert result == {"role": "Topic", "name": "TOPIC_VAR"}
    
    def test_get_role_variable_not_found(self):
        """Test _get_role_variable method when role variable is not found."""
        data = {
            "variables": [
                {"role": "Identifier", "name": "ID"},
                {"role": "Qualifier", "name": "QUAL"}
            ]
        }
        
        result = self.api._get_role_variable(data)
        assert result is None
    
    def test_get_role_variable_exception(self):
        """Test _get_role_variable method with invalid data."""
        data = {"invalid": "data"}
        
        result = self.api._get_role_variable(data)
        assert result is None
    
    def test_get_dec_match_found(self):
        """Test _get_dec_match method when match is found."""
        data = {
            "dataElementConcepts": [
                {"conceptId": "C12345", "name": "Concept1"},
                {"conceptId": "C67890", "name": "Concept2"}
            ]
        }
        
        result = self.api._get_dec_match(data, "C67890")
        assert result == {"conceptId": "C67890", "name": "Concept2"}
    
    def test_get_dec_match_not_found(self):
        """Test _get_dec_match method when match is not found."""
        data = {
            "dataElementConcepts": [
                {"conceptId": "C12345", "name": "Concept1"}
            ]
        }
        
        result = self.api._get_dec_match(data, "C99999")
        assert result is None
    
    def test_get_dec_match_exception(self):
        """Test _get_dec_match method with invalid data."""
        data = {"invalid": "data"}
        
        result = self.api._get_dec_match(data, "C12345")
        assert result is None
    
    @patch('requests.get')
    def test_get_from_url_success(self, mock_get):
        """Test _get_from_url method with successful response."""
        mock_response = Mock()
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        result = self.api._get_from_url("/test/url")
        
        assert result == {"test": "data"}
        mock_get.assert_called_once_with(f"{LibraryAPI.API_ROOT}/test/url", headers=self.api._headers)
    
    @patch('requests.get')
    def test_get_package_metadata_success(self, mock_get):
        """Test _get_package_metadata method with successful response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "_links": {
                "packages": [{"href": "/package1"}, {"href": "/package2"}]
            }
        }
        mock_get.return_value = mock_response
        
        self.api._get_package_metadata()
        
        assert "generic" in self.api._package_metadata
        assert "sdtm" in self.api._package_metadata
        assert len(self.api._package_metadata["generic"]) == 2
        assert len(self.api._package_metadata["sdtm"]) == 2
    
    @patch('requests.get')
    def test_get_package_metadata_exception(self, mock_get):
        """Test _get_package_metadata method with exception."""
        mock_get.side_effect = Exception("Network error")
        
        self.api._get_package_metadata()
        
        # Should handle exception gracefully
        assert self.api.errors.error_count() > 0
    
    @patch('requests.get')
    def test_get_package_success(self, mock_get):
        """Test _get_package method with successful response."""
        mock_response = Mock()
        mock_response.json.return_value = {
            "_links": {
                "biomedicalConcepts": [
                    {"title": "Test BC", "href": "/bc/test"}
                ]
            }
        }
        mock_get.return_value = mock_response
        
        # Initialize the package_items structure
        self.api._package_items["generic"] = {}
        
        package = {"href": "/package/test"}
        self.api._get_package(package, "generic")
        
        assert "TEST BC" in self.api._package_items["generic"]
    
    @patch('requests.get')
    def test_get_package_exception(self, mock_get):
        """Test _get_package method with exception."""
        mock_get.side_effect = Exception("Network error")
        
        package = {"href": "/package/test"}
        result = self.api._get_package(package, "generic")
        
        assert result == {}
        assert self.api.errors.error_count() > 0
    
    @patch('requests.get')
    def test_get_from_url_all_success(self, mock_get):
        """Test _get_from_url_all method with successful response."""
        # Mock SDTM response
        sdtm_response = {
            "shortName": "TEST_BC",
            "_links": {
                "parentBiomedicalConcept": {"href": "/generic/test"}
            }
        }
        # Mock generic response
        generic_response = {"shortName": "Generic Test BC"}
        
        mock_get.side_effect = [
            Mock(json=lambda: sdtm_response),
            Mock(json=lambda: generic_response)
        ]
        
        details = {"href": "/sdtm/test"}
        sdtm, generic = self.api._get_from_url_all("TEST_BC", details)
        
        assert sdtm == sdtm_response
        assert generic == generic_response
    
    @patch('requests.get')
    def test_get_from_url_all_exception(self, mock_get):
        """Test _get_from_url_all method with exception."""
        mock_get.side_effect = Exception("Network error")
        
        details = {"href": "/sdtm/test"}
        sdtm, generic = self.api._get_from_url_all("TEST_BC", details)
        
        assert sdtm is None
        assert generic is None
        assert self.api.errors.error_count() > 0
    
    def test_generic_bc_as_usdm(self):
        """Test _generic_bc_as_usdm method."""
        api_bc = {
            "conceptId": "C12345",
            "shortName": "TEST_BC",
            "synonyms": ["synonym1", "synonym2"],
            "_links": {"self": {"href": "/bc/test"}}
        }
        
        result = self.api._generic_bc_as_usdm(api_bc)
        
        assert result["name"] == "TEST_BC"
        assert result["label"] == "TEST_BC"
        assert result["synonyms"] == ["synonym1", "synonym2"]
        assert result["reference"] == "/bc/test"
        assert result["instanceType"] == "BiomedicalConcept"
    
    def test_generic_bc_property_as_usdm_without_examples(self):
        """Test _generic_bc_property_as_usdm method without examples."""
        property_data = {
            "conceptId": "C67890",
            "shortName": "TEST_PROP",
            "dataType": "text"
        }
        
        result = self.api._generic_bc_property_as_usdm(property_data)
        
        assert result["name"] == "TEST_PROP"
        assert result["label"] == "TEST_PROP"
        assert result["datatype"] == "text"
        assert result["responseCodes"] == []
        assert result["instanceType"] == "BiomedicalConceptProperty"
    
    def test_generic_bc_property_as_usdm_with_examples(self):
        """Test _generic_bc_property_as_usdm method with examples."""
        property_data = {
            "conceptId": "C67890",
            "shortName": "TEST_PROP",
            "dataType": "text",
            "exampleSet": ["example1", "example2"]
        }
        
        # Mock CT library to return None for examples (no matching terms)
        self.mock_ct_library.preferred_term.return_value = None
        
        result = self.api._generic_bc_property_as_usdm(property_data)
        
        assert result["name"] == "TEST_PROP"
        assert result["responseCodes"] == []
    
    @patch('requests.get')
    def test_refresh_method(self, mock_get):
        """Test refresh method."""
        # Mock responses for package metadata
        package_response = Mock()
        package_response.json.return_value = {
            "_links": {"packages": []}
        }
        
        # Mock responses for package items
        items_response = Mock()
        items_response.json.return_value = {
            "_links": {"biomedicalConcepts": [], "datasetSpecializations": []}
        }
        
        mock_get.return_value = package_response
        
        # Mock the internal methods to avoid complex setup
        with patch.object(self.api, '_get_sdtm_bcs') as mock_sdtm, \
             patch.object(self.api, '_get_generic_bcs') as mock_generic:
            
            result = self.api.refresh()
            
            mock_sdtm.assert_called_once()
            mock_generic.assert_called_once()
            assert result == self.api._bcs_raw
    
    def test_sdtm_bc_as_usdm_with_role_variable_and_assigned_term(self):
        """Test _sdtm_bc_as_usdm method with role variable and assigned term."""
        sdtm = {
            "shortName": "TEST_BC",
            "_links": {"self": {"href": "/sdtm/test"}},
            "variables": [{
                "role": "Topic",
                "assignedTerm": {
                    "conceptId": "C12345",
                    "value": "Test Value"
                }
            }]
        }
        generic = {
            "conceptId": "C67890",
            "shortName": "Generic BC",
            "synonyms": ["syn1", "syn2"]
        }
        
        result = self.api._sdtm_bc_as_usdm(sdtm, generic)
        
        assert result["name"] == "TEST_BC"
        assert result["instanceType"] == "BiomedicalConcept"
        assert "Generic BC" in result["synonyms"]
    
    def test_sdtm_bc_as_usdm_excluded_bc(self):
        """Test _sdtm_bc_as_usdm method with excluded BC."""
        sdtm = {"shortName": "Exclusion Criteria 01"}
        generic = {"shortName": "Generic BC"}
        
        result = self.api._sdtm_bc_as_usdm(sdtm, generic)
        assert result is None
    
    def test_sdtm_bc_as_usdm_exception(self):
        """Test _sdtm_bc_as_usdm method with exception."""
        sdtm = {"shortName": "TEST_BC"}  # Missing required fields
        generic = None  # This will cause an exception
        
        result = self.api._sdtm_bc_as_usdm(sdtm, generic)
        assert result is None
        assert self.api.errors.error_count() > 0
    
    def test_sdtm_bc_property_as_usdm_with_dec_id(self):
        """Test _sdtm_bc_property_as_usdm method with dataElementConceptId."""
        sdtm_property = {
            "name": "TESTVAL",
            "dataElementConceptId": "C12345",
            "dataType": "text"
        }
        generic = {
            "dataElementConcepts": [{
                "conceptId": "C12345",
                "shortName": "Test Concept"
            }]
        }
        
        result = self.api._sdtm_bc_property_as_usdm(sdtm_property, generic)
        
        assert result["name"] == "TESTVAL"
        assert result["datatype"] == "text"
        assert result["instanceType"] == "BiomedicalConceptProperty"
    
    def test_sdtm_bc_property_as_usdm_excluded_property(self):
        """Test _sdtm_bc_property_as_usdm method with excluded property."""
        sdtm_property = {"name": "XXTEST"}  # Excluded property
        generic = {}
        
        result = self.api._sdtm_bc_property_as_usdm(sdtm_property, generic)
        assert result is None
    
    def test_sdtm_bc_property_as_usdm_with_value_list(self):
        """Test _sdtm_bc_property_as_usdm method with value list."""
        sdtm_property = {
            "name": "TESTVAL",
            "dataType": "text",
            "valueList": ["VALUE1", "VALUE2"],
            "codelist": {"conceptId": "CL123"}
        }
        generic = {}
        
        # Mock CT library responses
        self.mock_ct_library.preferred_term.side_effect = [
            {"conceptId": "C111", "preferredTerm": "Value 1"},
            None  # Second call returns None
        ]
        self.mock_ct_library.submission.return_value = {
            "conceptId": "C222", "preferredTerm": "Value 2"
        }
        
        result = self.api._sdtm_bc_property_as_usdm(sdtm_property, generic)
        
        assert result["name"] == "TESTVAL"
        assert len(result["responseCodes"]) == 2
    
    def test_sdtm_bc_property_as_usdm_exception(self):
        """Test _sdtm_bc_property_as_usdm method with exception."""
        sdtm_property = {"name": "XXTEST"}  # Excluded property that should return None
        generic = {}
        
        result = self.api._sdtm_bc_property_as_usdm(sdtm_property, generic)
        assert result is None
