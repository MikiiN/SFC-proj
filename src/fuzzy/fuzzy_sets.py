import numpy as np 
from dataclasses import dataclass

@dataclass
class SetsInputValues:
    value: float = 0.0
    variance: float = 0.0
    lower_bound: float = 0.0
    upper_bound: float = 0.0



class FuzzySet:
    def __init__(self, value, sets_values: dict[SetsInputValues]):
        self.sets_values = sets_values
        self.mf_values = {}
        for name, set_val in self.sets_values.items():
            self.mf_values[name] = self.membership_function(
                value,
                set_val.value,
                set_val.variance,
                set_val.lower_bound,
                set_val.upper_bound
            )

    
    def membership_function(
        self, 
        value: float, 
        center: float, 
        variance: float,
        lower_bound: float,
        upper_bound: float
    ) -> float:
        if value < lower_bound or value > upper_bound:
            return 0.0
        return np.exp(-(((value-center)**2)/(2*variance**2)))



class MeanIntensitySet(FuzzySet):
    DEFAULT_VALUES = {
        "low": SetsInputValues(0, 5, 0, 13),
        "medium": SetsInputValues(13, 5, 0, 25),
        "high": SetsInputValues(25, 5, 13, 25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class StdIntensitySet(FuzzySet):
    DEFAULT_VALUES = {
        "low": SetsInputValues(0, 5, 0, 13),
        "medium": SetsInputValues(13, 5, 0, 25),
        "high": SetsInputValues(25, 5, 13, 25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class AspectRatioSet(FuzzySet):
    DEFAULT_VALUES = {
        "bigger_heigh": SetsInputValues(0, 0.5, 0, 1),
        "same": SetsInputValues(1, 0.5, 0, 2),
        "bigger_width": SetsInputValues(2, 0.5, 1, 2)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class ZoneIntensitySet(FuzzySet):
    DEFAULT_VALUES = {
        "low": SetsInputValues(0, 5, 0, 13),
        "medium": SetsInputValues(13, 5, 0, 25),
        "high": SetsInputValues(25, 5, 13, 25)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class SymmetrySet(FuzzySet):
    DEFAULT_VALUES = {
        "low": SetsInputValues(0, 0.25, 0, 0.5),
        "medium": SetsInputValues(0.5, 0.25, 0, 1),
        "high": SetsInputValues(1, 0.25, 0.5, 1)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class LoopSet(FuzzySet):
    DEFAULT_VALUES = {
        "low": SetsInputValues(0, 0.5, 0, 1),
        "medium": SetsInputValues(1, 0.5, 0, 2),
        "high": SetsInputValues(2, 0.5, 1, 2)
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)



class NumberSet(FuzzySet):
    DEFAULT_VALUES = {
        0: SetsInputValues(0, 0.5, 0, 1),
        1: SetsInputValues(1, 0.5, 0, 2),
        2: SetsInputValues(2, 0.5, 1, 3),
        3: SetsInputValues(3, 0.5, 2, 4),
        4: SetsInputValues(4, 0.5, 3, 5),
        5: SetsInputValues(5, 0.5, 4, 6),
        6: SetsInputValues(6, 0.5, 5, 7),
        7: SetsInputValues(7, 0.5, 6, 8),
        8: SetsInputValues(8, 0.5, 7, 9),
        9: SetsInputValues(9, 0.5, 8, 9),
    }


    def __init__(self, value, sets_values: dict[SetsInputValues] = DEFAULT_VALUES):
        super().__init__(value, sets_values)