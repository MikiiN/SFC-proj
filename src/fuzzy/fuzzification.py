import numpy as np 

from enum import Enum

class MeanIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass



class StdIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass



class AspectRatioSet:
    class Values(Enum):
        BIGGER_WIDTH=0
        SAME=1
        BIGGER_HEIGH=2

    def __init__(self, value):
        pass



class ZoneIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass



class SymmetrySet:
    class Values(Enum):
        LOW=0
        MEDIUM=0.5
        HIGH=1

    VARIANCE = 0.5

    def __init__(self, value):
        self.low = self.low_mf(value)
        self.medium = self.medium_mf(value)
        self.high = self.high_mf(value)


    def low_mf(self, value):
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def medium_mf(self, value):
        center = self.Values.MEDIUM
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def high_mf(self, value):
        center = self.Values.HIGH
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))



class VerticalProjectionVarianceSet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass



class HorizontalProjectionVarianceSet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass
