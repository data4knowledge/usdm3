import pytest
from usdm3.rules.library.rule_ddf00005 import RuleDDF00005
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00005()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00005"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Every study version must have exactly one study identifier with an identifier scope that references a clinical study sponsor organization."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
