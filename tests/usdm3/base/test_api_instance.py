from usdm3.base.api_instance import APIInstance
from usdm3.base.globals import Globals
from usdm3.api.code import Code


class Something:
    pass


def test_api_instance():
    globals = Globals()
    api_instance = APIInstance(globals)
    assert api_instance is not None


def test_create():
    globals = Globals()
    globals.clear()
    api_instance = APIInstance(globals)
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
    globals = Globals()
    globals.clear()
    api_instance = APIInstance(globals)
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
    globals = Globals()
    globals.clear()
    api_instance = APIInstance(globals)
    code = api_instance.create(Something, {"code": "CODE-1"})
    assert code is None
    assert globals.errors.dump()[0] == {
        "level": "Error",
        "location": {
            "class_name": "APIInstance",
            "method_name": "create",
        },
        "message": "Exception ''Something'' raised. Error creating class 'Something' API instance",
    }
