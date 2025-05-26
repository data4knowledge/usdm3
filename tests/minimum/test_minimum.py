import os
import pathlib
from src.usdm3.minimum.minimum import Minimum
from src.usdm3.__version__ import __package_version__


def root_path():
    base = pathlib.Path(__file__).parent.parent.parent.resolve()
    return os.path.join(base, "src/usdm3")


def test_init():
    root = root_path()
    # print(f"ROOT: {root}")
    instance = Minimum.minimum(root, "Test Study", "SPONSOR-1234", "1.0.0")
    instance.study.id = "88888888-4444-4444-4444-121212121212"  # UUID is dynamic
    assert instance.model_dump() == {
        "id": "Wrapper_1",
        "study": {
            "description": "",
            "documentedBy": {
                "description": "The study protocol document",
                "id": "StudyProtocolDocument_1",
                "instanceType": "StudyProtocolDocument",
                "label": "Study Protocol",
                "name": "PROTOCOL",
                "versions": [
                    {
                        "childIds": [],
                        "contents": [],
                        "dateValues": [],
                        "id": "StudyProtocolDocumentVersion_1",
                        "instanceType": "StudyProtocolDocumentVersion",
                        "protocolStatus": {
                            "code": "C25425",
                            "codeSystem": "cdisc.org",
                            "codeSystemVersion": "2024-09-27",
                            "decode": "Approved",
                            "id": "Code_3",
                            "instanceType": "Code",
                        },
                        "protocolVersion": "1.0.0",
                    },
                ],
            },
            "id": "88888888-4444-4444-4444-121212121212",
            "instanceType": "Study",
            "label": "",
            "name": "Study",
            "versions": [
                {
                    "amendments": [],
                    "businessTherapeuticAreas": [],
                    "dateValues": [],
                    "documentVersionId": "StudyProtocolDocumentVersion_1",
                    "id": "StudyVersion_1",
                    "instanceType": "StudyVersion",
                    "rationale": "To be provided",
                    "studyDesigns": [],
                    "studyIdentifiers": [
                        {
                            "id": "StudyIdentifier_1",
                            "instanceType": "StudyIdentifier",
                            "studyIdentifier": "SPONSOR-1234",
                            "studyIdentifierScope": {
                                "id": "Organization_1",
                                "identifier": "To be provided",
                                "identifierScheme": "To be provided",
                                "instanceType": "Organization",
                                "label": None,
                                "legalAddress": None,
                                "name": "Sponsor",
                                "organizationType": {
                                    "code": "C70793",
                                    "codeSystem": "cdisc.org",
                                    "codeSystemVersion": "2024-09-27",
                                    "decode": "Clinical Study Sponsor",
                                    "id": "Code_2",
                                    "instanceType": "Code",
                                },
                            },
                        },
                    ],
                    "studyPhase": None,
                    "studyType": None,
                    "titles": [
                        {
                            "id": "StudyTitle_1",
                            "instanceType": "StudyTitle",
                            "text": "Test Study",
                            "type": {
                                "code": "C207616",
                                "codeSystem": "cdisc.org",
                                "codeSystemVersion": "2024-09-27",
                                "decode": "Official Study Title",
                                "id": "Code_1",
                                "instanceType": "Code",
                            },
                        },
                    ],
                    "versionIdentifier": "1",
                },
            ],
        },
        "systemName": "Python USDM3 Package",
        "systemVersion": __package_version__,
        "usdmVersion": "3.0.0",
    }
