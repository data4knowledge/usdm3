import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00028 import RuleDDF00028
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00028 instance"""
    rule = "DDF00028"
    level = RuleTemplate.WARNING
    description = "An activity must only reference activities that are specified within the same study design."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00028"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "An activity must only reference activities that are specified within the same study design."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
