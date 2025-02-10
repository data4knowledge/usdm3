import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00143 import RuleDDF00143
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00143 instance"""
    rule = "DDF00143"
    level = RuleTemplate.WARNING
    description = "A study amendment reason must be coded using the study amendment reason (C207415) DDF codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00143"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A study amendment reason must be coded using the study amendment reason (C207415) DDF codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
