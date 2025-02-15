import pytest
from usdm3.rules.library.rule_ddf00094 import RuleDDF00094
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00094()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00094"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Within a study version, if a date of a specific type exists with a global geographic scope then no other dates are expected with the same type."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
