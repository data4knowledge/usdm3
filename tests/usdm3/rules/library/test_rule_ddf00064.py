import pytest
from usdm3.rules.library.rule_ddf00064 import RuleDDF00064
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00064()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00064"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A scheduled decision instance is not expected to refer to a timeline exit."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
