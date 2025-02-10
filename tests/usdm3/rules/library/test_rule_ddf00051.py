import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00051 import RuleDDF00051
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00051 instance"""
    rule = "DDF00051"
    level = RuleTemplate.WARNING
    description = "A timing's type must be specified using the Timing Type Value Set Terminology (C201264) DDF codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00051"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A timing's type must be specified using the Timing Type Value Set Terminology (C201264) DDF codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
