import datetime
from uuid import UUID, uuid4
from unittest.mock import patch
from usdm3.api.api_base_model import ApiBaseModel


class TestOne(ApiBaseModel):
    x: str
    y: str


class TestTwo(ApiBaseModel):
    z: str
    d: datetime.date
    a: TestOne
    u: UUID


def test_create():
    to = TestOne(**{"id": "id", "x": "x", "y": "y"})
    assert to.model_dump() == {
        "id": "id",
        "x": "x",
        "y": "y",
    }


# Test with direct UUID assignment
def test_to_json_direct():
    # Instead of mocking uuid4, we directly use a fixed UUID for testing
    # This effectively serves as a mock for uuid4() by providing a predictable value
    fixed_uuid = UUID('12345678-1234-5678-1234-567812345678')
    
    to = TestOne(**{"id": "id", "x": "x", "y": "y"})
    tt = TestTwo(**{"id": "id", "z": "z", "d": datetime.date(2025, 1, 1), "u": fixed_uuid, "a": to})
    
    # Get the actual JSON and compare it to expected values
    actual_json = tt.to_json()
    assert '"id": "id"' in actual_json
    assert '"z": "z"' in actual_json
    assert '"d": "2025-01-01"' in actual_json
    assert '"u": "12345678-1234-5678-1234-567812345678"' in actual_json
    assert '"a": {"id": "id", "x": "x", "y": "y"}' in actual_json


