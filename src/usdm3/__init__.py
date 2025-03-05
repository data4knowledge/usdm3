import os
import pathlib
from usdm3.rules.rules_validation import RulesValidation
from usdm3.rules.rules_validation_results import RulesValidationResults
from usdm3.minimum.minimum import Minimum
from usdm3.api.wrapper import Wrapper


class USDM3:
    def validate(self, file_path: str) -> RulesValidationResults:
        validator = RulesValidation(self._library_path(), "usdm3.rules.library")
        return validator.validate_rules(file_path)

    def minimum(self, study_name: str, sponsor_id: str, version: str) -> Wrapper:
        return Minimum.minimum(study_name, sponsor_id, version)

    def _library_path(self) -> str:
        root = pathlib.Path(__file__).parent.resolve()
        return os.path.join(root, "rules/library")
