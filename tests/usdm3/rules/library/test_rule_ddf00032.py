import pytest
from usdm3.rules.library.rule_ddf00032 import RuleDDF00032
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00032()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00032"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Within a study version, if more than 1 business therapeutic area is defined then they must be distinct."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
