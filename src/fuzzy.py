import numpy as np
from src.fuzzy_set import *


def eval_rule(hot_valve, cold_valve, first, *rest):
    result = first
    for condition in rest:
        result = min(result, condition)
    return (result, hot_valve, cold_valve)


def append_limits(rule, hot_limits: dict, cold_limits: dict):
    if not rule[1] in hot_limits.keys():
        hot_limits[rule[1]] = [rule[0]]
    else: 
        hot_limits[rule[1]].append(rule[0])
    if not rule[2] in cold_limits.keys():
        cold_limits[rule[2]] = [rule[0]]
    else:
        cold_limits[rule[2]].append(rule[0])
    return hot_limits, cold_limits


def fuzzification(
        current_temperature_error, 
        current_flow_error,
        temp_precise_variance = 5.0,
        temp_approximate_variance = 10.0,
        flow_precise_variance = 0.5,
        flow_approximate_variance = 1.0,
        change_precise_variance = 0.05,
        change_approximate_variance = 0.1
    ):
    temp_set = ErrorTempSet(
        current_temperature_error,
        temp_precise_variance,
        temp_approximate_variance
    )
    flow_set = ErrorFlowSet(
        current_flow_error,
        flow_precise_variance,
        flow_approximate_variance
    )
    hot_limits = {}
    cold_limits = {}

    # if temperature is PB and flow is ZE then hot_valve is NB and cold_valve is PB 
    rule0 = eval_rule(
        ValveChangeValues.NEGATIVE_BIG,
        ValveChangeValues.POSITIVE_BIG,
        temp_set.mf_values[ErrorTempValues.POSITIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.ZERO]
    )
    hot_limits, cold_limits = append_limits(rule0, hot_limits, cold_limits)

    # if temperature is PS and flow is ZE then hot_valve is NS and cold_valve is PS
    rule1 = eval_rule(
        ValveChangeValues.NEGATIVE_SMALL,
        ValveChangeValues.POSITIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.POSITIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.ZERO]
    )
    hot_limits, cold_limits = append_limits(rule1, hot_limits, cold_limits)

    # if temperature is ZE and flow is ZE then hot_valve is ZE and cold_valve is ZE
    rule2 = eval_rule(
        ValveChangeValues.ZERO,
        ValveChangeValues.ZERO,
        temp_set.mf_values[ErrorTempValues.ZERO],
        flow_set.mf_values[ErrorFlowValues.ZERO]
    )
    hot_limits, cold_limits = append_limits(rule2, hot_limits, cold_limits)

    # if temperature is NS and flow is ZE then hot_valve is PS and cold_valve is NS
    rule3 = eval_rule(
        ValveChangeValues.POSITIVE_SMALL,
        ValveChangeValues.NEGATIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.ZERO]
    )
    hot_limits, cold_limits = append_limits(rule3, hot_limits, cold_limits)

    # if temperature is NB and flow is N then hot_valve is PB and cold_valve is NB
    rule4 = eval_rule(
        ValveChangeValues.POSITIVE_BIG,
        ValveChangeValues.NEGATIVE_BIG,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.ZERO]
    )
    hot_limits, cold_limits = append_limits(rule4, hot_limits, cold_limits)

    # if temperature is PB and flow is N then hot_valve is NS and cold_valve is PB 
    rule5 = eval_rule(
        ValveChangeValues.NEGATIVE_SMALL,
        ValveChangeValues.POSITIVE_BIG,
        temp_set.mf_values[ErrorTempValues.POSITIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.NEGATIVE]
    )
    hot_limits, cold_limits = append_limits(rule5, hot_limits, cold_limits)

    # if temperature is PS and flow is N then hot_valve is ZE and cold_valve is PB
    rule6 = eval_rule(
        ValveChangeValues.ZERO,
        ValveChangeValues.POSITIVE_BIG,
        temp_set.mf_values[ErrorTempValues.POSITIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.NEGATIVE]
    )
    hot_limits, cold_limits = append_limits(rule6, hot_limits, cold_limits)

    # if temperature is ZE and flow is N then hot_valve is ZE and cold_valve is ZE
    rule7 = eval_rule(
        ValveChangeValues.POSITIVE_SMALL,
        ValveChangeValues.POSITIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.ZERO],
        flow_set.mf_values[ErrorFlowValues.NEGATIVE]
    )
    hot_limits, cold_limits = append_limits(rule7, hot_limits, cold_limits)

    # if temperature is NS and flow is N then hot_valve is PS and cold_valve is ZE
    rule8 = eval_rule(
        ValveChangeValues.POSITIVE_BIG,
        ValveChangeValues.ZERO,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.NEGATIVE]
    )
    hot_limits, cold_limits = append_limits(rule8, hot_limits, cold_limits)

    # if temperature is NB and flow is N then hot_valve is PB and cold_valve is NS
    rule9 = eval_rule(
        ValveChangeValues.POSITIVE_BIG,
        ValveChangeValues.NEGATIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.NEGATIVE]
    )
    hot_limits, cold_limits = append_limits(rule9, hot_limits, cold_limits)

    # if temperature is PB and flow is P then hot_valve is NB and cold_valve is PS 
    rule10 = eval_rule(
        ValveChangeValues.NEGATIVE_BIG,
        ValveChangeValues.POSITIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.POSITIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.POSITIVE]
    )
    hot_limits, cold_limits = append_limits(rule10, hot_limits, cold_limits)

    # if temperature is PS and flow is P then hot_valve is NB and cold_valve is ZE
    rule11 = eval_rule(
        ValveChangeValues.NEGATIVE_BIG,
        ValveChangeValues.ZERO,
        temp_set.mf_values[ErrorTempValues.POSITIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.POSITIVE]
    )
    hot_limits, cold_limits = append_limits(rule11, hot_limits, cold_limits)

    # if temperature is ZE and flow is P then hot_valve is PS and cold_valve is PS
    rule12 = eval_rule(
        ValveChangeValues.POSITIVE_SMALL,
        ValveChangeValues.POSITIVE_SMALL,
        temp_set.mf_values[ErrorTempValues.ZERO],
        flow_set.mf_values[ErrorFlowValues.POSITIVE]
    )
    hot_limits, cold_limits = append_limits(rule12, hot_limits, cold_limits)

    # if temperature is NS and flow is P then hot_valve is ZE and cold_valve is NB
    rule13 = eval_rule(
        ValveChangeValues.ZERO,
        ValveChangeValues.NEGATIVE_BIG,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_SMALL],
        flow_set.mf_values[ErrorFlowValues.POSITIVE]
    )
    hot_limits, cold_limits = append_limits(rule13, hot_limits, cold_limits)

    # if temperature is NB and flow is P then hot_valve is PS and cold_valve is NB
    rule14 = eval_rule(
        ValveChangeValues.POSITIVE_SMALL,
        ValveChangeValues.NEGATIVE_BIG,
        temp_set.mf_values[ErrorTempValues.NEGATIVE_BIG],
        flow_set.mf_values[ErrorFlowValues.POSITIVE]
    )
    hot_limits, cold_limits = append_limits(rule14, hot_limits, cold_limits)

    hot_change_set = ValveChangeSet(
        change_precise_variance,
        change_approximate_variance,
        hot_limits[ValveChangeValues.NEGATIVE_BIG],
        hot_limits[ValveChangeValues.NEGATIVE_SMALL],
        hot_limits[ValveChangeValues.ZERO],
        hot_limits[ValveChangeValues.POSITIVE_SMALL],
        hot_limits[ValveChangeValues.POSITIVE_BIG]
    )
    cold_change_set = ValveChangeSet(
        change_precise_variance,
        change_approximate_variance,
        cold_limits[ValveChangeValues.NEGATIVE_BIG],
        cold_limits[ValveChangeValues.NEGATIVE_SMALL],
        cold_limits[ValveChangeValues.ZERO],
        cold_limits[ValveChangeValues.POSITIVE_SMALL],
        cold_limits[ValveChangeValues.POSITIVE_BIG]
    )
    return hot_change_set, cold_change_set


def defuzzification(change_set: ValveChangeSet):
    sum_vals = 0.0
    sum_weights = 0.0
    for w in np.arange(ValveChangeValues.NEGATIVE_BIG.value, ValveChangeValues.POSITIVE_BIG.value, 0.01):
        sum_vals += w * change_set.mf_result(w)
        sum_weights += change_set.mf_result(w)
    return sum_vals/sum_weights
