from usdm3.ct.cdisc.library import Library
from dotenv import load_dotenv

if __name__ == "__main__":
    load_dotenv(".development_env")
    library = Library()
    library.load()
