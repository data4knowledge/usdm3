from src.usdm3.rules.rules_validation import RulesValidation3


def clear_rules_library():
    type(RulesValidation3)._clear(RulesValidation3)
