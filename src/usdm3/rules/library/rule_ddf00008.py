from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00008(RuleTemplate):
    """
    DDF00008: A scheduled activity instance must refer to either a default condition or a timeline exit, but not both.

    Applies to: ScheduledActivityInstance
    Attributes: timelineExit, defaultCondition
    """

    def __init__(self):
        super().__init__(
            "DDF00008",
            RuleTemplate.ERROR,
            "A scheduled activity instance must refer to either a default condition or a timeline exit, but not both.",
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
        items = data.instances_by_klass("ScheduledActivityInstance")
        for item in items:
            if "timelineExitId" in item and "defaultConditionId" in item:
                timeline_exit = data.instance_by_id(item["timelineExitId"])
                default_condition = data.instance_by_id(item["defaultConditionId"])
                if timeline_exit and default_condition:
                    self._add_failure(
                        JSONLocation(item["instanceType"], "timelineExitId and defaultConditionId", item["id"])
                    )
        return self._result()