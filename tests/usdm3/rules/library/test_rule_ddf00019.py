import pytest
from usdm3.rules.library.rule_ddf00019 import RuleDDF00019
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00019()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00019"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A scheduled activity/decision instance must not refer to itself as its default condition."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
