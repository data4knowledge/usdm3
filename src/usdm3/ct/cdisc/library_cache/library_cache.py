import os
import yaml
import pathlib


class LibraryCache:
    def __init__(self, file_path: str = "library_cache.yaml"):
        self._file_path = file_path

    def exists(self) -> bool:
        return self._file_exists()

    def save(self, data: dict) -> None:
        try:
            if not self._file_exists():
                with open(self._filepath(), "w") as f:
                    yaml.dump(data, f, indent=2, sort_keys=True)
        except Exception as e:
            raise Exception(f"failed to save CDSIC CT file, {str(e)}")

    def read(self) -> dict:
        try:
            if self._file_exists():
                with open(self._filepath()) as f:
                    return yaml.safe_load(f)
            else:
                raise Exception("Failed to read CDSIC CT file, does not exist")
        except Exception as e:
            raise Exception(f"failed to read CDSIC CT file, {str(e)}")

    def delete(self) -> None:
        try:
            os.remove(self._filepath())
        except Exception as e:
            raise Exception(f"failed to delete CDSIC CT file, {str(e)}")

    def _file_exists(self) -> bool:
        return os.path.isfile(self._filepath())

    def _filepath(self) -> str:
        root = pathlib.Path(__file__).parent.resolve()
        return os.path.join(root, self._file_path)
