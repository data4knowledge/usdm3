from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00100(RuleTemplate):
    """
    DDF00100: Within a study version, there must be no more than one title of each type.

    Applies to: StudyVersion
    Attributes: titles
    """

    def __init__(self):
        super().__init__(
            "DDF00100",
            RuleTemplate.ERROR,
            "Within a study version, there must be no more than one title of each type.",
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
