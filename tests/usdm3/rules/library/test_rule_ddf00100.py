import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00100 import RuleDDF00100
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00100 instance"""
    rule = "DDF00100"
    level = RuleTemplate.WARNING
    description = (
        "Within a study version, there must be no more than one title of each type."
    )
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00100"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Within a study version, there must be no more than one title of each type."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
