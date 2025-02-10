import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00043 import RuleDDF00043
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00043 instance"""
    rule = "DDF00043"
    level = RuleTemplate.WARNING
    description = "A unit must not be specified for a planned enrollment number or a planned completion number."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00043"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A unit must not be specified for a planned enrollment number or a planned completion number."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
