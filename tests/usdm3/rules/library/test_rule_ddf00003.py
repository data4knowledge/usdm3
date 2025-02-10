import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00003 import RuleDDF00003
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00003 instance"""
    rule = "DDF00003"
    level = RuleTemplate.WARNING
    description = "If the duration of an administration will vary, a quantity is not expected for the administration duration and vice versa."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00003"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "If the duration of an administration will vary, a quantity is not expected for the administration duration and vice versa."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

