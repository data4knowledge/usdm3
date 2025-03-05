import pytest
from usdm3.rules.library.rule_ddf00151 import RuleDDF00151
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00151()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00151"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "If geographic scope type is global then there must be only one geographic scope specified."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
