import pytest
from usdm3.rules.library.rule_ddf00085 import RuleDDF00085
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00085()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00085"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "Narrative content text is expected to be HTML formatted."
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
