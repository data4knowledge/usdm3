import os
from pathlib import Path
#from usdm3.bc.cdisc.library import Library
from usdm3.bc.cdisc.library_api import LibraryAPI
from usdm3.file_cache.file_cache import FileCache

from dotenv import load_dotenv

if __name__ == "__main__":
    root = os.path.join(Path(__file__).parent.resolve(), "src/usdm3/bc/cdisc")
    load_dotenv(".development_env")
    api = LibraryAPI("cdisc.org", "2025-03-01")
    bc = api.refresh()
    cache = FileCache("src/usdm3/bc/cdisc", "bc_cache.yaml")
    cache.save(bc)
    print(f"BC Library Valid: {api.valid}")
    print(f"BC Library Errors: {api.errors.dump()}")
    # library = Library(root)
    # library.load()
