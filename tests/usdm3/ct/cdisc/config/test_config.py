import pytest
from src.usdm3.ct.cdisc.config.config import Config


@pytest.fixture
def sample_config_file(tmp_path):
    """Create a sample config file for testing"""
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
    config_file = tmp_path / "ct_config.yaml"
    config_file.write_text(config_content)
    return config_file


def test_with_sample_config(sample_config_file, monkeypatch):
    """Test Config with a known sample configuration"""
    import os

    monkeypatch.setattr(os.path, "dirname", lambda _: str(sample_config_file.parent))

    config = Config()
    assert config.required_code_lists() == ["codelist1", "codelist2"]
    assert config.required_packages() == ["package1", "package2"]
    assert config.klass_and_attribute("TestClass", "testAttribute") == "test-codelist"
