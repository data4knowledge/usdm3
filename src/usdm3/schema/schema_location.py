from d4k_sel import ErrorLocation

class SchemaErrorLocation(ErrorLocation):
    def __init__(self, path: str, instance):
        self.path = path
        self.instance = instance

    def to_dict(self):
        """
        Convert the grid location to a dictionary
        """
        return {"path": self.path, "instance": self.instance}

    def __str__(self):
        """
        Convert the grid location to a string
        """
        return f"[{self.path}, {self.instance}]"