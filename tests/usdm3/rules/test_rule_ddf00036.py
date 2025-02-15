import pytest
from usdm3.rules.library.rule_ddf00036 import RuleDDF00036
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00036()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00036"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == 'If timing type is "Fixed Reference" then the corresponding attribute relativeToFrom must be filled with "Start to Start".'
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
