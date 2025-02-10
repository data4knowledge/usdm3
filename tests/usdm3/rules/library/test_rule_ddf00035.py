import pytest
from usdm3.rules.library.rule_ddf00035 import RuleDDF00035
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00035()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00035"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Within a code system and corresponding version, a one-to-one relationship between code and decode is expected."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
