from typing import List, Literal, Union
from .api_base_model import ApiBaseModelNameLabelDesc
from .quantity import Quantity
from .agent_administration import AgentAdministration
from .code import Code


class StudyIntervention(ApiBaseModelNameLabelDesc):
    role: Code
    type: Code
    minimumResponseDuration: Union[Quantity, None] = None
    codes: List[Code] = []
    administrations: List[AgentAdministration] = []
    productDesignation: Code
    pharmacologicClass: Union[Code, None] = None
    instanceType: Literal["StudyIntervention"]
