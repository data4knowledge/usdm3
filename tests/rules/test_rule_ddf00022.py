import pytest
from usdm3.rules.library.rule_ddf00022 import RuleDDF00022
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00022()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00022"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "An instance of a class must not refer to itself as its next instance."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
