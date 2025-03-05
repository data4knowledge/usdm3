import pytest
from usdm3.rules.library.rule_ddf00139 import RuleDDF00139
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00139()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00139"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "An identified organization is not expected to have more than one identifier for the study."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
