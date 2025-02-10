import pytest
from usdm3.rules.library.rule_ddf00013 import RuleDDF00013
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00013()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00013"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "If a biomedical concept property is required then it must also be enabled, while if it is not enabled then it must not be required."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
