import enum 
import random

class ErrorTempValues(enum.Enum):
    NEGATIVE_BIG = -15.0
    NEGATIVE_SMALL = -5.0
    ZERO = 0
    POSITIVE_SMALL = 5.0
    POSITIVE_BIG = 15.0



class ErrorFlowValues(enum.Enum):
    NEGATIVE = -0.5
    ZERO = 0
    POSITIVE = 0.5



class ValveChangeValues(enum.Enum):
    NEGATIVE_BIG = -0.05
    NEGATIVE_SMALL = -0.02
    ZERO = 0
    POSITIVE_SMALL = 0.02
    POSITIVE_BIG = 0.05



class FuzzySet:
    def __init__(
            self, 
            value, 
            precise_variance, 
            approximate_variance
    ):
        self.value = value
        self.precise_variance = precise_variance
        self.approximate_variance = approximate_variance

    
    def triangle_function(
        self, 
        value: float, 
        center: float, 
        left: float,
        right: float
    ) -> float:
       lower_bound = center - left
       upper_bound = center + right
       rising = (value - lower_bound) / (center - lower_bound)
       falling = (upper_bound - value) / (upper_bound - center)
       return max(min(rising, falling), 0.0)



class ErrorTempSet(FuzzySet):
    def __init__(self, 
            value, 
            precise_variance = 5.0, 
            approximate_variance = 10.0
    ):
        super().__init__(value, precise_variance, approximate_variance)
        self.mf_values = {
            ErrorTempValues.NEGATIVE_BIG : self.mf_negative_big(),
            ErrorTempValues.NEGATIVE_SMALL : self.mf_negative_small(),
            ErrorTempValues.ZERO : self.mf_zero(),
            ErrorTempValues.POSITIVE_SMALL : self.mf_positive_small(),
            ErrorTempValues.POSITIVE_BIG : self.mf_positive_big()
        } 


    def mf_negative_big(self):
        value = max(ErrorTempValues.NEGATIVE_BIG.value, self.value)
        return self.triangle_function(
            value,
            ErrorTempValues.NEGATIVE_BIG.value,
            self.approximate_variance,
            self.approximate_variance
        )


    def mf_negative_small(self):
        return self.triangle_function(
            self.value,
            ErrorTempValues.NEGATIVE_SMALL.value,
            self.approximate_variance,
            self.precise_variance
        )


    def mf_zero(self):
        return self.triangle_function(
            self.value,
            ErrorTempValues.ZERO.value,
            self.precise_variance,
            self.precise_variance
        )


    def mf_positive_small(self):
        return self.triangle_function(
            self.value,
            ErrorTempValues.POSITIVE_SMALL.value,
            self.precise_variance,
            self.approximate_variance
        )


    def mf_positive_big(self):
        value = min(ErrorTempValues.POSITIVE_BIG.value, self.value)
        return self.triangle_function(
            value,
            ErrorTempValues.POSITIVE_BIG.value,
            self.approximate_variance,
            self.approximate_variance
        )
    


class ErrorFlowSet(FuzzySet):
    def __init__(self, 
            value, 
            precise_variance = 0.5, 
            approximate_variance = 1.0
    ):
        super().__init__(value, precise_variance, approximate_variance)
        self.mf_values = {
            ErrorFlowValues.NEGATIVE : self.mf_negative(),
            ErrorFlowValues.ZERO : self.mf_zero(),
            ErrorFlowValues.POSITIVE : self.mf_positive()
        } 

    
    def mf_negative(self):
        value = max(ErrorFlowValues.NEGATIVE.value, self.value)
        return self.triangle_function(
            value,
            ErrorFlowValues.NEGATIVE.value,
            self.approximate_variance,
            self.approximate_variance
        )


    def mf_zero(self):
        return self.triangle_function(
            self.value,
            ErrorFlowValues.ZERO.value,
            self.precise_variance,
            self.precise_variance
        )


    def mf_positive(self):
        value = min(ErrorFlowValues.POSITIVE.value, self.value)
        return self.triangle_function(
            value,
            ErrorFlowValues.POSITIVE.value,
            self.approximate_variance,
            self.approximate_variance
        )
    


class ValveChangeSet:
    def __init__(self, 
            precise_variance = 0.05, 
            approximate_variance = 0.1,
            negative_big_limits = [-1.0],
            negative_small_limits = [-1.0],
            zero_limits = [-1.0],
            positive_small_limits = [-1.0],
            positive_big_limits = [-1.0]
    ):
        self.precise_variance = precise_variance
        self.approximate_variance = approximate_variance
        self.limits = {
            ValveChangeValues.NEGATIVE_BIG : max(negative_big_limits),
            ValveChangeValues.NEGATIVE_SMALL : max(negative_small_limits),
            ValveChangeValues.ZERO : max(zero_limits),
            ValveChangeValues.POSITIVE_SMALL : max(positive_small_limits),
            ValveChangeValues.POSITIVE_BIG : max(positive_big_limits)
        }


    def mf_result(self, value):
        return max(
            self.mf_negative_big(value),
            self.mf_negative_small(value),
            self.mf_zero(value),
            self.mf_positive_small(value),
            self.mf_positive_big(value)
        )
    

    def triangle_function(
        self, 
        value: float, 
        center: float, 
        left: float,
        right: float
    ) -> float:
        lower_bound = center - left
        upper_bound = center + right
        rising = (value - lower_bound) / (center - lower_bound)
        falling = (upper_bound - value) / (upper_bound - center)
        return max(min(rising, falling), 0.0)


    def mf_negative_big(self, value):
        res = self.triangle_function(
            value,
            ValveChangeValues.NEGATIVE_BIG.value,
            self.approximate_variance,
            self.approximate_variance
        )
        return min(self.limits[ValveChangeValues.NEGATIVE_BIG], res)


    def mf_negative_small(self, value):
        res = self.triangle_function(
            value,
            ValveChangeValues.NEGATIVE_SMALL.value,
            self.approximate_variance,
            self.precise_variance
        )
        return min(self.limits[ValveChangeValues.NEGATIVE_SMALL], res)


    def mf_zero(self, value):
        res = self.triangle_function(
            value,
            ValveChangeValues.ZERO.value,
            self.precise_variance,
            self.precise_variance
        )
        return min(self.limits[ValveChangeValues.ZERO], res)


    def mf_positive_small(self, value):
        res = self.triangle_function(
            value,
            ValveChangeValues.POSITIVE_SMALL.value,
            self.precise_variance,
            self.approximate_variance
        )
        return min(self.limits[ValveChangeValues.POSITIVE_SMALL], res)


    def mf_positive_big(self, value):
        res = self.triangle_function(
            value,
            ValveChangeValues.POSITIVE_BIG.value,
            self.approximate_variance,
            self.approximate_variance
        ) 
        return min(self.limits[ValveChangeValues.POSITIVE_BIG], res)
    


def generate_random_rules():
    rules = []
    values = [
        ValveChangeValues.NEGATIVE_BIG,
        ValveChangeValues.NEGATIVE_SMALL,
        ValveChangeValues.ZERO,
        ValveChangeValues.POSITIVE_SMALL,
        ValveChangeValues.POSITIVE_BIG
    ]
    for _ in range(15):
        rules.append((
            random.sample(values, 1)[0], random.sample(values, 1)[0]
        ))
    return rules