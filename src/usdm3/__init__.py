from usdm3.rules.rules_validation import RulesValidation
from usdm3.rules.rules_validation_results import RulesValidationResults

class USDM3:

    def validate(self, file_path: str) -> RulesValidationResults:
        validator = RulesValidation("usdm3/rules/library")
        return validator.validate_rules(file_path)
