from usdm3.file_cache.file_cache import FileCache


class LibraryCache(FileCache):
    def __init__(self, filepath: str, filename: str = "library_cache.yaml"):
        super().__init__(filepath, filename)

