import re
import requests
from d4k_ms_base.service_environment import ServiceEnvironment

class LibraryAPI:
    """
    CDISC Library API Client
    
    This class provides an interface to interact with the CDISC Library API,
    handling authentication, pagination, and data retrieval for controlled terminology.
    
    The API requires authentication via an API key which should be set in the
    environment variables as CDISC_API_KEY.
    
    Attributes:
        API_ROOT (str): Base URL for all CDISC Library API endpoints
    """

    API_ROOT = "https://api.library.cdisc.org/api"

    class APIError(Exception):
        """Custom exception for API-related errors"""
        pass

    def __init__(self) -> None:
        """
        Initialize the LibraryAPI client.
        
        Sets up the service environment and configures the default headers
        with the API key for authentication.
        
        Raises:
            APIError: If the CDISC_API_KEY environment variable is not set
        """
        self._packages = None
        self._se = ServiceEnvironment()
        print(f"ENVIRONMENT: {self._se.environment(), self._se.get('CDISC_API_KEY')}")
        self._headers = {
            "Content-Type": "application/json",
            "api-key": self._se.get("CDISC_API_KEY")
        }

    def refresh(self) -> None:
        """
        Refresh the packages cache.
        
        This method clears and reloads the packages cache, ensuring
        the latest data is available for subsequent requests.
        """
        self._packages = self._get_packages()

    def code_list(self, c_code: str) -> dict:
        """
        Retrieve a specific code list from the CDISC Library.
        
        Attempts to find the code list in each of the supported packages
        (ddfct, sdtmct, protocolct) using the most recent version.
        
        Args:
            c_code (str): The code list identifier to retrieve
            
        Returns:
            dict: The complete code list data including all terms
            
        Raises:
            APIError: If the API request fails
            ValueError: If the code list cannot be found in any package
        """
        use_list = ["ddfct", "sdtmct", "protocolct"]
        for package in use_list:
            try:
                version = self._packages[package][-1]["effective"]
            except Exception:
                version = None
            if version:
                package_full_name = f"{package}-{version}"
                api_url = self._url(
                    f"/mdr/ct/packages/{package_full_name}/codelists/{c_code}"
                )
                raw = requests.get(api_url, headers=self._headers)
                if raw.status_code == 200:
                    response = raw.json()
                    response.pop("_links", None)
                    return response
                else:
                    raise self.APIError(
                        f"failed to obtain code list from library for {c_code}, "
                        f"response: {raw.status_code} {raw.text}"
                    )
        raise ValueError(f"failed to obtain code list for {c_code}")

    def _get_packages(self) -> dict:
        """
        Retrieve all available packages from the CDISC Library.
        
        This method fetches the complete list of packages and organizes them
        by name and effective date.
        
        Returns:
            dict: A dictionary mapping package names to lists of version information
                 Each version contains 'effective' date and API 'url'
                 
        Raises:
            APIError: If the API request fails or returns invalid data
        """
        packages = {}
        api_url = self._url("/mdr/ct/packages")
        raw = requests.get(api_url, headers=self._headers)
        if raw.status_code == 200:
            response = raw.json()
            for item in response["_links"]["packages"]:
                name = self._extract_ct_name(item["href"])
                effective_date = self._extract_effective_date(item["title"])
                if name and effective_date:
                    if name not in packages:
                        packages[name] = []
                    packages[name].append({"effective": effective_date, "url": item["href"]})
            return packages
        else:
            raise self.APIError(
                f"Failed to get packages, response: {raw.status_code} {raw.text}"
            )

    def _extract_ct_name(self, url: str) -> str:
        """
        Extract the controlled terminology name from a package URL.
        
        Args:
            url (str): The package URL to parse
            
        Returns:
            str: The extracted CT name, or None if no match is found
            
        Example:
            URL: ".../sdtmct-2024-01-01" returns "sdtmct"
        """
        match = re.search(r"([a-zA-Z]+)-\d{4}-\d{2}-\d{2}$", url)
        if match:
            return match.group(1)
        return None

    def _extract_effective_date(self, title: str) -> str:
        """
        Extract the effective date from a package title.
        
        Args:
            title (str): The package title to parse
            
        Returns:
            str: The extracted date in YYYY-MM-DD format, or None if no match is found
            
        Example:
            Title: "Package Name Effective 2024-01-01" returns "2024-01-01"
        """
        match = re.search(r"Effective (\d{4}-\d{2}-\d{2})$", title)
        if match:
            return match.group(1)
        return None

    def _url(self, relative_url: str) -> str:
        """
        Construct a full API URL from a relative path.
        
        Args:
            relative_url (str): The relative path to append to the API root
            
        Returns:
            str: The complete API URL
            
        Example:
            relative_url: "/packages" returns "https://api.library.cdisc.org/api/packages"
        """
        return f"{self.__class__.API_ROOT}{relative_url}"
