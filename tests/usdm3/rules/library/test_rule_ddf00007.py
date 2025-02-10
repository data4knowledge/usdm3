import pytest
from usdm3.rules.library.rule_ddf00007 import RuleDDF00007
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00007()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00007"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'If timing type is "Fixed Reference" then it must point to only one scheduled instance (e.g. attribute relativeToScheduledInstance must be equal to relativeFromScheduledInstance or it must be missing).'
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
