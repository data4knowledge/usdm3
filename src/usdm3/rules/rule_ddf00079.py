from .rule_template import RuleTemplate, JSONLocation


class RuleDDF00079(RuleTemplate):
    """
    DDF00079: If a synonym is specified then it is not expected to be equal to the name of the biomedical concept (case insensitive).

    Applies to: BiomedicalConcept
    Attributes: synonyms
    """

    def __init__(self):
        super().__init__(
            "DDF00079",
            RuleTemplate.WARNING,
            "If a synonym is specified then it is not expected to be equal to the name of the biomedical concept (case insensitive).",
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
