import pytest
from usdm3.rules.library.rule_ddf00080 import RuleDDF00080
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00080()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00080"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "All scheduled activity instances are expected to refer to an epoch."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
