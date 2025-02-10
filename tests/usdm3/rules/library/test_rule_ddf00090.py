import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00090 instance"""
    rule = "DDF00090"
    level = RuleTemplate.WARNING
    description = "The same Biomedical Concept Category must not be referenced more than once from the same activity."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00090"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "The same Biomedical Concept Category must not be referenced more than once from the same activity."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
