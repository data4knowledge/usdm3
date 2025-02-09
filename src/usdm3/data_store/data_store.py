import json


class DataStore:
    def __init__(self, filename: str):
        self._klasses = {}
        self._ids = {}
        self._parent = {}
        self._path = {}
        self.filename = filename
        self.data = None

    def decompose(self):
        self.data = self._load_data()
        self._decompose(self.data, None, "")

    def instance_by_id(self, id: str) -> dict:
        if id not in self._ids:
            return None
        return self._ids[id]

    def instances_by_klass(self, klass: str) -> list:
        if klass not in self._klasses:
            return []
        return list(self._klasses[klass].values())

    def parent_by_klass(self, id: str, klass: str) -> dict:
        found = False
        instance = self._ids[id]
        while not found:
            if instance["instanceType"] == klass:
                found = True
            else:
                instance = self._parent[instance["id"]]
        return instance

    def _decompose(self, data, parent, path, instance_index=None) -> None:
        if isinstance(data, dict):
            path = self._add_klass_instance(data, parent, path, instance_index)
            for key, value in data.items():
                if isinstance(value, dict):
                    self._decompose(value, data, path)
                elif isinstance(value, list):
                    for index, item in enumerate(value):
                        self._decompose(item, data, path, index)

    def _add_klass_instance(self, data, parent, path, instance_index) -> None:
        id = data["id"] if "id" in data else "-"
        klass = data["instanceType"] if "instanceType" in data else "Wrapper"
        print(f"ADD KLASS INSTANCE: {id}, {klass}")
        path = self._update_path(path, data, instance_index)
        if klass not in self._klasses:
            self._klasses[klass] = {}
        self._klasses[klass][id] = data
        self._ids[id] = data
        if parent:
            self._parent[data["id"]] = parent
        self._path[id] = path
        print(f"PATH: {path}")
        return path

    def _load_data(self) -> dict:
        with open(self.filename, "r") as file:
            return json.load(file)

    def _update_path(self, path: str, data: dict, instance_index: int) -> str:
        path = path + "." + data["instanceType"] if "instanceType" in data else "root"
        path = path + f"[{instance_index}]" if instance_index is not None else path
        return path
