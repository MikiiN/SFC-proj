from dataclasses import dataclass

from src.fuzzy.features import extract_fuzzy_features
import src.fuzzy.fuzzy_sets as fsets
from src.fuzzy.fuzzy_sets import FuzzyValues, SetsInputValues
from src.fuzzy.rules import Rule


@dataclass
class FuzzyConfiguration:
    centroid_low_center: float
    centroid_low_variance: float
    centroid_medium_center: float
    centroid_medium_variance: float
    centroid_high_center: float
    centroid_high_variance: float
    a_ratio_low_center: float
    a_ratio_low_variance: float
    a_ratio_medium_center: float
    a_ratio_medium_variance: float
    a_ratio_high_center: float
    a_ratio_high_variance: float
    extent_low_center: float
    extent_low_variance: float
    extent_medium_center: float
    extent_medium_variance: float
    extent_high_center: float
    extent_high_variance: float
    solidity_low_center: float
    solidity_low_variance: float
    solidity_medium_center: float
    solidity_medium_variance: float
    solidity_high_center: float
    solidity_high_variance: float
    h_symmetry_low_center: float
    h_symmetry_low_variance: float
    h_symmetry_medium_center: float
    h_symmetry_medium_variance: float
    h_symmetry_high_center: float
    h_symmetry_high_variance: float
    v_symmetry_low_center: float
    v_symmetry_low_variance: float
    v_symmetry_medium_center: float
    v_symmetry_medium_variance: float
    v_symmetry_high_center: float
    v_symmetry_high_variance: float
    holes_low_center: float
    holes_low_variance: float
    holes_medium_center: float
    holes_medium_variance: float
    holes_high_center: float
    holes_high_variance: float
    rule_zero_cfg: list
    rule_one_cfg: list
    rule_two_cfg: list
    rule_three_cfg: list
    rule_four_cfg: list
    rule_five_cfg: list
    rule_six_cfg: list
    rule_seven_cfg: list
    rule_eight_cfg: list
    rule_nine_cfg: list



def classify(img, cfg: FuzzyConfiguration):
    features = extract_fuzzy_features(img)

    sets = []
    centroid = fsets.CentroidSet(
        features.centroid,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.centroid_low_center, cfg.holes_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.centroid_medium_center, cfg.centroid_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.centroid_high_center, cfg.centroid_high_variance
            ),
        }
    )
    sets.append(centroid)

    a_ratio = fsets.AspectRatioSet(
        features.aspect_ratio,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.a_ratio_low_center, cfg.a_ratio_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.a_ratio_medium_center, cfg.a_ratio_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.a_ratio_high_center, cfg.a_ratio_high_variance
            ),
        }
    )
    sets.append(a_ratio)

    extent = fsets.ExtentSet(
        features.extent,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.extent_low_center, cfg.extent_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.extent_medium_center, cfg.extent_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.extent_high_center, cfg.extent_high_variance
            ),
        }
    )
    sets.append(extent)

    solidity = fsets.SoliditySet(
        features.solidity,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.solidity_low_center, cfg.solidity_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.solidity_medium_center, cfg.solidity_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.solidity_high_center, cfg.solidity_high_variance
            ),
        }
    )
    sets.append(solidity)

    h_symmetry = fsets.SymmetrySet(
        features.horizontal_symmetry,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.h_symmetry_low_center, cfg.h_symmetry_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.h_symmetry_medium_center, cfg.h_symmetry_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.h_symmetry_high_center, cfg.h_symmetry_high_variance
            ),
        }
    )
    sets.append(h_symmetry)

    v_symmetry = fsets.SymmetrySet(
        features.vertical_symmetry,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.v_symmetry_low_center, cfg.v_symmetry_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.v_symmetry_medium_center, cfg.v_symmetry_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.v_symmetry_high_center, cfg.v_symmetry_high_variance
            ),
        }
    )
    sets.append(v_symmetry)

    holes = fsets.HolesSet(
        features.holes,
        {
            FuzzyValues.LOW: SetsInputValues(
                cfg.holes_low_center, cfg.holes_low_variance
            ),
            FuzzyValues.MEDIUM: SetsInputValues(
                cfg.holes_medium_center, cfg.holes_medium_variance
            ),
            FuzzyValues.HIGH: SetsInputValues(
                cfg.holes_high_center, cfg.holes_high_variance
            ),
        }
    )
    sets.append(holes)

    rule_zero = Rule.from_list(cfg.rule_zero_cfg)
    rule_one = Rule.from_list(cfg.rule_one_cfg)
    rule_two = Rule.from_list(cfg.rule_two_cfg)
    rule_three = Rule.from_list(cfg.rule_three_cfg)
    rule_four = Rule.from_list(cfg.rule_four_cfg)
    rule_five = Rule.from_list(cfg.rule_five_cfg)
    rule_six = Rule.from_list(cfg.rule_six_cfg)
    rule_seven = Rule.from_list(cfg.rule_seven_cfg)
    rule_eight = Rule.from_list(cfg.rule_eight_cfg)
    rule_nine = Rule.from_list(cfg.rule_nine_cfg)

    results = []
    results.append(rule_zero.eval(*sets))
    results.append(rule_one.eval(*sets))
    results.append(rule_two.eval(*sets))
    results.append(rule_three.eval(*sets))
    results.append(rule_four.eval(*sets))
    results.append(rule_five.eval(*sets))
    results.append(rule_six.eval(*sets))
    results.append(rule_seven.eval(*sets))
    results.append(rule_eight.eval(*sets))
    results.append(rule_nine.eval(*sets))

    choosen_num = results[0]
    for res in results:
        choosen_num = max(res, choosen_num, key=lambda a: a[0])
    
    return choosen_num[1] 
