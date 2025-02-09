import csv
from d4k_sel.errors import Errors
from usdm3.rules.library.rule_template import ValidationLocation


class RulesValidationResults:
    def __init__(self):
        self._items = {}

    def add_success(self, rule: str):
        self._items[rule] = {
            "status": "Success",
            "errors": None,
            "exception": None,
        }

    def add_failure(self, rule: str, errors: Errors):
        self._items[rule] = {
            "status": "Failure",
            "errors": [],
            "exception": None,
        }
        for error in errors._items:
            item = error.to_dict()
            self._items[rule]["errors"].append(item)

    def add_exception(self, rule: str, exception: Exception):
        self._items[rule] = {
            "status": "Exception",
            "errors": None,
            "exception": str(exception),
        }

    def add_not_implemented(self, rule: str):
        self._items[rule] = {
            "status": "Not Implemented",
            "errors": None,
            "exception": None,
        }

    def count(self):
        return len(self._items)

    def passed(self):
        return all(item["status"] == "Success" for item in self._items.values())

    def to_dict(self):
        return self._items

    def as_csv(self, filename: str) -> list[list[dict]]:
        if len(self._items) == 0:
            return []
        else:
            headers = ["rule", "status", "exception"] + ValidationLocation.headers()
            rows = [headers]
            for rule, item in self._items.items():
                row = [rule, item["status"], str(item["exception"])]
                for error in item["errors"]:
                    row.extend(
                        [error[header] for header in ValidationLocation.headers()]
                    )
                rows.append(row)
            return rows
