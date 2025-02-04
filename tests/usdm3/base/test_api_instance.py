import pytest
from usdm3.base.api_instance import APIInstance
from usdm3.base.id_manager import IdManager
from usdm3.api.code import Code


class Something:
    pass


def test_api_instance():
    id_manager = IdManager()
    api_instance = APIInstance(id_manager)
    assert api_instance is not None


def test_create():
    id_manager = IdManager()
    api_instance = APIInstance(id_manager)
    code = api_instance.create(
        Code,
        {
            "id": "XXX",
            "code": "CODE-1",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1.0.0",
            "decode": "Decode-1",
        },
    )
    assert code.model_dump() == {
        "code": "CODE-1",
        "codeSystem": "CDISC",
        "codeSystemVersion": "1.0.0",
        "decode": "Decode-1",
        "id": "XXX",
        "instanceType": "Code",
    }


def test_create_no_id():
    id_manager = IdManager()
    api_instance = APIInstance(id_manager)
    code = api_instance.create(
        Code,
        {
            "code": "CODE-1",
            "codeSystem": "CDISC",
            "codeSystemVersion": "1.0.0",
            "decode": "Decode-1",
        },
    )
    assert code.model_dump() == {
        "code": "CODE-1",
        "codeSystem": "CDISC",
        "codeSystemVersion": "1.0.0",
        "decode": "Decode-1",
        "id": "Code_1",
        "instanceType": "Code",
    }


def test_create_exception():
    id_manager = IdManager()
    api_instance = APIInstance(id_manager)
    with pytest.raises(APIInstance.APIInstanceError):
        api_instance.create(Something, {"code": "CODE-1"})
