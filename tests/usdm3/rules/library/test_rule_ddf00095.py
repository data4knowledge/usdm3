import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00095 import RuleDDF00095
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00095 instance"""
    rule = "DDF00095"
    level = RuleTemplate.WARNING
    description = "Within a study protocol document version, if a date of a specific type exists with a global geographic scope then no other dates are expected with the same type."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00095"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Within a study protocol document version, if a date of a specific type exists with a global geographic scope then no other dates are expected with the same type."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

