import pytest
from usdm3.rules.library.rule_ddf00037 import RuleDDF00037
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00037()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00037"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "At least one scheduled activity instance within a timeline must point to a timeline exit."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
