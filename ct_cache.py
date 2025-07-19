import os
from pathlib import Path
from usdm3.ct.cdisc.library import Library
from dotenv import load_dotenv

if __name__ == "__main__":
    root = os.path.join(Path(__file__).parent.resolve(), "src/usdm3")
    load_dotenv(".development_env")
    library = Library(root, Library.USDM)
    library._cache.delete()
    library.load()
    library = Library(root, Library.ALL)
    library._cache.delete()
    library.load()
