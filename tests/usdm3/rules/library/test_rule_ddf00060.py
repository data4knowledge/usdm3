import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00060 import RuleDDF00060
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00060 instance"""
    rule = "DDF00060"
    level = RuleTemplate.WARNING
    description = "The value for each timing must be a non-negative duration specified in ISO 8601 format."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00060"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "The value for each timing must be a non-negative duration specified in ISO 8601 format."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

