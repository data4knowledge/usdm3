from usdm3.base.id_manager import IdManager
from usdm3.api.address import Address


def test_check_id_valid():
    instance = IdManager(["Address", "Study"])
    # Valid ID with value greater than current index
    assert instance.check_id("Address_5") is True
    # After successful check, the index should be updated
    assert instance._id_index["Address"] == 5

    # Another valid ID with greater value
    assert instance.check_id("Study_10") is True
    assert instance._id_index["Study"] == 10


def test_check_id_invalid_format():
    instance = IdManager(["Address", "Study"])
    # No delimiter
    assert instance.check_id("Address5") is False
    # More than one delimiter
    assert instance.check_id("Address_5_extra") is False
    # Empty string
    assert instance.check_id("") is False


def test_check_id_invalid_class():
    instance = IdManager(["Address", "Study"])
    # Class not in registered classes
    assert instance.check_id("Unknown_5") is False


def test_check_id_invalid_value():
    instance = IdManager(["Address", "Study"])
    # Value not a digit
    assert instance.check_id("Address_abc") is False

    # Set up current index
    instance.build_id("Address")  # Address_1
    # Value not greater than current index
    assert instance.check_id("Address_1") is False


def test_init():
    instance_1 = IdManager(["Address", "xxx"])
    assert instance_1._id_index["Address"] == 0
    assert instance_1._id_index["xxx"] == 0


def test_clear():
    instance_1 = IdManager(["Address", "xxx"])
    instance_1.clear()
    assert instance_1._id_index["Address"] == 0
    assert instance_1._id_index["xxx"] == 0


def test_build_id_with_string():
    instance_1 = IdManager(["Address", "xxx"])
    assert instance_1.build_id("Address") == "Address_1"
    assert instance_1.build_id("Address") == "Address_2"
    assert instance_1.build_id("xxx") == "xxx_1"
    assert instance_1.build_id("xxx") == "xxx_2"


def test_build_id_with_class():
    instance_1 = IdManager(["Address"])
    assert instance_1.build_id(Address) == "Address_1"
    assert instance_1.build_id(Address) == "Address_2"
