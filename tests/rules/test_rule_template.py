import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleTemplate("TEST0001", RuleTemplate.ERROR, "TEST RULE")


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "TEST0001"
    assert rule._level == RuleTemplate.ERROR
    assert rule._rule_text == "TEST RULE"
    assert rule._errors.count() == 0


def test_validate_not_implemented(rule):
    """Test that validate method raises NotImplementedError"""
    config = {"data": {}, "ct": {}}
    with pytest.raises(NotImplementedError) as exc_info:
        rule.validate(config)
    assert str(exc_info.value) == "rule is not implemented"


def test_return_errors(rule):
    assert rule.errors().count() == 0
    rule._add_failure("TEST MESSAGE", "TEST CLASS", "TEST ATTRIBUTE", "TEST PATH")
    assert rule.errors().count() == 1
    assert rule.errors()._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "TEST ATTRIBUTE",
            "klass": "TEST CLASS",
            "path": "TEST PATH",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "TEST MESSAGE",
    }


def test_add_failure(rule):
    rule._add_failure("TEST MESSAGE", "TEST CLASS", "TEST ATTRIBUTE", "TEST PATH")
    assert rule.errors().count() == 1
    assert rule.errors()._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "TEST ATTRIBUTE",
            "klass": "TEST CLASS",
            "path": "TEST PATH",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "TEST MESSAGE",
    }


def test_ct_check_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": {"code": "C12345", "decode": "Decode 1"}},
        {"id": "TEST ID", "attribute": {"code": "C12346", "decode": "Decode 2"}},
        {"id": "TEST ID", "attribute": [{"code": "C12346", "decode": "Decode 2"}]},
    ]
    data_store.path_by_id.return_value = "path/address1"
    ct = Mock()
    ct.klass_and_attribute.return_value = {
        "terms": [
            {"conceptId": "C12345", "preferredTerm": "Decode 1"},
            {"conceptId": "C12346", "preferredTerm": "Decode 2"},
        ]
    }

    config = {"data": data_store, "ct": ct}
    assert rule._ct_check(config, "klass", "attribute") is True
    assert rule.errors().count() == 0
    assert rule._result() is True


def test_ct_check_invalid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": {"code": "C12345", "decode": "Decode 1"}},
        {"id": "TEST ID", "attribute": {"code": "C12347", "decode": "Decode 2"}},
        {"id": "TEST ID", "attribute": {"code": "C12346", "decode": "Decode 3"}},
        {"id": "TEST ID", "attribute": {"code": "C12348", "decode": "Decode 3"}},
    ]
    data_store.path_by_id.side_effect = [
        "path/address1",
        "path/address2",
        "path/address3",
    ]
    ct = Mock()
    ct.klass_and_attribute.return_value = {
        "terms": [
            {"conceptId": "C12345", "preferredTerm": "Decode 1"},
            {"conceptId": "C12346", "preferredTerm": "Decode 2"},
        ]
    }

    config = {"data": data_store, "ct": ct}
    assert rule._ct_check(config, "klass", "attribute") is False
    assert rule.errors().count() == 3
    assert rule._result() is False
    assert rule.errors()._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address1",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid code 'C12347', the code is not in the codelist",
    }
    assert rule.errors()._items[1].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address2",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid decode 'Decode 3', the decode is not in the codelist",
    }
    assert rule.errors()._items[2].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address3",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid code and decode 'C12348' and 'Decode 3', neither the code and decode are in the codelist",
    }


def test_ct_check_invalid_list(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": [{"code": "C12345", "decode": "Decode 1"}]},
        {"id": "TEST ID", "attribute": [{"code": "C12347", "decode": "Decode 2"}]},
        {"id": "TEST ID", "attribute": [{"code": "C12346", "decode": "Decode 3"}]},
        {"id": "TEST ID", "attribute": {"code": "C12348", "decode": "Decode 3"}},
    ]
    data_store.path_by_id.side_effect = [
        "path/address1",
        "path/address2",
        "path/address3",
    ]
    ct = Mock()
    ct.klass_and_attribute.return_value = {
        "terms": [
            {"conceptId": "C12345", "preferredTerm": "Decode 1"},
            {"conceptId": "C12346", "preferredTerm": "Decode 2"},
        ]
    }

    config = {"data": data_store, "ct": ct}
    assert rule._ct_check(config, "klass", "attribute") is False
    assert rule.errors().count() == 3
    assert rule._result() is False
    assert rule.errors()._items[0].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address1",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid code 'C12347', the code is not in the codelist",
    }
    assert rule.errors()._items[1].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address2",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid decode 'Decode 3', the decode is not in the codelist",
    }
    assert rule.errors()._items[2].to_dict() == {
        "level": "Error",
        "location": {
            "attribute": "attribute",
            "klass": "klass",
            "path": "path/address3",
            "rule": "TEST0001",
            "rule_text": "TEST RULE",
        },
        "message": "Invalid code and decode 'C12348' and 'Decode 3', neither the code and decode are in the codelist",
    }


def test_ct_no_code_list(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": [{"code": "C12345", "decode": "Decode 1"}]}
    ]
    data_store.path_by_id.side_effect = [
        "path/address1",
    ]
    ct = Mock()
    ct.klass_and_attribute.return_value = None
    # config = {"data": data_store, "ct": ct}
    with pytest.raises(RuleTemplate.CTException):  # as exc_info:
        rule._check_codelist(ct, "x", "y")


def test_ct_no_terms(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": [{"code": "C12345", "decode": "Decode 1"}]}
    ]
    data_store.path_by_id.side_effect = [
        "path/address1",
    ]
    ct = Mock()
    ct.klass_and_attribute.return_value = {"terms": []}
    # config = {"data": data_store, "ct": ct}
    with pytest.raises(RuleTemplate.CTException):  # as exc_info:
        rule._check_codelist(ct, "x", "y")


def test_ct_missing_terms(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {"id": "TEST ID", "attribute": [{"code": "C12345", "decode": "Decode 1"}]}
    ]
    data_store.path_by_id.side_effect = [
        "path/address1",
    ]
    ct = Mock()
    ct.klass_and_attribute.return_value = {"termsXX": []}
    # config = {"data": data_store, "ct": ct}
    with pytest.raises(RuleTemplate.CTException):  # as exc_info:
        rule._check_codelist(ct, "x", "y")
