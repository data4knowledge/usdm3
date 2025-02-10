import pytest
from usdm3.rules.library.rule_ddf00127 import RuleDDF00127
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00127()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00127"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "An encounter must only be scheduled at a timing that is defined within the same study design as the encounter."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
