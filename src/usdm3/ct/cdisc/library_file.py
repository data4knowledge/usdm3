import os
import yaml


class LibraryFile:
    def __init__(self, path: str, filename: str):
        self._path = path
        self._filename = filename

    def save(self, data: dict) -> None:
        try:
            if not self._file_exist():
                with open(self._filepath(), "w") as f:
                    yaml.dump(data, f, indent=2, sort_keys=True)
        except Exception as e:
            raise Exception(f"failed to save CDSIC CT file, {str(e)}")

    def read(self) -> dict:
        try:
            if self._file_exist():
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

    def _file_exist(self) -> bool:
        return os.path.isfile(self._filepath())

    def _filepath(self) -> str:
        return os.path.join(self._path, self._filename)
