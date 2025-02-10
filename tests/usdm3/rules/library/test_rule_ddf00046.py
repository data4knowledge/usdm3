import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00046 import RuleDDF00046
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00046 instance"""
    rule = "DDF00046"
    level = RuleTemplate.WARNING
    description = "A timing must only be specified as being relative to/from a scheduled activity/decision instance that is defined within the same timeline as the timing."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00046"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "A timing must only be specified as being relative to/from a scheduled activity/decision instance that is defined within the same timeline as the timing."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

