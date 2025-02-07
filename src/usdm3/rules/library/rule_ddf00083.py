from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00083(RuleTemplate):
    """
    DDF00083: Within a study version, all id values must be unique.

    Applies to: All
    Attributes: id
    """

    def __init__(self):
        super().__init__(
            "DDF00083",
            RuleTemplate.ERROR,
            "Within a study version, all id values must be unique.",
        )

    def validate(self, config: dict) -> bool:
        """
        Validate the rule against the provided data

        Args:
            config (dict): Standard configuration structure contain the data, CT etc

        Returns:
            bool: True if validation passes
        """
        # See rule DDF00082 for schema checks
        return True
