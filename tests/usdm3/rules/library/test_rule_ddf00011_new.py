import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00011 import RuleDDF00011


@pytest.fixture
def rule():
    return RuleDDF00011()


def test_init(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00011"
    assert rule._level == rule.ERROR
    assert "Fixed Reference" in rule._rule_text
    assert "relativeFromScheduledInstance" in rule._rule_text


def test_validate_valid_timing(rule):
    """Test validation with valid timing (has required relationship)"""
    # Create mock data store with valid timing
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Fixed Reference"},
            "relativeFromScheduledInstance": "some_instance",
        }
    ]

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is True
    assert rule._errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("Timing")


def test_validate_invalid_timing(rule):
    """Test validation with invalid timing (missing relationship)"""
    # Create mock data store with invalid timing
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Fixed Reference"},
            # Missing relativeFromScheduledInstance
        }
    ]

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is False

    # Check error details
    errors = rule.errors()
    assert errors.count() == 1
    assert errors.dump(0) == []
    data_store.instances_by_klass.assert_called_once_with("Timing")


def test_validate_non_fixed_reference(rule):
    """Test validation with non-Fixed Reference timing"""
    # Create mock data store with non-Fixed Reference timing
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Other Type"},
            # Missing relativeFromScheduledInstance is OK here
        }
    ]

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is True
    errors = rule.errors()
    assert errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("Timing")


def test_validate_multiple_timings(rule):
    """Test validation with multiple timing instances"""
    # Create mock data store with multiple timings
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "timing1",
            "type": {"decode": "Fixed Reference"},
            "relativeFromScheduledInstance": "instance1",
        },
        {
            "id": "timing2",
            "type": {"decode": "Fixed Reference"},
            # Missing relativeFromScheduledInstance
        },
        {"id": "timing3", "type": {"decode": "Other Type"}},
    ]

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is False

    # Check error details
    errors = rule.errors()
    assert errors.count() == 1
    assert errors.dump(0) == []

    data_store.instances_by_klass.assert_called_once_with("Timing")


def test_validate_empty_data(rule):
    """Test validation with no timing instances"""
    # Create mock data store with no timings
    data_store = Mock()
    data_store.instances_by_klass.return_value = []

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is True
    errors = rule.errors()
    assert errors.count() == 0
    data_store.instances_by_klass.assert_called_once_with("Timing")
