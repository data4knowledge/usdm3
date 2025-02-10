import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00137 import RuleDDF00137
from usdm3.rules.library.rule_template import RuleTemplate

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00137 instance"""
    rule = "DDF00137"
    level = RuleTemplate.WARNING
    description = "References must be a fixed value or a reference to items stored elsewhere in the data model which must be specified in the correct format. They must start with '<usdm:ref', end with either '/>' or '></usdm:ref>', and must contain 'klass=\"klassName\"', 'id=\"idValue\"', and 'attribute=\"attributeName\"/>' in any order (where \"klassName\" and \"attributeName\" contain only letters in upper or lower case)."
    return RuleTemplate(rule, level, description)

def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00137"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "References must be a fixed value or a reference to items stored elsewhere in the data model which must be specified in the correct format. They must start with '<usdm:ref', end with either '/>' or '></usdm:ref>', and must contain 'klass=\"klassName\"', 'id=\"idValue\"', and 'attribute=\"attributeName\"/>' in any order (where \"klassName\" and \"attributeName\" contain only letters in upper or lower case)."
    assert rule._errors.count() == 0

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

