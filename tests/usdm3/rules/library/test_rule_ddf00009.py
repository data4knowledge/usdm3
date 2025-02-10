import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00009 instance"""
    rule = "DDF00009"
    level = RuleTemplate.WARNING
    description = "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00009"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Each schedule timeline must contain at least one anchor (fixed time) - i.e., at least one scheduled activity instance that is referenced by a Fixed Reference timing."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
