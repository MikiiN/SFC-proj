from dataclasses import dataclass
from enum import Enum

from src.fuzzy.fuzzy_sets import FuzzySet

@dataclass
class Condition:
    feature: FuzzySet = None
    value: str = ""



class LogicOperator(Enum):
    AND = 0
    OR = 1



class Rule:
    def __init__(self, conditions: list, result: int):
        self.conditions = conditions
        self.result = result