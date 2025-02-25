import pytest
from unittest.mock import Mock
from usdm3.rules.library.rule_ddf00155 import RuleDDF00155
from usdm3.rules.library.rule_template import RuleTemplate


@pytest.fixture
def rule():
    return RuleDDF00155()


def test_initialization(rule):
    """Test rule initialization"""
    assert rule._rule == "DDF00155"
    assert rule._level == RuleTemplate.ERROR
    assert (
        rule._rule_text
        == "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format."
    )
    assert rule._errors.count() == 0


def test_validate_valid(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2020-03-27",
        },
        {
            "id": "code2",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2020-03-27",
        },
        {
            "id": "code3",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2020-03-27",
        },
        {
            "id": "code4",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2021-12-17",
        },
        {
            "id": "code5",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2022-06-24",
        },
        {
            "id": "code6",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2022-09-30",
        },
        {
            "id": "code7",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2023-12-15",
        },
        {
            "id": "code8",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-03-29",
        },
        {
            "id": "code9",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2024-09-27",
        },
        {
            "id": "code10",
            "codeSystem": "http://www.example.com",
            "codeSystemVersion": "2024-09-27",
        },
    ]

    config = {"data": data_store}
    assert rule.validate(config) is True
    assert rule._errors.count() == 0

def test_validate_missing_code_system_version(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
            "codeSystem": "http://www.cdisc.org"
        },
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        'location': {
            'attribute': 'codeSystemVersion',
            'klass': 'Code',
            'path': 'path/path1',
            'rule': 'DDF00155',
            'rule_text': "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format.",
        },
        "message": "Missing codeSystemVersion",
    }


def test_validate_invalid_code_system_version(rule):
    data_store = Mock()
    data_store.instances_by_klass.return_value = [
        {
            "id": "code1",
            "codeSystem": "http://www.cdisc.org",
            "codeSystemVersion": "2020-03-01",
        },
    ]
    data_store.path_by_id.side_effect = ["path/path1"]

    config = {"data": data_store}
    assert rule.validate(config) is False
    assert rule._errors.count() == 1
    assert rule._errors._items[0].to_dict() == {
        "level": "Error",
        'location': {
            'attribute': 'codeSystemVersion',
            'klass': 'Code',
            'path': 'path/path1',
            'rule': 'DDF00155',
            'rule_text': "For CDISC codelist references (where the code system is 'http://www.cdisc.org'), the code system version must be a valid CDISC terminology release date in ISO 8601 date format.",
        },
        "message": "Invalid codeSystemVersion",
    }