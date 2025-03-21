from typing import List, Literal
from .alias_code import AliasCode
from .api_base_model import ApiBaseModelNameLabel
from .response_code import ResponseCode


class BiomedicalConceptProperty(ApiBaseModelNameLabel):
    isRequired: bool
    isEnabled: bool
    datatype: str
    responseCodes: List[ResponseCode] = []
    code: AliasCode
    instanceType: Literal["BiomedicalConceptProperty"]
