from .rule_template import RuleTemplate


class RuleDDF00141(RuleTemplate):
    """
    DDF00141: A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist.

    Applies to: StudyDesignPopulation, StudyCohort
    Attributes: plannedSex
    """

    def __init__(self):
        super().__init__(
            "DDF00141",
            RuleTemplate.ERROR,
            "A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist.",
        )

    def validate(self, config: dict) -> bool:
        """
        Validate the rule against the provided data

        Args:
            config (dict): Standard configuration structure contain the data, CT etc

        Returns:
            bool: True if validation passes
        """
        pop_result = self._ct_check(config, "StudyDesignPopulation", "plannedSex")
        cohort_result = self._ct_check(config, "StudyCohort", "plannedSex")
        return pop_result or cohort_result
