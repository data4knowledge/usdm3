import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00147 import RuleDDF00147
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00147 instance"""
    rule = "DDF00147"
    level = RuleTemplate.WARNING
    description = "An objective level must be specified using the objective level (C188725) DDF codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00147"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "An objective level must be specified using the objective level (C188725) DDF codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
