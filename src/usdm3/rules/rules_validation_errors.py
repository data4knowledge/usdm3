import csv
from d4k_sel.errors import Errors


class RulesValidationErrors:
    def __init__(self):
        self._items = []

    def add(self, errors: Errors):
        for error in errors._items:
            item = error.to_dict()
            self._items.append(item)

    def count(self):
        return len(self._items)

    def passed(self):
        return len(self._items) == 0

    def to_dict(self):
        return self._items

    def save_as_csv(self, filename: str):
        if len(self._items) == 0:
            with open(filename, "w") as f:
                f.write("")
        else:
            headers = self._items[0].keys()
            with open(filename, "w") as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                for item in self._items:
                    writer.writerow([item[header] for header in headers])
