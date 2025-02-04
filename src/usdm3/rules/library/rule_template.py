from d4k_sel.error_location import ErrorLocation
from d4k_sel.errors import Errors
from data_store.data_store import DataStore


class JSONLocation(ErrorLocation):
    def __init__(self, klass: str, attribute: str, path: str):
        self.klass = klass
        self.attribute = attribute
        self.path = path

    def to_dict(self):
        return {"klass": self.klass, "attribute": self.attribute, "path": self.path}

    def __str__(self):
        return f"{self.klass}.{self.attribute} at {self.path}"


class RuleTemplate:
    """
    Base class for rule templates
    """

    ERROR = Errors.ERROR
    WARNING = Errors.WARNING

    def __init__(self, rule: str, level: int, rule_text: str):
        self._errors = Errors()
        self._rule = rule
        self._level = level
        self._rule_text = rule_text

    def validate(self, data: DataStore) -> bool:
        """
        Run the rule on the data
        """
        raise NotImplementedError("Rule not implemented")

    def errors(self) -> Errors:
        return self._errors

    def _add_failure(self, location: JSONLocation):
        self._errors.add(location, f"{self._rule}: {self._rule_text}", self._level)

    def _result(self) -> bool:
        return self._errors.count() == 0

    def _ct_check(self, config: dict, klass: str, attribute: str) -> bool:
        data = config["data"]
        ct = config["ct"]
        items = data.instances_by_klass(klass)
        codelist = ct.klass_and_attribute(klass, attribute)
        codes = [x["conceptId"] for x in codelist["terms"]]
        decodes = [x["preferredTerm"] for x in codelist["terms"]]
        for item in items:
            if attribute in item:
                if (
                    item[attribute]["code"] not in codes
                    or item[attribute]["decode"] not in decodes
                ):
                    self._add_failure(JSONLocation(klass, attribute, item["id"]))
            else:
                self._add_failure(JSONLocation(klass, attribute, item["id"]))
        return self._result()
