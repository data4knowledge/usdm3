import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00109 import RuleDDF00109
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00109 instance"""
    rule = "DDF00109"
    level = RuleTemplate.WARNING
    description = "A study element must only reference study interventions that are defined within the same study design as the study element."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00109"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A study element must only reference study interventions that are defined within the same study design as the study element."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
