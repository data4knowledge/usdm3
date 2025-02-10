import pytest
from usdm3.rules.library.rule_ddf00042 import RuleDDF00042
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00042()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00042"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "The range specified for a planned age is not expected to be approximate."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
