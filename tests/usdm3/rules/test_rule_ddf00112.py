import pytest
from usdm3.rules.library.rule_ddf00112 import RuleDDF00112
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00112()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00112"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A study intervention's role must be specified using the study intervention role (C207417) DDF codelist."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
