import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00011 import RuleDDF00011
from tests.helpers.rule_error import error_timestamp


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
            "relativeFromScheduledInstanceId": "some_instance",
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
    data_store.path_by_id.return_value = "path/address1"

    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is False

    # Check error details
    errors = rule.errors()
    assert errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "relativeFromScheduledInstanceId",
            "klass": "Timing",
            "path": "path/address1",
            "rule": "DDF00011",
            "rule_text": 'Anchor timings (e.g. type is "Fixed Reference") must be related to a scheduled activity instance via a relativeFromScheduledInstance relationship.',
        },
        "message": "Missing relativeFromScheduledInstance",
        "type": "DDF00011",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
    }
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
            "relativeFromScheduledInstanceId": "instance1",
        },
        {
            "id": "timing2",
            "type": {"decode": "Fixed Reference"},
            # Missing relativeFromScheduledInstance
        },
        {"id": "timing3", "type": {"decode": "Other Type"}},
    ]
    data_store.path_by_id.return_value = "path/address1"
    config = {"data": data_store}

    # Validate
    assert rule.validate(config) is False

    # Check error details
    errors = rule.errors()
    assert errors.count() == 1
    assert error_timestamp(rule._errors) == {
        "level": "Error",
        "location": {
            "attribute": "relativeFromScheduledInstanceId",
            "klass": "Timing",
            "path": "path/address1",
            "rule": "DDF00011",
            "rule_text": 'Anchor timings (e.g. type is "Fixed Reference") must be related '
            "to a scheduled activity instance via a "
            "relativeFromScheduledInstance relationship.",
        },
        "message": "Missing relativeFromScheduledInstance",
        "timestamp": "YYYY-MM-DD HH:MM:SS.nnnnnn",
        "type": "DDF00011",
    }

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
