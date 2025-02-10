import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00116 import RuleDDF00116
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00116 instance"""
    rule = "DDF00116"
    level = RuleTemplate.WARNING
    description = "A study version's study type must be specified using the Study Type Response (C99077) SDTM codelist."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00116"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "A study version's study type must be specified using the Study Type Response (C99077) SDTM codelist."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

