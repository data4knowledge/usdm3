import pytest
from d4k_sel.errors import Errors, Error
from usdm3.rules.rules_validation_results import RulesValidationResults
from usdm3.rules.library.rule_template import ValidationLocation

@pytest.fixture
def validation_results():
    """Fixture to create a fresh RulesValidationResults instance"""
    return RulesValidationResults()

def test_initialization(validation_results):
    """Test initialization of RulesValidationResults"""
    assert validation_results._items == {}
    assert validation_results.count() == 0

def test_add_success(validation_results):
    """Test adding a successful validation result"""
    validation_results.add_success("test_rule")
    
    assert "test_rule" in validation_results._items
    assert validation_results._items["test_rule"]["status"] == "Success"
    assert validation_results._items["test_rule"]["errors"] is None
    assert validation_results._items["test_rule"]["exception"] is None
    assert validation_results.count() == 1

def test_add_failure(validation_results):
    """Test adding a failed validation result"""
    location = ValidationLocation(rule="test_rule", rule_text="test_rule_text", klass="test_klass", attribute="test_attribute", path="test_path")
    errors = Errors()
    errors.add("Test error", location, Errors.ERROR)
    
    validation_results.add_failure("test_rule", errors)
    
    assert validation_results.to_dict() ==     [
        {
            'exception': None,
            'level': 'Error',
            'location': {
                'attribute': 'test_attribute',
                'klass': 'test_klass',
                'path': 'test_path',
                'rule': 'test_rule',
                'rule_text': 'test_rule_text',
            },
            'message': 'Test error',
            'rule_id': 'test_rule',
            'status': 'Failure',
        },
    ]

def test_add_exception(validation_results):
    """Test adding an exception result"""
    exception = ValueError("Test exception")
    validation_results.add_exception("test_rule", exception)
    
    assert "test_rule" in validation_results._items
    assert validation_results._items["test_rule"]["status"] == "Exception"
    assert validation_results._items["test_rule"]["errors"] is None
    assert validation_results._items["test_rule"]["exception"] == str(exception)
    assert validation_results.count() == 1

def test_add_not_implemented(validation_results):
    """Test adding a not implemented result"""
    validation_results.add_not_implemented("test_rule")
    
    assert "test_rule" in validation_results._items
    assert validation_results._items["test_rule"]["status"] == "Not Implemented"
    assert validation_results._items["test_rule"]["errors"] is None
    assert validation_results._items["test_rule"]["exception"] is None
    assert validation_results.count() == 1

def test_count(validation_results):
    """Test count method with multiple results"""
    validation_results.add_success("rule1")
    validation_results.add_success("rule2")
    validation_results.add_success("rule3")
    
    assert validation_results.count() == 3

def test_passed_all_success(validation_results):
    """Test passed method when all results are successful"""
    validation_results.add_success("rule1")
    validation_results.add_success("rule2")
    
    assert validation_results.passed() is True

def test_passed_with_failure(validation_results):
    """Test passed method when there's a failure"""
    validation_results.add_success("rule1")
    validation_results.add_failure("rule2", Errors())
    
    assert validation_results.passed() is False

def test_passed_with_exception(validation_results):
    """Test passed method when there's an exception"""
    validation_results.add_success("rule1")
    validation_results.add_exception("rule2", Exception("test"))
    
    assert validation_results.passed() is False

def test_passed_with_not_implemented(validation_results):
    """Test passed method when there's a not implemented result"""
    validation_results.add_success("rule1")
    validation_results.add_not_implemented("rule2")
    
    assert validation_results.passed() is False

def test_to_dict_empty(validation_results):
    """Test to_dict method with no results"""
    assert validation_results.to_dict() == []

def test_to_dict_with_success(validation_results):
    """Test to_dict method with successful result"""
    validation_results.add_success("test_rule")
    assert validation_results.to_dict() == [
        {
            'exception': None,
            'level': '',
            'message': '',
            'location': {
                'attribute': '',
                'klass': '',
                'path': '',
                'rule': '',
                'rule_text': '',
            },
            'rule_id': 'test_rule',
            'status': 'Success',
        },
    ]
def test_to_dict_with_multiple_errors(validation_results):
    """Test to_dict method with multiple errors in one rule"""
    location = ValidationLocation(rule="test_rule", rule_text="test_rule_text", klass="test_klass", attribute="test_attribute", path="test_path")
    errors = Errors()
    errors.add("Error 1", location, Errors.ERROR)
    errors.add("Error 2", location, Errors.ERROR)
    
    validation_results.add_failure("test_rule", errors)
    assert validation_results.to_dict() == [
        {
            'exception': None,
            'level': 'Error',
            'location': {
                'attribute': 'test_attribute',
                'klass': 'test_klass',
                'path': 'test_path',
                'rule': 'test_rule',
                'rule_text': 'test_rule_text',
            },
            'message': 'Error 1',
            'rule_id': 'test_rule',
            'status': 'Failure',
        },
        {
            'exception': None,
            'level': 'Error',
            'location': {
                'attribute': 'test_attribute',
                'klass': 'test_klass',
                'path': 'test_path',
                'rule': 'test_rule',
                'rule_text': 'test_rule_text',
            },
            'message': 'Error 2',
            'rule_id': 'test_rule',
            'status': 'Failure',
        },
    ]

def test_to_dict_mixed_results(validation_results):
    """Test to_dict method with mixed result types"""
    validation_results.add_success("rule1")
    
    location = ValidationLocation(rule="rule2", rule_text="test_rule_text", klass="test_klass", attribute="test_attribute", path="test_path")
    errors = Errors()
    errors.add("Error 1", location, Errors.ERROR)
    errors.add("Error 2", location, Errors.ERROR)
    validation_results.add_failure("rule2", errors)
    
    validation_results.add_exception("rule3", Exception("test exception"))
    
    assert validation_results.to_dict() == [
        {
            'exception': None,
            'level': '',
            'message': '',
            'location': {
                'attribute': '',
                'klass': '',
                'path': '',
                'rule': '',
                'rule_text': '',
            },
            'rule_id': 'rule1',
            'status': 'Success',
        },
        {
            'exception': None,
            'level': 'Error',
            'location': {
                'attribute': 'test_attribute',
                'klass': 'test_klass',
                'path': 'test_path',
                'rule': 'rule2',
                'rule_text': 'test_rule_text',
            },
            'message': 'Error 1',
            'rule_id': 'rule2',
            'status': 'Failure',
        },
        {
            'exception': None,
            'level': 'Error',
            'location': {
                'attribute': 'test_attribute',
                'klass': 'test_klass',
                'path': 'test_path',
                'rule': 'rule2',
                'rule_text': 'test_rule_text',
            },
            'message': 'Error 2',
            'rule_id': 'rule2',
            'status': 'Failure',
        },
        {
            'exception': 'test exception',
            'level': '',
            'message': '',
            'location': {
                'attribute': '',
                'klass': '',
                'path': '',
                'rule': '',
                'rule_text': '',
            },
            'rule_id': 'rule3',
            'status': 'Exception',
        },
    ]