import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00044 instance"""
    rule = "DDF00044"
    level = RuleTemplate.WARNING
    description = "The target for a condition must not be equal to its parent."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00044"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text == "The target for a condition must not be equal to its parent."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
