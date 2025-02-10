import pytest
from usdm3.rules.library.rule_ddf00031 import RuleDDF00031
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00031()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00031"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'If timing type is not "Fixed Reference" then it must point to two scheduled instances (e.g. the relativeFromScheduledInstance and relativeToScheduledInstance attributes must not be missing and must not be equal to each other).'
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
