import pytest
from usdm3.rules.library.rule_ddf00027 import RuleDDF00027
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00027()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00027"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "To ensure consistent ordering, the same instance must not be referenced more than once as previous or next."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
