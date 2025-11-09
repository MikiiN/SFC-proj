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
        BIGGER_HEIGH=0
        SAME=1
        BIGGER_WIDTH=2

    VARIANCE = 0.5

    def __init__(self, value):
        self.low = self.bigger_heigh_mf(value)
        self.medium = self.same_mf(value)
        self.high = self.bigger_width_mf(value)


    def bigger_heigh_mf(self, value):
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def same_mf(self, value):
        center = self.Values.SAME
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def bigger_width_mf(self, value):
        center = self.Values.BIGGER_WIDTH
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))



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



class ProjectionVarianceSet:
    class Values(Enum):
        LOW=0
        MEDIUM=1
        HIGH=2

    def __init__(self, value):
        pass



class LoopSet:
    class Values(Enum):
        ZERO=0
        ONE=1
        TWO=2

    VARIANCE = 0.5

    def __init__(self, value):
        self.zero = self.zero_mf(value)
        self.one = self.one_mf(value)
        self.two = self.two_mf(value)


    def zero_mf(self, value):
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def one_mf(self, value):
        center = self.Values.ONE
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def two_mf(self, value):
        center = self.Values.TWO
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))