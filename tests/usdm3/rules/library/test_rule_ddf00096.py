import pytest
from usdm3.rules.library.rule_ddf00096 import RuleDDF00096
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00096()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00096"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "All primary endpoints must be referenced by a primary objective."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
