import numpy as np 

from enum import Enum

class MeanIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=13
        HIGH=25

    def __init__(self, value, variance=5):
        self.low = self.low_mean_intensity_mf(value)
        self.medium = self.medium_mean_intensity_mf(value)
        self.high = self.high_mean_intensity_mf(value)
        self.VARIANCE = variance

    
    def low_mean_intensity_mf(self, value):
        if value < self.Values.LOW or value >= self.Values.MEDIUM:
            return 0.0
        return np.exp(-(((value-self.Values.LOW)**2)/(2*self.VARIANCE**2)))


    def medium_mean_intensity_mf(self, value):
        if value < self.Values.LOW or value > self.Values.HIGH:
            return 0.0
        return np.exp(-(((value-self.Values.MEDIUM)**2)/(2*self.VARIANCE**2)))
    

    def high_mean_intensity_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        return np.exp(-(((value-self.Values.HIGH)**2)/(2*self.VARIANCE**2)))



class StdIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=13
        HIGH=25

    def __init__(self, value, variance=5):
        self.low = self.low_std_intensity_mf(value)
        self.medium = self.medium_std_intensity_mf(value)
        self.high = self.high_std_intensity_mf(value)
        self.VARIANCE = variance

    
    def low_std_intensity_mf(self, value):
        if value < self.Values.LOW or value > self.Values.MEDIUM:
            return 0.0
        return np.exp(-(((value-self.Values.LOW)**2)/(2*self.VARIANCE**2)))


    def medium_std_intensity_mf(self, value):
        if value < self.Values.LOW or value > self.Values.HIGH:
            return 0.0
        return np.exp(-(((value-self.Values.MEDIUM)**2)/(2*self.VARIANCE**2)))
    

    def high_std_intensity_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        return np.exp(-(((value-self.Values.HIGH)**2)/(2*self.VARIANCE**2)))



class AspectRatioSet:
    class Values(Enum):
        BIGGER_HEIGH=0
        SAME=1
        BIGGER_WIDTH=2


    def __init__(self, value, variance=0.5):
        self.low = self.bigger_heigh_mf(value)
        self.medium = self.same_mf(value)
        self.high = self.bigger_width_mf(value)
        self.VARIANCE = variance


    def bigger_heigh_mf(self, value):
        if value < self.Values.BIGGER_HEIGH or value >= self.Values.SAME:
            return 0.0
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def same_mf(self, value):
        if value < self.Values.BIGGER_HEIGH or value > self.Values.BIGGER_WIDTH:
            return 0.0
        center = self.Values.SAME
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def bigger_width_mf(self, value):
        if value < self.Values.SAME or value > self.Values.BIGGER_WIDTH:
            return 0.0
        center = self.Values.BIGGER_WIDTH
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))



class ZoneIntensitySet:
    class Values(Enum):
        LOW=0
        MEDIUM=13
        HIGH=25

    def __init__(self, value, variance=5):
        self.low = self.low_mean_intensity_mf(value)
        self.medium = self.medium_mean_intensity_mf(value)
        self.high = self.high_mean_intensity_mf(value)
        self.VARIANCE = variance

    
    def low_mean_intensity_mf(self, value):
        if value < self.Values.LOW or value >= self.Values.MEDIUM:
            return 0.0
        return np.exp(-(((value-self.Values.LOW)**2)/(2*self.VARIANCE**2)))


    def medium_mean_intensity_mf(self, value):
        if value < self.Values.LOW or value > self.Values.HIGH:
            return 0.0
        return np.exp(-(((value-self.Values.MEDIUM)**2)/(2*self.VARIANCE**2)))
    

    def high_mean_intensity_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        return np.exp(-(((value-self.Values.HIGH)**2)/(2*self.VARIANCE**2)))



class SymmetrySet:
    class Values(Enum):
        LOW=0
        MEDIUM=0.5
        HIGH=1


    def __init__(self, value, variance=0.5):
        self.low = self.low_mf(value)
        self.medium = self.medium_mf(value)
        self.high = self.high_mf(value)
        self.VARIANCE = variance


    def low_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def medium_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        center = self.Values.MEDIUM
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def high_mf(self, value):
        if value < self.Values.MEDIUM or value > self.Values.HIGH:
            return 0.0 
        center = self.Values.HIGH
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))



# class ProjectionVarianceSet:
#     class Values(Enum):
#         LOW=0
#         MEDIUM=1
#         HIGH=2

#     def __init__(self, value):
#         pass



class LoopSet:
    class Values(Enum):
        ZERO=0
        ONE=1
        TWO=2
    

    def __init__(self, value, variance=0.5):
        self.zero = self.zero_mf(value)
        self.one = self.one_mf(value)
        self.two = self.two_mf(value)
        self.VARIANCE = variance


    def zero_mf(self, value):
        if value < self.Values.ZERO or value > self.Values.ONE:
            return 0.0 
        return np.exp(-((value**2)/(2*self.VARIANCE**2)))


    def one_mf(self, value):
        if value < self.Values.ZERO or value > self.Values.TWO:
            return 0.0 
        center = self.Values.ONE
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))
    

    def two_mf(self, value):
        if value < self.Values.ONE or value > self.Values.TWO:
            return 0.0 
        center = self.Values.TWO
        return np.exp(-(((value-center)**2)/(2*self.VARIANCE**2)))