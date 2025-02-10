import pytest
from usdm3.rules.library.rule_ddf00008 import RuleDDF00008
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00008()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00008"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A scheduled activity instance must refer to either a default condition or a timeline exit, but not both."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
