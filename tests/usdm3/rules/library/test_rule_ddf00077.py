import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00077 import RuleDDF00077
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00077 instance"""
    rule = "DDF00077"
    level = RuleTemplate.WARNING
    description = "If geographic scope type is global then no codes are expected to specify the specific area within scope while if it is not global then at least one code is expected to specify the specific area within scope."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00077"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "If geographic scope type is global then no codes are expected to specify the specific area within scope while if it is not global then at least one code is expected to specify the specific area within scope."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

