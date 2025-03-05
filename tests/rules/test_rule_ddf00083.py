import pytest
from usdm3.rules.library.rule_ddf00083 import RuleDDF00083
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00083()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00083"
    assert rule._level == RuleTemplate.ERROR
    assert rule._rule_text == "Within a study version, all id values must be unique."
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    assert rule.validate(config)
