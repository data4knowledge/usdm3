import pytest
from usdm3.rules.library.rule_ddf00152 import RuleDDF00152
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00152()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00152"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "An activity must only reference timelines that are specified within the same study design."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
