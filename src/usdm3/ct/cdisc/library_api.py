import re
import requests
from d4k_ms_base.service_environment import ServiceEnvironment

class LibraryAPI:
    """
    CDISC Library API
    """

    API_ROOT = "https://api.library.cdisc.org/api"

    class APIError(Exception):
        pass

    def __init__(self) -> None:
        """
        Initialize the LibraryAPI
        """
        self._packages = None
        self._se = ServiceEnvironment()
        self._headers = {"Content-Type": "application/json", "api-key": self._se.get("CDISC_API_KEY")}

    def refresh(self) -> None:
        """
        Refresh the packages
        """
        self._packages = self._get_packages()

    def code_list(self, c_code) -> dict:
        """
        Get the code list from the library
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
                raw = requests.get(api_url, headers=self.__class__.HEADERS)
                if raw.status_code == 200:
                    response = raw.json()
                    response.pop("_links", None)
                    return response
                else:
                    raise self.APIError(f"Failed to obtain code list from library for {c_code}, response: {raw.status_code} {raw.text}")
        raise ValueError(f"Failed to obtain code list for {c_code}")

    def _get_packages(self) -> dict:
        """
        Get the packages from the library
        """
        packages = {}
        api_url = self._url("/mdr/ct/packages")
        raw = requests.get(api_url, headers=self.__class__.HEADERS)
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
            raise self.APIError(f"Failed to get packages, response: {raw.status_code} {raw.text}")

    def _extract_ct_name(self, url) -> str:
        """
        Extract the CT name from the URL
        """
        match = re.search(r"([a-zA-Z]+)-\d{4}-\d{2}-\d{2}$", url)
        if match:
            return match.group(1)
        return None

    def _extract_effective_date(self, title) -> str:
        """
        Extract the effective date from the title
        """
        match = re.search(r"Effective (\d{4}-\d{2}-\d{2})$", title)
        if match:
            return match.group(1)
        return None

    
    def _url(self, relative_url) -> str:
        """
        Get the full URL from the relative URL
        """
        return f"{self.__class__.API_ROOT}{relative_url}"
