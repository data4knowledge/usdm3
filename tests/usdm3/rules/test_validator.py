import pytest
from unittest.mock import Mock, patch
from usdm3.rules.validator import Validator
from usdm3.rules.library.rule_template import RuleTemplate

# Mock rule classes for testing
class MockValidRule(RuleTemplate):
    def validate(self, config):
        return True
    
    def errors(self):
        return []

class MockInvalidRule(RuleTemplate):
    def validate(self, config):
        return False
    
    def errors(self):
        return ["Test error"]

class MockErrorRule(RuleTemplate):
    def validate(self, config):
        raise Exception("Test exception")

class MockNotImplementedRule(RuleTemplate):
    pass  # validate not implemented

@pytest.fixture
def validator():
    return Validator("test_package")

@patch('pkgutil.iter_modules')
@patch('importlib.import_module')
def test_load_rules(mock_import_module, mock_iter_modules, validator):
    """Test loading rules from package"""
    # Setup mock module
    mock_module = Mock()
    mock_module.__file__ = "/path/to/module"
    mock_import_module.return_value = mock_module
    
    # Setup mock module iteration
    mock_iter_modules.return_value = [
        (None, "rule_module", None)
    ]
    
    # Setup mock module members
    mock_rule_module = Mock()
    mock_rule_module.__dict__ = {
        'TestRule': MockValidRule,
        'NotARule': object,  # Should be ignored
    }
    mock_import_module.return_value = mock_rule_module
    
    # Load rules
    rules = validator.load_rules()
    
    # Verify results
    assert len(rules) == 1
    assert rules[0] == MockValidRule
    mock_import_module.assert_any_call("test_package")
    mock_import_module.assert_any_call("test_package.rule_module")

def test_execute_rules_valid(validator):
    """Test executing rules with valid rule"""
    validator.rules = [MockValidRule]
    results = validator.execute_rules({})
    
    assert len(results) == 1
    assert results[0]["rule"] == "MockValidRule"
    assert results[0]["valid"] is True
    assert results[0]["errors"] == []
    assert results[0]["exception"] is None

def test_execute_rules_invalid(validator):
    """Test executing rules with invalid rule"""
    validator.rules = [MockInvalidRule]
    results = validator.execute_rules({})
    
    assert len(results) == 1
    assert results[0]["rule"] == "MockInvalidRule"
    assert results[0]["valid"] is False
    assert results[0]["errors"] == ["Test error"]
    assert results[0]["exception"] is None

def test_execute_rules_error(validator):
    """Test executing rules with rule that raises exception"""
    validator.rules = [MockErrorRule]
    results = validator.execute_rules({})
    
    assert len(results) == 1
    assert results[0]["rule"] == "MockErrorRule"
    assert results[0]["valid"] is False
    assert results[0]["errors"] is None
    assert results[0]["exception"] == "Test exception"

def test_execute_rules_not_implemented(validator):
    """Test executing rules with rule that has not implemented validate"""
    validator.rules = [MockNotImplementedRule]
    results = validator.execute_rules({})
    
    assert len(results) == 1
    assert results[0]["rule"] == "MockNotImplementedRule"
    assert results[0]["valid"] is False
    assert results[0]["errors"] is None
    assert results[0]["exception"] == "not implemented"

def test_execute_multiple_rules(validator):
    """Test executing multiple rules"""
    validator.rules = [MockValidRule, MockInvalidRule, MockErrorRule]
    results = validator.execute_rules({})
    
    assert len(results) == 3
    
    # Check valid rule results
    assert results[0]["rule"] == "MockValidRule"
    assert results[0]["valid"] is True
    
    # Check invalid rule results
    assert results[1]["rule"] == "MockInvalidRule"
    assert results[1]["valid"] is False
    assert results[1]["errors"] == ["Test error"]
    
    # Check error rule results
    assert results[2]["rule"] == "MockErrorRule"
    assert results[2]["valid"] is False
    assert results[2]["exception"] == "Test exception"

def test_empty_rules(validator):
    """Test executing with no rules loaded"""
    results = validator.execute_rules({})
    assert len(results) == 0