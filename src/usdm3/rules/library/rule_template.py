from d4k_sel.error_location import ErrorLocation
from d4k_sel.errors import Errors


class ValidationLocation(ErrorLocation):
    def __init__(
        self, rule: str, rule_text: str, klass: str, attribute: str, path: str
    ):
        self.rule = rule
        self.rule_text = rule_text
        self.klass = klass
        self.attribute = attribute
        self.path = path

    def to_dict(self):
        return {
            "rule": self.rule,
            "rule_text": self.rule_text,
            "klass": self.klass,
            "attribute": self.attribute,
            "path": self.path,
        }

    @classmethod
    def headers(self):
        return ["rule", "rule_text", "klass", "attribute", "path"]

    def __str__(self):
        return f"{self.rule} [{self.rule_text}]: {self.klass}.{self.attribute} at {self.path}"


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

    def validate(self, config: dict) -> bool:
        """
        Run the rule on the data
        """
        raise NotImplementedError("rule is not implemented")

    def errors(self) -> Errors:
        return self._errors

    def _add_failure(self, message: str, klass: str, attribute: str, path: str):
        location = ValidationLocation(
            self._rule, self._rule_text, klass, attribute, path
        )
        self._errors.add(message, location, self._level)

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
                    self._add_failure(
                        "Invalid code/decode",
                        klass,
                        attribute,
                        data.path_by_id(item["id"]),
                    )
            else:
                self._add_failure(
                    "Missing attribute", klass, attribute, data.path_by_id(item["id"])
                )
        return self._result()
