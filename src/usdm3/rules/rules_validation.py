import inspect
import pkgutil
import importlib
from pathlib import Path
from typing import List, Type
from usdm3.rules.library.rule_template import RuleTemplate
from usdm3.data_store.data_store import DataStore
from usdm3.ct.cdisc.library import Library
from usdm3.rules.rules_validation_results import RulesValidationResults


class RulesValidation:
    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self.rules: List[Type[RuleTemplate]] = []

    def validate_rules(self, filename: str) -> RulesValidationResults:
        self._load_rules()
        data_store = DataStore(filename)
        data_store.decompose()
        ct = Library()
        config = {"data": data_store, "ct": ct}
        results = self._execute_rules(config)
        return results

    def _load_rules(self) -> None:
        # Get the package module
        package = importlib.import_module(self.rules_dir)
        package_path = Path(package.__file__).parent

        # Find all rule classes in the package
        for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
            # Import the module
            module = importlib.import_module(f"{self.rules_dir}.{module_name}")
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, RuleTemplate)
                    and obj != RuleTemplate
                ):
                    self.rules.append(obj)

    def _execute_rules(self, config: dict) -> RulesValidationResults:
        results = RulesValidationResults()
        for rule_class in self.rules:
            try:
                # Execute the rule
                rule: RuleTemplate = rule_class()
                passed = rule.validate(config)
                if passed:
                    results.add_success(rule._rule)
                else:
                    results.add_failure(rule._rule, rule.errors())
            except NotImplementedError:
                # Rule not implemented yet
                results.add_not_implemented(rule._rule)
            except Exception as e:
                results.add_exception(rule._rule, e)
        return results
