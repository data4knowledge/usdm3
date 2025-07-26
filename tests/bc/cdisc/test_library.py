import os
import tempfile
import shutil
from unittest.mock import Mock, patch
from usdm3.bc.cdisc.library import Library
from usdm3.ct.cdisc.library import Library as CtLibrary


class TestLibrary:
    def setup_method(self):
        """Set up test fixtures before each test method."""
        self.temp_dir = tempfile.mkdtemp()
        self.ct_library_mock = Mock(spec=CtLibrary)
        self.library = Library(self.temp_dir, self.ct_library_mock)

    def teardown_method(self):
        """Clean up after each test method."""
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_initialization(self):
        """Test Library initialization."""
        assert self.library.root_path == self.temp_dir
        assert (
            self.library._ct_library == CtLibrary
        )  # Note: this is the class, not instance
        assert self.library._bcs == {}
        assert self.library._bc_index == {}
        assert self.library.API_ROOT == "https://api.library.cdisc.org/api/cosmos/v2"
        assert self.library.BASE_PATH == "bc/cdisc"

    @patch("usdm3.bc.cdisc.library.LibraryCache")
    @patch("usdm3.bc.cdisc.library.LibraryAPI")
    def test_load_from_cache(self, mock_api, mock_cache):
        """Test loading BCs from cache when cache exists."""
        # Setup mocks
        mock_cache_instance = Mock()
        mock_cache_instance.exists.return_value = True
        mock_cache_instance.read.return_value = {
            "TEST_BC": {"name": "Test BC", "synonyms": ["TEST", "test_bc"]}
        }
        mock_cache.return_value = mock_cache_instance

        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance

        # Replace the library's cache and api with mocks
        self.library._cache = mock_cache_instance
        self.library._api = mock_api_instance

        # Execute
        self.library.load()

        # Verify
        mock_cache_instance.exists.assert_called_once()
        mock_cache_instance.read.assert_called_once()
        mock_api_instance.refresh.assert_not_called()
        mock_cache_instance.save.assert_not_called()

        assert "TEST_BC" in self.library._bcs
        assert "TEST_BC" in self.library._bc_index
        assert "TEST" in self.library._bc_index
        assert "TEST_BC" in self.library._bc_index

    @patch("usdm3.bc.cdisc.library.LibraryCache")
    @patch("usdm3.bc.cdisc.library.LibraryAPI")
    def test_load_from_api(self, mock_api, mock_cache):
        """Test loading BCs from API when cache doesn't exist."""
        # Setup mocks
        mock_cache_instance = Mock()
        mock_cache_instance.exists.return_value = False
        mock_cache.return_value = mock_cache_instance

        mock_api_instance = Mock()
        mock_api_instance.refresh.return_value = {
            "API_BC": {"name": "API BC", "synonyms": ["API", "api_bc"]}
        }
        mock_api.return_value = mock_api_instance

        # Replace the library's cache and api with mocks
        self.library._cache = mock_cache_instance
        self.library._api = mock_api_instance

        # Execute
        self.library.load()

        # Verify
        mock_cache_instance.exists.assert_called_once()
        mock_api_instance.refresh.assert_called_once()
        mock_cache_instance.save.assert_called_once()
        mock_cache_instance.read.assert_not_called()

        assert "API_BC" in self.library._bcs
        assert "API_BC" in self.library._bc_index
        assert "API" in self.library._bc_index
        assert "API_BC" in self.library._bc_index

    def test_exists_true(self):
        """Test exists method returns True for existing BC."""
        self.library._bc_index = {"TEST_BC": "TEST_BC", "TEST": "TEST_BC"}

        assert self.library.exists("test_bc") is True
        assert self.library.exists("TEST") is True
        assert self.library.exists("TEST_BC") is True

    def test_exists_false(self):
        """Test exists method returns False for non-existing BC."""
        self.library._bc_index = {"TEST_BC": "TEST_BC"}

        assert self.library.exists("NONEXISTENT") is False
        assert self.library.exists("missing") is False

    def test_catalogue(self):
        """Test catalogue method returns list of BC names."""
        self.library._bcs = {
            "BC1": {"name": "BC1"},
            "BC2": {"name": "BC2"},
            "BC3": {"name": "BC3"},
        }

        catalogue = self.library.catalogue()
        assert isinstance(catalogue, list)
        assert len(catalogue) == 3
        assert "BC1" in catalogue
        assert "BC2" in catalogue
        assert "BC3" in catalogue

    def test_catalogue_empty(self):
        """Test catalogue method with empty BCs."""
        catalogue = self.library.catalogue()
        assert isinstance(catalogue, list)
        assert len(catalogue) == 0

    def test_usdm_existing_bc(self):
        """Test usdm method returns BC data for existing BC."""
        test_bc_data = {"name": "Test BC", "synonyms": ["TEST"], "properties": []}
        self.library._bcs = {"TEST_BC": test_bc_data}
        self.library._bc_index = {"TEST": "TEST_BC"}

        result = self.library.usdm("test")
        assert result == test_bc_data

    def test_usdm_nonexistent_bc(self):
        """Test usdm method returns None for non-existing BC."""
        self.library._bc_index = {}

        result = self.library.usdm("nonexistent")
        assert result is None

    def test_load_bcs(self):
        """Test _load_bcs method."""
        mock_cache = Mock()
        test_data = {"BC1": {"name": "BC1"}}
        mock_cache.read.return_value = test_data
        self.library._cache = mock_cache

        self.library._load_bcs()

        assert self.library._bcs == test_data
        mock_cache.read.assert_called_once()

    def test_get_bcs(self):
        """Test _get_bcs method."""
        mock_api = Mock()
        test_data = {"BC1": {"name": "BC1"}}
        mock_api.refresh.return_value = test_data
        self.library._api = mock_api

        self.library._get_bcs()

        assert self.library._bcs == test_data
        mock_api.refresh.assert_called_once()

    def test_create_bc_index(self):
        """Test _create_bc_index method."""
        self.library._bcs = {
            "BC1": {"name": "BC1", "synonyms": ["SYNONYM1", "SYNONYM2"]},
            "BC2": {"name": "BC2", "synonyms": ["SYN3"]},
        }

        self.library._create_bc_index()

        expected_index = {
            "BC1": "BC1",
            "SYNONYM1": "BC1",
            "SYNONYM2": "BC1",
            "BC2": "BC2",
            "SYN3": "BC2",
        }

        assert self.library._bc_index == expected_index

    def test_create_bc_index_empty_synonyms(self):
        """Test _create_bc_index method with empty synonyms."""
        self.library._bcs = {"BC1": {"name": "BC1", "synonyms": []}}

        self.library._create_bc_index()

        expected_index = {"BC1": "BC1"}
        assert self.library._bc_index == expected_index

    def test_get_bc_data(self):
        """Test _get_bc_data method."""
        test_data = {"name": "Test BC", "properties": []}
        self.library._bcs = {"TEST_BC": test_data}
        self.library._bc_index = {"TEST": "TEST_BC"}

        result = self.library._get_bc_data("test")
        assert result == test_data

    def test_get_bc_data_case_insensitive(self):
        """Test _get_bc_data method is case insensitive."""
        test_data = {"name": "Test BC", "properties": []}
        self.library._bcs = {"TEST_BC": test_data}
        self.library._bc_index = {"TEST": "TEST_BC"}

        result = self.library._get_bc_data("TeSt")
        assert result == test_data
