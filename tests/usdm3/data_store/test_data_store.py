import pytest
from pathlib import Path
from usdm3.data_store.data_store import DataStore, DecompositionError


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


def test_id_errors(data_store_with_id_errors):
    """Test id errors in JSON"""
    with pytest.raises(DecompositionError) as e:
        data_store_with_id_errors.decompose()
    # assert str(e) == "error decomposing the '.json' file, missing id at $.Study.StudyVersion[0].StudyDesign[0], with xxx"
    print(f"X: {str(e.value)}")


def test_instance_type_errors(data_store_with_instance_type_errors):
    """Test id errors in JSON"""
    with pytest.raises(DecompositionError) as e:
        data_store_with_id_errors.decompose()
    print(f"X: {str(e.value)}")
