import pytest
from usdm3.rules.library.rule_ddf00052 import RuleDDF00052
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00052()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00052"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "All standard code aliases referenced by an instance of the alias code class must be unique."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
