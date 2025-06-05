from usdm3.base.id_manager import IdManager
from usdm3.api.address import Address


def test_add_id():
    instance_1 = IdManager(["Address", "xxx"])

    # Test adding an ID with a higher number than current index
    instance_1.add_id("Address", "Address_5")
    assert instance_1._id_index["Address"] == 5

    # Test that build_id continues from the updated index
    assert instance_1.build_id("Address") == "Address_6"

    # Test that adding a lower number doesn't change the index
    instance_1.add_id("Address", "Address_3")
    assert instance_1._id_index["Address"] == 6

    # Test adding an ID for another class
    instance_1.add_id("xxx", "xxx_10")
    assert instance_1._id_index["xxx"] == 10
    assert instance_1.build_id("xxx") == "xxx_11"

    # Test with invalid ID format
    instance_1.add_id("Address", "InvalidFormat")
    assert instance_1._id_index["Address"] == 6  # Should remain unchanged


def test_find_id_instance():
    instance_1 = IdManager(["Address"])

    # Test with valid ID format
    assert instance_1._find_id_instance("Address_5") == 5
    assert instance_1._find_id_instance("xxx_123") == 123

    # Test with invalid ID format
    assert instance_1._find_id_instance("InvalidFormat") is None
    assert instance_1._find_id_instance("Address") is None
    assert instance_1._find_id_instance("Address_") is None
    assert instance_1._find_id_instance("_123") is None


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
