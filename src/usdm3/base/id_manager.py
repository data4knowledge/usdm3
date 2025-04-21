class IdManager:

    DELIMITER = "_"

    def __init__(self, classes: list[str]):
        self._classes = classes
        self._id_index = {}
        self.clear()

    def clear(self) -> None:
        for klass in self._classes:
            name = klass if isinstance(klass, str) else klass.__name__
            self._id_index[name] = 0

    def build_id(self, klass) -> str:
        klass_name = klass if isinstance(klass, str) else str(klass.__name__)
        self._id_index[klass_name] += 1
        return f"{klass_name}{self.DELIMITER}{self._id_index[klass_name]}"

    def check_id(self, id: str) -> bool:
        if self.DELIMITER in id:
            parts = id.split(self.DELIMITER)
            if len(parts) == 2:
                klass = parts[0]
                value = parts[1]
                if klass in self._classes:
                    if value.isdigit():
                        if int(value) > self._id_index[klass]:
                            self._id_index[klass] = int(value)
                            return True
        return False