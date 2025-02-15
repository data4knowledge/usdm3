import pytest
from usdm3.rules.library.rule_ddf00076 import RuleDDF00076
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00076()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00076"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "If a biomedical concept is referenced from an activity then it is not expected to be referenced as well by a biomedical concept category that is referenced from the same activity."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
