from src.fuzzy import fuzzification, defuzzification
from src.simulation import Simulator
from src.generic_algorithm import Population


WANTED_FLOW = 0.8
WANTED_TEMP = 38.0

sim = Simulator()
flow, temp = sim.step(0, 0.5, 0.5)
error_flow = flow - WANTED_FLOW
error_temp = temp - WANTED_TEMP

hot, cold = fuzzification(error_temp, error_flow)
hot_change = defuzzification(hot)
cold_change = defuzzification(cold)
print(hot_change, cold_change)

pop = Population(100)
best = pop.run(100)
print(best)