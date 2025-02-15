import pytest
from usdm3.rules.library.rule_ddf00067 import RuleDDF00067
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00067()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00067"
    assert rule._level == RuleTemplate.ERROR
    assert rule._rule_text == "A study cell must refer to at least one element."
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
