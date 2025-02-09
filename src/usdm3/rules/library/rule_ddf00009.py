from .rule_template import RuleTemplate


class RuleDDF00009(RuleTemplate):
    """
    DDF00009: Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing.

    Applies to: Timing
    Attributes: type
    """

    def __init__(self):
        super().__init__(
            "DDF00009",
            RuleTemplate.ERROR,
            "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing.",
        )

    def validate(self, config: dict) -> bool:
        """
        Validate the rule against the provided data

        Args:
            config (dict): Standard configuration structure contain the data, CT etc

        Returns:
            bool: True if validation passes
        """
        data = config["data"]
        items = data.instances_by_klass("ScheduledTimeline")
        for item in items:
            valid = False
            for timing in item["timings"]:
                if timing["type"]["decode"] == "Fixed Reference":
                    valid = True
            if not valid:
                self._add_failure(
                    "No fixed reference timing",
                    item["instanceType"],
                    "timings",
                    item["id"],
                )
        return self._result()
