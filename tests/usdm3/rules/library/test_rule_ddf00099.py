import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00099 instance"""
    rule = "DDF00099"
    level = RuleTemplate.WARNING
    description = (
        "All epochs are expected to be referred to from a scheduled Activity Instance."
    )
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00099"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "All epochs are expected to be referred to from a scheduled Activity Instance."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
