import inspect
import importlib
import sys
from pathlib import Path
from typing import List, Type

from usdm3.rules.library.rule_template import RuleTemplate
from usdm3.data_store.data_store import DataStore
from usdm3.ct.cdisc.library import Library
from usdm3.rules.rules_validation_results import RulesValidationResults
from usdm3.base.singleton import Singleton

class RulesValidation(metaclass=Singleton):

    def __init__(self, rules_dir: str):
        self.rules_dir = rules_dir
        self.rules: List[Type[RuleTemplate]] = []
        self._load_rules()

    def validate_rules(self, filename: str) -> RulesValidationResults:
        data_store = DataStore(filename)
        data_store.decompose()
        ct = Library()
        config = {"data": data_store, "ct": ct}
        results = self._execute_rules(config)
        return results

    def _load_rules(self) -> None:
        # Get absolute path to the rules library directory
        library_path = Path(__file__).parent / "library"
        package_name = "usdm3.rules.library"

        # Iterate through all .py files in the library directory
        for file in library_path.glob("rule_*.py"):
            print(f"file: {file}")
            if file.name.startswith("rule_") and file.name.endswith(".py"):
                try:
                    # Create module name from file name
                    module_name = f"{package_name}.{file.stem}"
                    
                    # Load module using absolute path
                    spec = importlib.util.spec_from_file_location(module_name, str(file))
                    if spec is None or spec.loader is None:
                        continue

                    print(f"spec: {spec}")
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[spec.name] = module
                    spec.loader.exec_module(module)

                    for name, obj in inspect.getmembers(module):
                        #print(f"name: {name} obj: {obj}")
                        if (
                            inspect.isclass(obj)
                            and issubclass(obj, RuleTemplate)
                            and obj != RuleTemplate
                        ):
                            try:
                                self.rules.append(obj)
                                print(f"Rule: {obj}")
                            except Exception as e:
                                print(f"Failed to load rule from {file}: {str(e)}")
                                continue
                except Exception as e:
                    print(f"Failed to load rule from {file}: {str(e)}")
                    continue


    def _execute_rules(self, config: dict) -> RulesValidationResults:
        results = RulesValidationResults()
        for rule_class in self.rules:
            try:
                # Execute the rule
                rule: RuleTemplate = rule_class()
                passed = rule.validate(config)
                print(f"rule: {rule._rule} passed: {passed}")
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
