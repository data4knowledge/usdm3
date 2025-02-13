from typing import Union, List, Literal
from .api_base_model import ApiBaseModelNameLabelDesc
from .code import Code
from .range import Range
from .eligibility_criterion import EligibilityCriterion
from .characteristic import Characteristic


class PopulationDefinition(ApiBaseModelNameLabelDesc):
    includesHealthySubjects: bool
    plannedEnrollmentNumber: Union[Range, None] = None
    plannedCompletionNumber: Union[Range, None] = None
    plannedSex: List[Code] = []
    criteria: List[EligibilityCriterion]
    plannedAge: Union[Range, None] = None
    instanceType: Literal["PopulationDefinition"]


class StudyCohort(PopulationDefinition):
    characteristics: List[Characteristic] = []
    instanceType: Literal["StudyCohort"]


class StudyDesignPopulation(PopulationDefinition):
    cohorts: List[StudyCohort] = []
    instanceType: Literal["StudyDesignPopulation"]
