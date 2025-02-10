import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00085 import RuleDDF00085
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00085 instance"""
    rule = "DDF00085"
    level = RuleTemplate.WARNING
    description = "Narrative content text is expected to be HTML formatted."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00085"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Narrative content text is expected to be HTML formatted."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

