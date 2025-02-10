import pytest
from usdm3.rules.library.rule_ddf00088 import RuleDDF00088
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00088()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00088"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "Epoch ordering using previous and next attributes is expected to be consistent with the order of corresponding scheduled activity instances according to their specified default conditions."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
