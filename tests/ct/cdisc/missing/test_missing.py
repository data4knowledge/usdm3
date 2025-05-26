import os
import pathlib
from usdm3.ct.cdisc.missing.missing import Missing

def root_path():
    base = pathlib.Path(__file__).parent.parent.parent.parent.parent.resolve()
    #print(f"BASE: {base}")
    return os.path.join(base, "src/usdm3")

def test_missing_initialization():
    """Test that Missing class can be initialized and loads YAML file"""
    missing = Missing(os.path.join(root_path(), "ct/cdisc/missing"))
    assert hasattr(missing, "_missing_ct")
    assert isinstance(missing._missing_ct, list)


def test_code_lists_iteration():
    """Test that code_lists method yields all entries from the YAML file"""
    missing = Missing(os.path.join(root_path(), "ct/cdisc/missing"))
    code_lists = list(missing.code_lists())
    assert len(code_lists) > 0
    for code_list in code_lists:
        assert isinstance(code_list, dict)
        assert "conceptId" in code_list
        assert "terms" in code_list
        for term in code_list["terms"]:
            assert "preferredTerm" in term
            assert "definition" in term
            assert "submissionValue" in term
            assert "synonyms" in term


# def test_yaml_file_exists():
#     """Test that the missing_ct.yaml file exists in the expected location"""
#     missing = Missing()  # This will raise FileNotFoundError if file doesn't exist
