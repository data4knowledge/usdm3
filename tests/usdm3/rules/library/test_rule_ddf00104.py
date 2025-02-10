import pytest
from usdm3.rules.library.rule_ddf00104 import RuleDDF00104
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00104()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00104"
    assert rule._level == RuleTemplate.ERROR
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
