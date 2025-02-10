import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00086 import RuleDDF00086
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00086 instance"""
    rule = "DDF00086"
    level = RuleTemplate.WARNING
    description = "Syntax template text is expected to be HTML formatted."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00086"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Syntax template text is expected to be HTML formatted."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

