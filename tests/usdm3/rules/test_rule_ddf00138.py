import pytest
from usdm3.rules.library.rule_ddf00138 import RuleDDF00138
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00138()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00138"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Every identifier must be unique within the scope of an identified organization."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
