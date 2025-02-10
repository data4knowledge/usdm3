import pytest
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00104 instance"""
    rule = "DDF00104"
    level = RuleTemplate.WARNING
    description = "A timing's relative to/from property must be specified using the Timing Relative To From Value Set Terminology (C201265) SDTM codelist."
    return RuleTemplate(rule, level, description)


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00104"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A timing's relative to/from property must be specified using the Timing Relative To From Value Set Terminology (C201265) SDTM codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
