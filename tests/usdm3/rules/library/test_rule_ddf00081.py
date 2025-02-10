import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00081 instance"""
    rule = "DDF00081"
    level = RuleTemplate.ERROR
    description = "Class relationships must conform with the USDM schema based on the API specification."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00081"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Class relationships must conform with the USDM schema based on the API specification."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
