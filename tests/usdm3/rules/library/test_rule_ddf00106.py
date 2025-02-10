import pytest
from usdm3.rules.library.rule_ddf00106 import RuleDDF00106
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00106()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00106"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "A scheduled activity instance must only reference an encounter that is defined within the same study design as the scheduled activity instance."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
