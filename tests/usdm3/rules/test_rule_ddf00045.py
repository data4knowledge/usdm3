import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00045 import RuleDDF00045
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00045()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00045"
    assert rule._level == RuleTemplate.WARNING
    assert rule._rule_text == "At least one attribute must be specified for an address."
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    empty_address = {
        "id": "address1",
        "text": "",
        "line": "",
        "city": "",
        "district": "",
        "state": "",
        "postalCode": "",
        "country": "",
        "instanceType": "Address",
    }
    data_store = Mock()
    data = []
    for attribute in [
        "text",
        "line",
        "city",
        "district",
        "state",
        "postalCode",
        "country",
    ]:
        address = dict(empty_address)
        address[attribute] = "value"
        data.append(address)
    data_store.instances_by_klass.return_value = data

    config = {"data": data_store}

    assert rule.validate(config) is True
    assert rule._errors.count() == 0


def test_validate_invalid(rule):
    empty_address = {
        "id": "address1",
        "text": "",
        "line": "",
        "city": "",
        "district": "",
        "state": "",
        "postalCode": "",
        "country": "",
        "instanceType": "Address",
    }
    data_store = Mock()
    data_store.instances_by_klass.return_value = [empty_address]
    data_store.path_by_id.return_value = "path/address1"
    config = {"data": data_store}

    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Warning",
        "location": {
            "attribute": "",
            "klass": "Address",
            "path": "path/address1",
            "rule": "DDF00045",
            "rule_text": "At least one attribute must be specified for an address.",
        },
        "message": "No attributes specified for address",
    }
