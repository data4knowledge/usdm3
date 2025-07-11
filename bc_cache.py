import os
from pathlib import Path
from usdm3.ct.cdisc.library import Library as CtLibrary
from usdm3.bc.cdisc.library_api import LibraryAPI
from usdm3.file_cache.file_cache import FileCache

from dotenv import load_dotenv

if __name__ == "__main__":
    root = os.path.join(Path(__file__).parent.resolve(), "src/usdm3")
    print(f"ROOT CT: {root}")
    load_dotenv(".development_env")
    ct = CtLibrary(root)
    ct.load()
    api = LibraryAPI(ct)
    bc = api.refresh()
    cache = FileCache(root, "bc_cache.yaml")
    cache.save(bc)
    print(f"BC Library Valid: {api.valid}")
    print(f"BC Library Errors: {api.errors.dump()}")
