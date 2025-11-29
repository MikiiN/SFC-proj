from src.fuzzy import fuzzification, defuzzification
from src.simulation import Simulator
from src.generic_algorithm import Population


WANTED_FLOW = 0.8
WANTED_TEMP = 38.0

# sim = Simulator()
# flow, temp = sim.step(0, 0.5, 0.5)
# error_flow = flow - WANTED_FLOW
# error_temp = temp - WANTED_TEMP

# hot, cold = fuzzification(error_temp, error_flow)
# hot_change = defuzzification(hot)
# cold_change = defuzzification(cold)
# print(hot_change, cold_change)


def test_rules(rules = None):
    hot_valve = 0.2
    cold_valve = 0.4
    temperatures = []
    flows = []
    sim = Simulator(start_fault_time=40, end_fault_time=50)
    for t in range(100):
        current_flow, current_temp = sim.step(t, hot_valve, cold_valve)
        error_temp = current_temp - WANTED_TEMP
        error_flow = current_flow - WANTED_FLOW
        if rules != None:
            hot_set, cold_set = fuzzification(
                error_temp,
                error_flow,
                rules = rules
            )
        else:
            hot_set, cold_set = fuzzification(
                error_temp,
                error_flow
            )
        hot_change = defuzzification(hot_set)
        cold_change = defuzzification(cold_set)

        hot_valve += hot_change
        cold_valve += cold_change
        temperatures.append(float(current_temp))
        flows.append(float(current_flow))
    return temperatures, flows


pop = Population(40)
best = pop.run(50, True)
print(best[1].rules)

# results_def = test_rules()
results_opt = test_rules(best[1].rules)

# print(results_def[0])
# print(results_def[1])
print(results_opt[0])
print(results_opt[1])


# import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-o", "--optimize", action="store_true", required=False)
# parser.add_argument("-l", "--load", required=False)

# args = parser.parse_args()