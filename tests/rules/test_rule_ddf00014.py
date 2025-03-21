import pytest
from usdm3.rules.library.rule_ddf00014 import RuleDDF00014
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00014()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00014"
    assert rule._level == RuleTemplate.WARNING
    assert (
        rule._rule_text
        == "A biomedical concept category is expected to have at least a member or a child."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
