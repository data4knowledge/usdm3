from usdm3.ct.cdisc.library_api import LibraryAPI
from usdm3.ct.cdisc.config.config import Config
from usdm3.ct.cdisc.missing.missing import Missing
from usdm3.ct.cdisc.library_file import LibraryFile

class Library:
    """
    A class to manage CDISC controlled terminology (CT) data.
    
    This class handles loading, caching, and accessing CDISC controlled terminology,
    including code lists and their associated terms. It can load data from a local
    cache file or fetch it from the CDISC API when needed.
    """
    
    def __init__(self, path: str, filename: str):
        """
        Initialize the Library with configuration and data structures.
        
        Args:
            path: Directory path where the cache file will be stored
            filename: Name of the cache file
        """
        self._config = Config()  # Configuration for required code lists and mappings
        self._missing = Missing()  # Handler for missing/additional code lists
        self._api = LibraryAPI()  # Interface to CDISC Library API
        self._file = LibraryFile(path, filename)  # Cache file handler
        
        # Data structures to store and index controlled terminology
        self._by_code_list = {}  # Maps concept IDs to complete code list data
        self._by_term = {}       # Maps term concept IDs to parent code list IDs
        self._by_submission = {} # Maps submission values to parent code list IDs
        self._by_pt = {}        # Maps preferred terms to parent code list IDs

    def load(self) -> None:
        """
        Load controlled terminology data from cache or API.
        
        If a cache file exists, loads from it. Otherwise, fetches from the API
        and saves to cache. Also adds any missing terminology after loading.
        """
        if self._file.file_exist():
            self._load_ct()  # Load from cache file
        else:
            self._api.refresh()  # Ensure API connection is fresh
            self._get_ct()      # Fetch from API
            self._file.save(self._by_code_list)  # Cache the results
        self._add_missing_ct()  # Add any additional required terminology

    def refresh(self) -> None:
        """Refresh the API connection."""
        self._api.refresh()

    def klass_and_attribute(self, klass, attribute) -> dict:
        """
        Retrieve code list data for a given class and attribute combination.
        
        Args:
            klass: The class name to look up
            attribute: The attribute name within the class
        
        Returns:
            dict: Code list data if found, None otherwise
        """
        try:
            concept_id = self._config.klass_and_attribute(klass, attribute)
            return self._by_code_list[concept_id]
        except Exception as e:
            return None

    def _get_ct(self) -> None:
        """
        Fetch controlled terminology from the CDISC API.
        
        Retrieves all required code lists and indexes their terms for quick lookup.
        """
        for item in self._config.required_code_lists():
            response = self._api.code_list(item)
            self._by_code_list[response["conceptId"]] = response
            for item in response["terms"]:
                # Index each term by its various identifiers
                self._check_in_and_add(
                    self._by_term, item["conceptId"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_pt, item["preferredTerm"], response["conceptId"]
                )

    def _load_ct(self) -> None:
        """
        Load controlled terminology from the cache file.
        
        Reads the cached data and rebuilds the term indexes.
        """
        self._by_code_list = self._file.read()
        for c_code, entry in self._by_code_list.items():
            for item in entry["terms"]:
                # Rebuild indexes from cached data
                self._check_in_and_add(self._by_term, item["conceptId"], c_code)
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], c_code
                )
                self._check_in_and_add(self._by_pt, item["preferredTerm"], c_code)

    def _add_missing_ct(self) -> None:
        """
        Add any missing controlled terminology from local configuration.
        
        This allows for custom or additional terminology not available in the CDISC API.
        """
        for response in self._missing.code_lists():
            self._by_code_list[response["conceptId"]] = response
            for item in response["terms"]:
                # Index the additional terms
                self._check_in_and_add(
                    self._by_term, item["conceptId"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_submission, item["submissionValue"], response["conceptId"]
                )
                self._check_in_and_add(
                    self._by_pt, item["preferredTerm"], response["conceptId"]
                )

    def _check_in_and_add(self, collection: dict, id: str, item: str) -> None:
        """
        Helper method to add items to a collection with duplicate checking.
        
        Args:
            collection: Dictionary to add to
            id: Key to check/add
            item: Value to append to the list at the key
        """
        if not id in collection:
            collection[id] = []
        collection[id].append(item)
