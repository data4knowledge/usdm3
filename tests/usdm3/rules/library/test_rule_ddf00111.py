import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00111 import RuleDDF00111
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00111 instance"""
    rule = "DDF00111"
    level = RuleTemplate.WARNING
    description = "The unit of a planned age is expected to be specified using terms from the Age Unit (C66781) SDTM codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00111"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "The unit of a planned age is expected to be specified using terms from the Age Unit (C66781) SDTM codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
