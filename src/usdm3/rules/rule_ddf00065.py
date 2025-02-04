from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00065(RuleTemplate):
    """
    DDF00065: A scheduled decision instance is not expected to have a sub-timeline.

    Applies to: ScheduledDecisionInstance
    Attributes: timeline
    """

    def __init__(self):
        super().__init__(
            "DDF00065",
            RuleTemplate.WARNING,
            "A scheduled decision instance is not expected to have a sub-timeline.",
        )

    def validate(self, config: dict) -> bool:
        """
        Validate the rule against the provided data

        Args:
            config (dict): Standard configuration structure contain the data, CT etc

        Returns:
            bool: True if validation passes
        """
        raise NotImplementedError("Rule is not implemented")
