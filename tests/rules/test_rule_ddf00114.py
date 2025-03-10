import pytest
from usdm3.rules.library.rule_ddf00114 import RuleDDF00114
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00114()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00114"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "If specified, the context of a condition must point to a valid instance in the activity or scheduled activity instance class."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
