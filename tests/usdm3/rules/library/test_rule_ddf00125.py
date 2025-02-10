import pytest
from usdm3.rules.library.rule_ddf00125 import RuleDDF00125
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00125()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00125"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "Attributes must be included as defined in the USDM schema based on the API specification (i.e., all required properties are present and no additional attributes are present)."
    )
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"
