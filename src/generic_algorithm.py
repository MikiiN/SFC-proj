import random

from src.fuzzy import fuzzification, defuzzification
from src.simulation import Simulator

class Chromosome:
    def __init__(
            self,
            temp_precise_variance,
            temp_approximate_variance,
            flow_precise_variance,
            flow_approximate_variance,
            change_precise_variance,
            change_approximate_variance
    ):
        self.temp_precise = temp_precise_variance
        self.temp_approximate = temp_approximate_variance
        self.flow_precise = flow_precise_variance
        self.flow_approximate = flow_approximate_variance
        self.change_precise = change_precise_variance
        self.change_approximate = change_approximate_variance
        self.score = None


    def get_score(self):
        if self.score == None:
            self.score = self._eval()
        return self.score

    
    def _eval(self):
        target_temp = 38.0
        target_flow = 0.8
        hot_valve = 0.5
        cold_valve = 0.5

        total_error = 0.0
        sim = Simulator(start_fault_time=40, end_fault_time=50)
        for t in range(80):
            current_temp, current_flow = sim.step(t, hot_valve, cold_valve)
            error_temp = current_temp - target_temp
            error_flow = current_flow - target_flow
            hot_set, cold_set = fuzzification(
                error_temp,
                error_flow,
                self.temp_precise,
                self.temp_approximate,
                self.flow_precise,
                self.flow_approximate,
                self.change_precise,
                self.change_approximate
            )
            hot_valve += defuzzification(hot_set)
            cold_valve += defuzzification(cold_set)
            
            total_error += abs(error_flow)*10 + abs(error_temp)*40
            if current_temp > 45.0:
                total_error += 500.0
        
        return 100000.0 / total_error


    def _avg(self, first, second):
        return (first + second) / 2.0


    def _mutation_values(self):
        return random.uniform(-0.5, 0.5), random.uniform(-1.0, 1.0)


    def mutate(self):
        self.temp_precise, self.temp_approximate = self._mutation_values()
        self.flow_precise, self.flow_approximate = self._mutation_values()
        self.change_precise, self.change_approximate = self._mutation_values()


    def breed(self, other):
        return self.__class__(
            self._avg(self.temp_precise, other.temp_precise),
            self._avg(self.temp_approximate, other.temp_approximate),
            self._avg(self.flow_precise, other.flow_precise),
            self._avg(self.flow_approximate, other.flow_approximate),
            self._avg(self.change_precise, other.change_precise),
            self._avg(self.change_approximate, other.change_approximate)
        )
    


class Population:
    def __init__(self, population_size = 50):
        self.population_size = population_size
        self.population = []
        for _ in range(self.population_size):
            temp_prec, temp_approx = self._gen_variances()
            flow_prec, flow_approx = self._gen_variances()
            change_prec, change_approx = self._gen_variances()
            self.population.append(
                Chromosome(
                    temp_prec, temp_approx,
                    flow_prec, flow_approx,
                    change_prec, change_approx
                )
            )
        

    def _gen_variances(self):
        precise = random.uniform(0.1, 5.0)
        approximate = precise + random.uniform(1.0, 20.0)
        return precise, approximate


    def run(self, num_of_generations = 30):
        best = None
        for gen in range(num_of_generations):
            score = []
            for indiv in self.population:
                score.append((indiv.get_score(), indiv))
            score.sort(key=lambda x: x[0], reverse=True)
            best = score[0]
            print(f"Generation {gen}: best fitness {best[0]:.2f}")

            new_population = [score[0][1], score[1][1]]
            for _ in range(len(self.population)-2):
                parent1 = max(random.sample(score, 3), key=lambda x:x[0])[1]
                parent2 = max(random.sample(score, 3), key=lambda x:x[0])[1]
                child = parent1.breed(parent2)

                if random.random() < 0.2:
                    child.mutate()
            self.population = new_population
        return best