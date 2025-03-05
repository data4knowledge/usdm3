from src.usdm3.rules.rules_validation import RulesValidation
from src.usdm3.base.singleton import Singleton

def clear_rules_library():
    print(f"CLEAR RULES LIB")
    type(RulesValidation).clear(RulesValidation)
