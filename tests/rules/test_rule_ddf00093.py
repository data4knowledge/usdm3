import pytest
from usdm3.rules.library.rule_ddf00093 import RuleDDF00093
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00093()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00093"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Date values associated to a study version must be unique regarding the combination of type and geographic scopes of the date."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
