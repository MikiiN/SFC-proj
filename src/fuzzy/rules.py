from dataclasses import dataclass
from enum import Enum

import src.fuzzy.fuzzy_sets as fsets
from src.fuzzy.fuzzy_sets import FuzzySet, FuzzyValues


class Condition:
    def __init__(self, set: FuzzySet, value: FuzzyValues):
        self.set = set
        self.value = value
        self.bound = set.get_upper_bound(value)



class Rule:
    DEFAULT_VALUE = FuzzyValues.IRRELEVANT

    def __init__(
        self,
        result_number: int,
        centroid: FuzzyValues = DEFAULT_VALUE,
        aspect_ratio: FuzzyValues = DEFAULT_VALUE,
        extent: FuzzyValues = DEFAULT_VALUE,
        solidity: FuzzyValues = DEFAULT_VALUE,
        h_symmetry: FuzzyValues = DEFAULT_VALUE,
        v_symmetry: FuzzyValues = DEFAULT_VALUE,
        holes: FuzzyValues = DEFAULT_VALUE
    ):
        self.result_number = result_number
        self.conditions = [
            centroid,
            aspect_ratio,
            extent,
            solidity,
            h_symmetry,
            v_symmetry,
            holes
        ]

    
    def eval(
        self,
        centroid: fsets.CentroidSet,
        aspect_ratio: fsets.AspectRatioSet,
        extent: fsets.ExtentSet,
        solidity: fsets.SoliditySet,
        h_symmetry: fsets.SymmetrySet,
        v_symmetry: fsets.SymmetrySet,
        holes: fsets.HoleSet
    ):
        set_list = [
            centroid,
            aspect_ratio,
            extent,
            solidity,
            h_symmetry,
            v_symmetry,
            holes
        ]
        result = centroid.get_upper_bound(self.conditions[0])
        for (set, value) in zip(set_list, self.conditions):
            result = min(
                set.get_upper_bound(value),
                result
            )
        return (result, self.result_number)

    
    @classmethod
    def from_string(cls, string: str):
        parts = string.split(",")
        result_number = parts[-1:][0]
        parts = parts[:-1]
        conditions = []
        for con in parts:
            conditions.append(fsets.FuzzyValues.from_string(con))
        return cls(result_number, *conditions)
        


    def __str__(self):
        string = ""
        for cond in self.conditions:
            string += f"{str(cond)},"
        string += str(self.result_number)
