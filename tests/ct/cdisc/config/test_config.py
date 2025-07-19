import pytest
from src.usdm3.ct.cdisc.config.config import Config


@pytest.fixture
def temp_file(tmp_path):
    filename = "ct_config.yaml"
    config_content = """
    code_lists:
      - "codelist1"
      - "codelist2"
    packages:
      - "package1"
      - "package2"
    klass_attribute_mapping:
      TestClass:
        testAttribute: "test-codelist"
    """
    config_file = tmp_path / filename
    config_file.write_text(config_content)
    return filename


def test_with_sample_config(tmp_path, temp_file):
    config = Config(str(tmp_path), temp_file)
    assert config.required_code_lists() == ["codelist1", "codelist2"]
    assert config.required_packages() == ["package1", "package2"]
    assert config.klass_and_attribute("TestClass", "testAttribute") == "test-codelist"


def test_klass_and_attribute_with_class_object(tmp_path, temp_file):
    """Test klass_and_attribute with class object instead of string"""
    config = Config(str(tmp_path), temp_file)
    
    class TestClass:
        pass
    
    # Test with class object - this should cover line 24 (klass.__name__)
    result = config.klass_and_attribute(TestClass, "testAttribute")
    assert result == "test-codelist"


def test_klass_and_attribute_exception(tmp_path, temp_file):
    """Test klass_and_attribute with non-existent mapping to cover exception handling"""
    config = Config(str(tmp_path), temp_file)
    
    # Test exception for non-existent class/attribute - this should cover lines 24-25
    with pytest.raises(ValueError) as excinfo:
        config.klass_and_attribute("NonExistentClass", "nonExistentAttribute")
    assert "failed to find codelist for class 'NonExistentClass' attribute 'nonExistentAttribute'" in str(excinfo.value)
    
    # Test exception for existing class but non-existent attribute
    with pytest.raises(ValueError) as excinfo:
        config.klass_and_attribute("TestClass", "nonExistentAttribute")
    assert "failed to find codelist for class 'TestClass' attribute 'nonExistentAttribute'" in str(excinfo.value)
