import random

from src.fuzzy import fuzzification, defuzzification
from src.fuzzy_set import ValveChangeValues
from src.simulation import Simulator

class Chromosome:
    def __init__(self, rules):
        self.rules = rules
        self.score = None


    def get_score(self):
        if self.score == None:
            self.score = self._eval()
        return self.score


    def to_list(self):
        rules_list = []
        for rule in self.rules:
            rules_list.append((rule[0].value, rule[1].value))
        return rules_list
    

    @classmethod
    def from_list(cls, rule_list: list[tuple[float, float]]):
        rules = []
        for first, second in rule_list:
            rules.append(
                (ValveChangeValues(first), ValveChangeValues(second)) 
            )
        return cls(rules)

    
    def _eval(self):
        target_temp = 38.0
        target_flow = 0.8
        hot_valve = 0.5
        cold_valve = 0.5

        total_error = 0.0
        sim = Simulator(start_fault_time=40, end_fault_time=50)
        for t in range(80):
            current_flow, current_temp = sim.step(t, hot_valve, cold_valve)
            error_temp = current_temp - target_temp
            error_flow = current_flow - target_flow
            hot_set, cold_set = fuzzification(
                error_temp,
                error_flow,
                rules = self.rules
            )
            hot_change = defuzzification(hot_set)
            cold_change = defuzzification(cold_set)
           
            hot_valve = max(0.0, min(hot_valve+hot_change, 1.0))
            cold_valve = max(0.0, min(cold_valve+cold_change, 1.0))
            
            total_error += (abs(error_flow)*10) + abs(error_temp)
            if current_temp > 45.0:
                total_error += 10 * current_temp
            if current_flow < 0.05:
                total_error += 5000.0
        
        return (10000.0 / (total_error+1.0)) 


    def mutate(self, value: ValveChangeValues):
        if value == ValveChangeValues.NEGATIVE_BIG:
            return ValveChangeValues.NEGATIVE_SMALL
        
        if value == ValveChangeValues.NEGATIVE_SMALL:
            if random.random() < 0.5:
                return ValveChangeValues.NEGATIVE_BIG
            else:
                return ValveChangeValues.ZERO
        
        if value == ValveChangeValues.ZERO:
            if random.random() < 0.5:
                return ValveChangeValues.NEGATIVE_SMALL
            else:
                return ValveChangeValues.POSITIVE_SMALL
        
        if value == ValveChangeValues.POSITIVE_SMALL:
            if random.random() < 0.5:
                return ValveChangeValues.ZERO
            else:
                return ValveChangeValues.POSITIVE_BIG
        
        if value == ValveChangeValues.POSITIVE_BIG:
            return ValveChangeValues.POSITIVE_SMALL


    def breed(self, other):
        new1 = []
        new2 = []
        for first, second in zip(self.rules, other.rules):
            if random.random() < 0.2:
                new1.append((self.mutate(first[0]), self.mutate(second[1])))
            else:    
                new1.append((first[0], second[1]))
            if random.random() < 0.2:
                new2.append((second[0], first[1]))
            else:
                new2.append((self.mutate(second[0]), self.mutate(first[1])))
        
        return self.__class__(new1), self.__class__(new2)
    


class Population:
    def __init__(self, population_size = 50):
        self.population_size = population_size
        self.population = []
        for _ in range(self.population_size):
            self.population.append(
                Chromosome(
                    self.generate_rules()
                )
            )


    def generate_rules(self):
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


    def run(self, num_of_generations = 30, is_printing = False):
        best = None
        for gen in range(num_of_generations):
            score = []
            for indiv in self.population:
                score.append((indiv.get_score(), indiv))
            score.sort(key=lambda x: x[0], reverse=True)
            best = score[0]
            if is_printing and not (gen % 5):
                print(f"Generation {gen}: best fitness {best[0]:.4f}")

            new_population = [score[0][1], score[1][1]]
            for _ in range(self.population_size-2):
                parent1 = max(random.sample(score, 3), key=lambda x:x[0])[1]
                parent2 = max(random.sample(score, 3), key=lambda x:x[0])[1]
                child1, child2 = parent1.breed(parent2)
                if random.random() < 0.5:
                    new_population.append(child1)
                else:
                    new_population.append(child2)

            self.population = new_population
        return best