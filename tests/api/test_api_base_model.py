import datetime
import enum
from uuid import UUID
from usdm3.api.api_base_model import ApiBaseModel, _serialize_as_json


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
    fixed_uuid = UUID("12345678-1234-5678-1234-567812345678")

    to = TestOne(**{"id": "id", "x": "x", "y": "y"})
    tt = TestTwo(
        **{
            "id": "id",
            "z": "z",
            "d": datetime.date(2025, 1, 1),
            "u": fixed_uuid,
            "a": to,
        }
    )

    # Get the actual JSON and compare it to expected values
    actual_json = tt.to_json()
    assert '"id": "id"' in actual_json
    assert '"z": "z"' in actual_json
    assert '"d": "2025-01-01"' in actual_json
    assert '"u": "12345678-1234-5678-1234-567812345678"' in actual_json
    assert '"a": {"id": "id", "x": "x", "y": "y"}' in actual_json


def test_serialize_as_json_enum():
    """Test _serialize_as_json function with enum to cover line 11."""

    class TestEnum(enum.Enum):
        VALUE1 = "test_value"
        VALUE2 = "another_value"

    result = _serialize_as_json(TestEnum.VALUE1)
    assert result == "test_value"

    result = _serialize_as_json(TestEnum.VALUE2)
    assert result == "another_value"


def test_serialize_as_json_date():
    """Test _serialize_as_json function with date."""
    test_date = datetime.date(2025, 1, 15)
    result = _serialize_as_json(test_date)
    assert result == "2025-01-15"


def test_serialize_as_json_uuid():
    """Test _serialize_as_json function with UUID."""
    test_uuid = UUID("12345678-1234-5678-1234-567812345678")
    result = _serialize_as_json(test_uuid)
    assert result == "12345678-1234-5678-1234-567812345678"


def test_serialize_as_json_object():
    """Test _serialize_as_json function with regular object."""

    class TestObj:
        def __init__(self):
            self.attr1 = "value1"
            self.attr2 = "value2"

    test_obj = TestObj()
    result = _serialize_as_json(test_obj)
    assert result == {"attr1": "value1", "attr2": "value2"}
