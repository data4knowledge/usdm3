import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00141 import RuleDDF00141
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00141 instance"""
    rule = "DDF00141"
    level = RuleTemplate.WARNING
    description = "A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00141"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A planned sex must be specified using the Sex of Participants (C66732) SDTM codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
