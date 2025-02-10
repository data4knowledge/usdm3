import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00074 instance"""
    rule = "DDF00074"
    level = RuleTemplate.WARNING
    description = "If the intervention model indicates a single group design then only one intervention is expected. In all other cases more interventions are expected."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00074"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "If the intervention model indicates a single group design then only one intervention is expected. In all other cases more interventions are expected."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
