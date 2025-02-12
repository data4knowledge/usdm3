from typing import List, Literal, Union
from .api_base_model import ApiBaseModelNameLabelDesc
from .code import Code
from .transition_rule import TransitionRule


class Encounter(ApiBaseModelNameLabelDesc):
    type: Code
    previousId: Union[str, None] = None
    nextId: Union[str, None] = None
    scheduledAtId: Union[str, None] = None
    environmentalSetting: List[Code] = []
    contactModes: List[Code] = []
    transitionStartRule: Union[TransitionRule, None] = None
    transitionEndRule: Union[TransitionRule, None] = None
    instanceType: Literal["Encounter"]
