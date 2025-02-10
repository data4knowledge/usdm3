import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00073 import RuleDDF00073

@pytest.fixture
def rule():
    """Fixture to create a RuleDDF00073 instance"""
    return RuleDDF00073()

def test_initialization(rule):
    """Test rule initialization"""
    assert rule.id == "DDF00073"
    assert rule.level == rule.WARNING
    assert rule.description == "Only one version of any code system is expected to be used within a study version."

def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"

