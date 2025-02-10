import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00131 import RuleDDF00131
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00131 instance"""
    rule = "DDF00131"
    level = RuleTemplate.WARNING
    description = "Referenced items in the narrative content must be available elsewhere in the data model."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00131"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Referenced items in the narrative content must be available elsewhere in the data model."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
