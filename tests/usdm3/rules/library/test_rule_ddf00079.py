import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00079 import RuleDDF00079
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00079 instance"""
    rule = "DDF00079"
    level = RuleTemplate.WARNING
    description = "If a synonym is specified then it is not expected to be equal to the name of the biomedical concept (case insensitive)."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00079"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "If a synonym is specified then it is not expected to be equal to the name of the biomedical concept (case insensitive)."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

