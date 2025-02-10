import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00054 instance"""
    rule = "DDF00054"
    level = RuleTemplate.WARNING
    description = "Within an encounter there must be no duplicate contact modes."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00054"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Within an encounter there must be no duplicate contact modes."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
