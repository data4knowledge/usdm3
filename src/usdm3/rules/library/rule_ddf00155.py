from .rule_template import RuleTemplate


class RuleDDF00155(RuleTemplate):
    """
    DDF00155: For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format.

    Applies to: Code
    Attributes: codeSystemVersion
    """

    def __init__(self):
        super().__init__(
            "DDF00155",
            RuleTemplate.ERROR,
            "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format.",
        )

    def validate(self, config: dict) -> bool:
        data = config["data"]
        items = data.instances_by_klass("Code")
        for item in items:
            if "codeSystem" in item and item["codeSystem"] == "http://www.cdisc.org":
                if "codeSystemVersion" not in item:
                    self._add_failure(
                        "Missing codeSystemVersion",
                        "Code",
                        "codeSystemVersion",
                        data.path_by_id(item["id"]),
                    )
                else:
                    if item["codeSystemVersion"] not in ["2023-06-01", "2023-06-01"]:
                        self._add_failure(
                            "Invalid codeSystemVersion",
                            "Code",
                            "codeSystemVersion",
                            data.path_by_id(item["id"]),
                        )
        return self._result()
