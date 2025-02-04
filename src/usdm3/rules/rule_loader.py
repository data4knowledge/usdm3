import inspect
import pkgutil
import importlib
from pathlib import Path
from typing import List, Type
from rules.rule_template import RuleTemplate
import traceback


class RuleLoader:
    def __init__(self, rules_package: str):
        """
        Initialize the rule loader
        Args:
            rules_package (str): The package path where rule classes are located
        """
        self.rules_package = rules_package
        self.rules: List[Type[RuleTemplate]] = []

    def load_rules(self) -> List[Type[RuleTemplate]]:
        """
        Dynamically load all rule classes from the rules package
        Returns:
            List[Type[RuleTemplate]]: List of loaded rule classes
        """
        # Get the package module
        package = importlib.import_module(self.rules_package)
        package_path = Path(package.__file__).parent

        # Find all rule classes in the package
        for _, module_name, _ in pkgutil.iter_modules([str(package_path)]):
            # Import the module
            module = importlib.import_module(f"{self.rules_package}.{module_name}")

            # Find all classes in the module that inherit from RuleTemplate
            for name, obj in inspect.getmembers(module):
                if (
                    inspect.isclass(obj)
                    and issubclass(obj, RuleTemplate)
                    and obj != RuleTemplate
                ):
                    self.rules.append(obj)

        return self.rules

    def execute_rules(self, config: dict) -> List[dict]:
        """
        Execute all loaded validation rules
        Args:
            config (dict): The configuration to validate
        Returns:
            List[dict]: List of validation results
        """
        results = []

        for rule_class in self.rules:
            try:
                rule = rule_class()
                is_valid = rule.validate(config)
                results.append(
                    {
                        "rule": rule_class.__name__,
                        "valid": is_valid,
                        "errors": rule.errors(),
                    }
                )
            except NotImplementedError as e:
                results.append(
                    {
                        "rule": rule_class.__name__,
                        "valid": False,
                        "errors": None,
                        "exception": "Not implemented",
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "rule": rule_class.__name__,
                        "valid": False,
                        "errors": None,
                        "exception": traceback.format_exc(),
                    }
                )

        return results
