from src.optimization.generate_values import *
from src.fuzzy.fuzzy_sets import FuzzyValues
from src.fuzzy.fuzzy import FuzzyConfiguration, classify


class Chromosome:
    NOT_CALCULATED = -1.0

    def __init__(self, config: FuzzyConfiguration):
        self.config = config
        self.eval = self.NOT_CALCULATED
        self.accuracy = self.NOT_CALCULATED

    
    def evaluate(self, images, labels):
        if self.eval == self.NOT_CALCULATED:
            cmp_list = []
            for img, label in zip(images, labels):
                result = classify(img, self.config)
                cmp_list.append(result == label)
            accuracy = sum(cmp_list)/float(len(cmp_list))
            self.accuracy = accuracy
            self.eval = self._fitness(accuracy)
        return self.eval
    
    
    def _fitness(self, accuracy):
        return 0.95*accuracy - 0.05*self._count_conditions()
    

    def _count_conditions(self):
        MAX_CONDITIONS = 70
        conditions = []
        conditions.extend(self.config.rule_zero_cfg[:-1])
        conditions.extend(self.config.rule_one_cfg[:-1])
        conditions.extend(self.config.rule_two_cfg[:-1])
        conditions.extend(self.config.rule_three_cfg[:-1])
        conditions.extend(self.config.rule_four_cfg[:-1])
        conditions.extend(self.config.rule_five_cfg[:-1])
        conditions.extend(self.config.rule_six_cfg[:-1])
        conditions.extend(self.config.rule_seven_cfg[:-1])
        conditions.extend(self.config.rule_eight_cfg[:-1])
        conditions.extend(self.config.rule_nine_cfg[:-1])
        valid_con = [c for c in conditions if c != FuzzyValues.IRRELEVANT.value]
        return len(valid_con)/MAX_CONDITIONS


    def _combine_rule_lists(self, rule1, rule2):
        first = []
        second = []
        flip = True
        for x, y in zip(rule1, rule2):
            if flip:
                first.append(y)
                second.append(x)
            else:
                first.append(x)
                second.append(y)
            flip = not flip
        return first, second


    def _combine_config(
        self, 
        cfg1: FuzzyConfiguration, 
        cfg2: FuzzyConfiguration
    ):
        cfg1_list = list(cfg1)
        cfg2_list = list(cfg2)
        first_list = []
        second_list = []
        flip = True
        for x, y in zip(cfg1_list, cfg2_list):
            if isinstance(x, list):
                c1, c2 = self._combine_rule_lists(x, y)
                first_list.append(c1)
                second_list.append(c2)
            if flip:
                first_list.append(x)
                second_list.append(y)
            else:
                first_list.append(y)
                second_list.append(x)
            flip = not flip
        first = FuzzyConfiguration.from_list(first_list)
        second = FuzzyConfiguration.from_list(second_list)
        return first, second


    def breed(self, other):
        first, second = self._combine_config(self.config, other.config)
        return self.__class__(first), self.__class__(second)
    


class Population:
    def __init__(self, chromosomes: list[Chromosome]):
        self.chromosomes = chromosomes
    

    def get_bests(self, num=1):
        self.chromosomes.sort(key=lambda x: x.eval)
        self.chromosomes.reverse()
        return self.chromosomes[:num]
    

    def run_eval(self, images, labels, num_breeding = 24):
        if num_breeding % 2 != 0:
            raise("Can't breed odd number of chromosomes")
        for chromosome in self.chromosomes:
            chromosome.evaluate(images, labels)
        best = self.get_bests(num_breeding)[0]
        print(f"Best accuracy in cycle: {best.accuracy}")




def gen_correct_params_config():
    return FuzzyConfiguration(
        *gen_correct_centroid_params(),
        *gen_correct_aspect_ratio_params(),
        *gen_correct_extent_params(),
        *gen_correct_solidity_params(),
        *gen_correct_h_sym_params(),
        *gen_correct_v_sym_params(),
        *gen_random_rules()
    )


def make_init_population(count = 50):
    population = [
        Chromosome(gen_correct_params_config()) for _ in range(count)
    ]
    return Population(population)


def optimize(images, labels, population_size = 50, breeding_size = 24):
    population = make_init_population(population_size)
    population.run_eval(images, labels, breeding_size)