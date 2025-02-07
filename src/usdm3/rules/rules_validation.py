import inspect
import pkgutil
import importlib
from pathlib import Path
from typing import List, Type
from usdm3.rules.library.rule_template import RuleTemplate
from usdm3.data_store.data_store import DataStore
from usdm3.ct.cdisc_ct import ct


class RulesValidation:
    def __init__(self, rules_dir: str):
        """
        Initialize the rule loader
        Args:
            rules_dir (str): The package path where rule classes are located
        """
        self.rules_dir = rules_dir
        self.rules: List[Type[RuleTemplate]] = []

    def validate_rules(self, filename: str) -> List[dict]:
        """
        Validate the rules against the provided data
        Args:
            filename (str): The filename of the data to validate
        Returns:
            List[dict]: List of validation results
        """
        self._load_rules()
        data_store = DataStore(filename)
        data_store.decompose()
        config = {"data": data_store, "ct": ct}
        results = self._execute_rules(config)
        return results

    def _load_rules(self) -> None:
        """
        Dynamically load all rule classes from the rules package
        """
        
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

    def _execute_rules(self, config: dict) -> List[dict]:
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
                        "exception": None,
                    }
                )
            except NotImplementedError as e:
                results.append(
                    {
                        "rule": rule_class.__name__,
                        "valid": False,
                        "errors": None,
                        "exception": "not implemented",
                    }
                )
            except Exception as e:
                results.append(
                    {
                        "rule": rule_class.__name__,
                        "valid": False,
                        "errors": None,
                        "exception": str(e),
                    }
                )
        return results
