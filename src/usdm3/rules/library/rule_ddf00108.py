from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00108(RuleTemplate):
    """
    DDF00108: There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship).

    Applies to: ScheduleTimeline
    Attributes: exits
    """

    def __init__(self):
        super().__init__(
            "DDF00108",
            RuleTemplate.ERROR,
            "There must be at least one exit defined for each timeline (i.e., at least one instance of StudyTimelineExit linked via the 'exits' relationship).",
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
        items = data.instances_by_klass("StudyTimeline")
        for item in items:
            if exits := item.get("exits"):
                if len(exits) == 0:
                    self._add_failure(
                        "No exits defined for timeline",
                        "StudyTimeline",
                        "exits",
                        item["id"],
                    )
            else:
                self._add_failure(
                    "Missing exits",
                    "StudyTimeline",
                    "exits",
                    item["id"],
                )
        return self._errors.count() == 0
