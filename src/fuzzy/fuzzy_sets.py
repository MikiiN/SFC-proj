import numpy as np 
from dataclasses import dataclass
from enum import Enum


@dataclass
class SetsInputValues:
    center: float = 0.0
    variance: float = 0.0



class FuzzyValues(Enum):
    IRRELEVANT= -1
    LOW = 0
    MEDIUM = 1
    HIGH = 2


    @classmethod
    def from_string(cls, value: str):
        value = value.replace(" ", "")
        return cls(int(value))
          

    def __str__(self):
        return self.value   



class FuzzySet:
    def __init__(self, value, sets_values: dict[SetsInputValues]):
        self.sets_values = sets_values
        self.mf_values = {}
        self.mf_params = {}
        for name, set_val in self.sets_values.items():
            v = FuzzyValues.from_string(name)
            self.mf_values[v] = self.membership_function(
                value,
                set_val.center,
                set_val.variance
            )
            self.mf_params[v] = set_val

    
    def get_upper_bound(self, value: FuzzyValues):
        return self.mf_values[value]

    
    def membership_function(
        self, 
        value: float, 
        center: float, 
        variance: float,
    ) -> float:
       lower_bound = center - variance
       upper_bound = center + variance
       rising = (value - lower_bound) / (center - lower_bound)
       falling = (upper_bound - value) / (upper_bound - center)
       return max(min(rising, falling), 0.0)



class CentroidSet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.25),
        FuzzyValues.MEDIUM: SetsInputValues(0.5, 0.25),
        FuzzyValues.HIGH: SetsInputValues(1, 0.25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class AspectRatioSet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.25),
        FuzzyValues.MEDIUM: SetsInputValues(0.5, 0.25),
        FuzzyValues.HIGH: SetsInputValues(1, 0.25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class ExtentSet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.25),
        FuzzyValues.MEDIUM: SetsInputValues(0.5, 0.25),
        FuzzyValues.HIGH: SetsInputValues(1, 0.25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class SoliditySet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.25),
        FuzzyValues.MEDIUM: SetsInputValues(0.5, 0.25),
        FuzzyValues.HIGH: SetsInputValues(1, 0.25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class SymmetrySet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.25),
        FuzzyValues.MEDIUM: SetsInputValues(0.5, 0.25),
        FuzzyValues.HIGH: SetsInputValues(1, 0.25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class HolesSet(FuzzySet):
    DEFAULT_VALUES = {
        FuzzyValues.LOW: SetsInputValues(0, 0.5),
        FuzzyValues.MEDIUM: SetsInputValues(1, 0.5),
        FuzzyValues.HIGH: SetsInputValues(2, 0.5)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class NumberSet(FuzzySet):
    DEFAULT_VALUES = {
        0: SetsInputValues(0, 0.5),
        1: SetsInputValues(1, 0.5),
        2: SetsInputValues(2, 0.5),
        3: SetsInputValues(3, 0.5),
        4: SetsInputValues(4, 0.5),
        5: SetsInputValues(5, 0.5),
        6: SetsInputValues(6, 0.5),
        7: SetsInputValues(7, 0.5),
        8: SetsInputValues(8, 0.5),
        9: SetsInputValues(9, 0.5)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)