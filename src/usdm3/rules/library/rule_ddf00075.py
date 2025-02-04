from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00075(RuleTemplate):
    """
    DDF00075: An activity is expected to refer to at least one procedure, biomedical concept, biomedical concept category or biomedical concept surrogate.

    Applies to: Activity
    Attributes: definedProcedures, biomedicalConcepts, bcCategories, bcSurrogates
    """

    def __init__(self):
        super().__init__(
            "DDF00075",
            RuleTemplate.WARNING,
            "An activity is expected to refer to at least one procedure, biomedical concept, biomedical concept category or biomedical concept surrogate.",
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
