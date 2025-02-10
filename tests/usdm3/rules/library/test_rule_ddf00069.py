import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00069 instance"""
    rule = "DDF00069"
    level = RuleTemplate.WARNING
    description = "Each combination of arm and epoch must occur no more than once within a study design."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00069"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Each combination of arm and epoch must occur no more than once within a study design."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
