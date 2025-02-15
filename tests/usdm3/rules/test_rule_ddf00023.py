import pytest
from usdm3.rules.library.rule_ddf00023 import RuleDDF00023
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00023()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00023"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "To ensure consistent ordering, when both previous and next attributes are available within an entity the previous id value must match the next id value of the referred instance."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
