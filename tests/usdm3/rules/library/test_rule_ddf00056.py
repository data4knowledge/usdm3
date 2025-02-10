import pytest
from usdm3.rules.library.rule_ddf00056 import RuleDDF00056
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00056()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00056"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Within a study design, if more therapeutic areas are defined, they must be distinct."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
