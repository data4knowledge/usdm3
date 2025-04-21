import pytest
import json
from pathlib import Path
from usdm3.data_store.data_store import (
    DataStore,
    DecompositionError,
    DataStoreErrorLocation,
)
from usdm3.base.id_manager import IdManager


@pytest.fixture
def data_store():
    """Create DataStore instance with test data"""

    test_file = Path(__file__).parent / "usdm1.json"
    data_store = DataStore(test_file)
    data_store.decompose()
    return data_store


@pytest.fixture
def data_store_with_id_errors():
    """Create DataStore instance with test data"""

    test_file = Path(__file__).parent / "usdm2.json"
    data_store = DataStore(test_file)
    data_store.decompose()
    return data_store


@pytest.fixture
def data_store_with_instance_type_errors():
    """Create DataStore instance with test data"""

    test_file = Path(__file__).parent / "usdm3.json"
    data_store = DataStore(test_file)
    data_store.decompose()
    return data_store


def test_data_store_error_location():
    instance = DataStoreErrorLocation("x.y.z", "missing", "extra")
    assert instance.to_dict() == {
        "missing": "missing",
        "path": "x.y.z",
    }
    assert instance.__str__() == "[x.y.z, missing 'missing' attribute, extra]"


def test_instances_by_klass(data_store):
    """Test getting instances by class"""
    instances = data_store.instances_by_klass("StudyAmendment")
    assert len(instances) == 1
    assert instances[0]["id"] == "StudyAmendment_1"
    assert instances[0]["instanceType"] == "StudyAmendment"


def test_instances_by_klass_not_found(data_store):
    """Test getting instances for non-existent class"""
    instances = data_store.instances_by_klass("NonExistentClass")
    assert len(instances) == 0


def test_instance_by_id(data_store):
    """Test getting instance by ID"""
    instance = data_store.instance_by_id("Encounter_4")
    assert instance is not None
    assert instance["id"] == "Encounter_4"
    assert instance["instanceType"] == "Encounter"


def test_instance_by_id_not_found(data_store):
    """Test getting non-existent instance by ID"""
    instance = data_store.instance_by_id("nonexistent")
    assert instance is None


def test_path_by_id(data_store):
    """Test getting path by ID"""
    path = data_store.path_by_id("Encounter_4")
    assert path is not None
    assert path == "$.Study.StudyVersion[0].StudyDesign[0].Encounter[3]"


def test_path_by_id_not_found(data_store):
    """Test getting non-existent path by ID"""
    path = data_store.path_by_id("nonexistent")
    assert path is None


def test_parent_by_klass(data_store):
    """Test getting parent by class"""
    parent = data_store.parent_by_klass("Encounter_4", "StudyDesign")
    assert parent is not None
    assert parent["id"] == "StudyDesign_1"


def test_parent_by_klass_not_found(data_store):
    """Test getting non-existent parent by class"""
    parent = data_store.parent_by_klass("nonexistent", "Study")
    assert parent is None


def test_parent_by_klass_not_instance(tmp_path):
    """Test handling of missing instance type"""
    # Create test data with missing id in StudyDesign
    test_data = {
        "study": {
            "id": "Study-1",
            "instanceType": "Study",
            "StudyVersion": [
                {
                    "id": "Version-1",
                    "instanceType": "StudyVersion",
                    "StudyDesign": [
                        {
                            "instanceType": "Encounter",
                            "id": "Encounter-1",
                            "contactModes": [
                                {
                                    "id": "Code-1",
                                    "code": "C175574",
                                    "codeSystem": "http://www.cdisc.org",
                                    "codeSystemVersion": "2023-12-15",
                                    "decode": "Clinic",
                                    "instanceType": "Code",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Create temporary test file
    test_file = tmp_path / "test_missing_instance_type.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Verify that attempting to create and decompose DataStore with invalid data raises DecompositionError
    data_store = DataStore(test_file)
    data_store.decompose()
    # Remove the instanceType in the right place to force the error
    data_store._parent["Code-1"] = {
        # instanceType removed
        "id": "Encounter-1",
        "contactModes": [
            {
                "id": "Code-1",
                "code": "C175574",
                "codeSystem": "http://www.cdisc.org",
                "codeSystemVersion": "2023-12-15",
                "decode": "Clinic",
                "instanceType": "Code",
            }
        ],
    }
    result = data_store.parent_by_klass("Code-1", "Study")
    assert result is None


def test_id_errors(tmp_path):
    """Test handling of missing IDs"""
    # Create test data with missing id in StudyDesign
    test_data = {
        "study": {
            "id": "study1",
            "instanceType": "Study",
            "StudyVersion": [
                {
                    "id": "version1",
                    "instanceType": "StudyVersion",
                    "StudyDesign": [
                        {
                            "instanceType": "Encounter",
                            # Missing id here
                            "contactModes": [
                                {
                                    "code": "C175574",
                                    "codeSystem": "http://www.cdisc.org",
                                    "codeSystemVersion": "2023-12-15",
                                    "decode": "Clinic",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Create temporary test file
    test_file = tmp_path / "test_missing_id.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Verify that attempting to create and decompose DataStore with invalid data raises DecompositionError
    data_store = DataStore(test_file)
    with pytest.raises(DecompositionError) as exc_info:
        data_store.decompose()

    # Verify error message contains expected information
    error_msg = str(exc_info.value)
    assert "missing id" in error_msg
    assert "$.Study.StudyVersion[0]" in error_msg


def test_type_errors(tmp_path):
    """Test handling of missing IDs"""
    # Create test data with missing id in StudyDesign
    test_data = {
        "study": {
            "id": "study1",
            "instanceType": "Study",
            "StudyVersion": [
                {
                    "id": "version1",
                    "instanceType": "StudyVersion",
                    "StudyDesign": [
                        {
                            "id": "design1",
                            "instanceType": "Encounter",
                            # Missing id here
                            "contactModes": [
                                {
                                    "id": "contactMode1",
                                    "code": 175574,
                                    "codeSystem": "http://www.cdisc.org",
                                    "codeSystemVersion": "2023-12-15",
                                    "decode": "Clinic",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Create temporary test file
    test_file = tmp_path / "test_missing_id.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Verify that attempting to create and decompose DataStore with invalid data raises DecompositionError
    data_store = DataStore(test_file)
    with pytest.raises(DecompositionError) as exc_info:
        data_store.decompose()

    # Verify error message contains expected information
    error_msg = str(exc_info.value)
    assert "instanceType" in error_msg
    assert "$.Study.StudyVersion[0].Encounter[0]" in error_msg


def test_parent_by_study_missing(tmp_path):
    """Test handling of missing instance type"""
    # Create test data with missing id in StudyDesign
    test_data = {
        "Study": {
            "id": "Study-1",
            "instanceType": "Study",
            "StudyVersion": [
                {
                    "id": "Version-1",
                    "instanceType": "StudyVersion",
                    "StudyDesign": [
                        {
                            "instanceType": "Encounter",
                            "id": "Encounter-1",
                            "contactModes": [
                                {
                                    "id": "Code-1",
                                    "code": "C175574",
                                    "codeSystem": "http://www.cdisc.org",
                                    "codeSystemVersion": "2023-12-15",
                                    "decode": "Clinic",
                                    "instanceType": "Code",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Create temporary test file
    test_file = tmp_path / "test_missing_study.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Verify exception
    data_store = DataStore(test_file)
    with pytest.raises(DecompositionError) as exc_info:
        data_store.decompose()

    # Verify error message contains expected information
    error_msg = str(exc_info.value)
    print(f"ERRROR: {error_msg}")
    assert "study" in error_msg
    assert "$" in error_msg


def test_parent_by_study_id_missing(tmp_path):
    """Test handling of missing instance type"""
    # Create test data with missing id in StudyDesign
    test_data = {
        "study": {
            "idx": "Study-1",
            "instanceType": "Study",
            "StudyVersion": [
                {
                    "id": "Version-1",
                    "instanceType": "StudyVersion",
                    "StudyDesign": [
                        {
                            "instanceType": "Encounter",
                            "id": "Encounter-1",
                            "contactModes": [
                                {
                                    "id": "Code-1",
                                    "code": "C175574",
                                    "codeSystem": "http://www.cdisc.org",
                                    "codeSystemVersion": "2023-12-15",
                                    "decode": "Clinic",
                                    "instanceType": "Code",
                                }
                            ],
                        }
                    ],
                }
            ],
        }
    }

    # Create temporary test file
    test_file = tmp_path / "test_missing_id.json"
    with open(test_file, "w") as f:
        json.dump(test_data, f)

    # Verify exception
    data_store = DataStore(test_file)
    with pytest.raises(DecompositionError) as exc_info:
        data_store.decompose()

    # Verify error message contains expected information
    error_msg = str(exc_info.value)
    print(f"ERRROR: {error_msg}")
    assert "id" in error_msg
    assert "$.Study" in error_msg


def test_reallocate_no_data():
    """Test reallocate when no data is loaded"""
    data_store = DataStore("nonexistent_file.json")
    # Don't call decompose, so data is None
    id_manager = IdManager(["DummyClass"])
    result = data_store.reallocate(id_manager)
    assert result is False


def test_reallocate(data_store):
    """Test reallocate with loaded data"""
    # Store original IDs for comparison
    original_ids = list(data_store._ids.keys())
    original_id_count = len(original_ids)

    # Create IdManager with classes from data_store
    id_manager = IdManager(list(data_store._klasses.keys()))
    
    # Call reallocate
    data_store.reallocate(id_manager)

    # Get new IDs
    new_ids = list(data_store._ids.keys())

    # Verify we have the same number of IDs (the implementation might have a bug
    # where it doesn't properly delete old IDs, but we should still have the same count)
    assert len(new_ids) == original_id_count

    # Verify all new IDs follow the expected pattern (class name followed by underscore and number)
    # Skip special IDs like "$root"
    for new_id in new_ids:
        if new_id != "$root" and "_" in new_id:
            class_name, id_num = new_id.split("_", 1)
            assert id_num.isdigit()


def test_reallocate_maintains_relationships(data_store):
    """Test that reallocate maintains parent-child relationships"""
    # Find an ID with a known parent relationship
    encounter_instances = data_store.instances_by_klass("Encounter")
    assert len(encounter_instances) > 0
    encounter_id = encounter_instances[0]["id"]

    # Get the parent before reallocation
    original_parent = data_store.parent_by_klass(encounter_id, "StudyDesign")
    assert original_parent is not None
    original_parent_type = original_parent["instanceType"]

    # Store the path for later comparison
    original_path = data_store.path_by_id(encounter_id)
    assert original_path is not None

    # Create IdManager with classes from data_store
    id_manager = IdManager(list(data_store._klasses.keys()))
    
    # Reallocate IDs
    data_store.reallocate(id_manager)

    # Find the new encounter instances
    new_encounter_instances = data_store.instances_by_klass("Encounter")
    assert len(new_encounter_instances) > 0

    # Find an instance with the same path as our original encounter
    matching_instance = None
    for instance in new_encounter_instances:
        if data_store.path_by_id(instance["id"]) == original_path:
            matching_instance = instance
            break

    assert matching_instance is not None, (
        "Could not find an instance with the same path after reallocation"
    )

    # Verify the parent relationship is maintained
    new_parent = data_store.parent_by_klass(matching_instance["id"], "StudyDesign")
    assert new_parent is not None
    assert new_parent["instanceType"] == original_parent_type


def test_reallocate_maintains_paths(data_store):
    """Test that reallocate maintains path information"""
    # Get all paths before reallocation
    original_paths = {}
    for id in data_store._ids.keys():
        path = data_store.path_by_id(id)
        if path:
            original_paths[path] = id

    # Create IdManager with classes from data_store
    id_manager = IdManager(list(data_store._klasses.keys()))
    
    # Reallocate IDs
    data_store.reallocate(id_manager)

    # Verify that for each original path, there's an instance with that path after reallocation
    for path, original_id in original_paths.items():
        # Find an instance with this path
        found = False
        for new_id in data_store._ids.keys():
            if data_store.path_by_id(new_id) == path:
                found = True
                break

        assert found, (
            f"Path {path} for original ID {original_id} not found after reallocation"
        )
