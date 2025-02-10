import pytest
from usdm3.rules.library.rule_ddf00078 import RuleDDF00078
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00078()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00078"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "If a transition start rule is defined then an end rule is expected and vice versa."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
