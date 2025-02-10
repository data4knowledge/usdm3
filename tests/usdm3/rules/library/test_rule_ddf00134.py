import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00134 import RuleDDF00134
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00134 instance"""
    rule = "DDF00134"
    level = RuleTemplate.WARNING
    description = "Within a study design, if more characteristics are defined, they must be distinct."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00134"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Within a study design, if more characteristics are defined, they must be distinct."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
