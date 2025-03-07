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
