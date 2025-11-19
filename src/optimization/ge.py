from src.fuzzy.fuzzy_sets import FuzzyValues
from src.fuzzy.fuzzy import FuzzyConfiguration, classify


class Chromosome:
    def __init__(self, config: FuzzyConfiguration):
        self.config = config

    
    def evaluate(self, images, labels):
        cmp_list = []
        for img, label in zip(images, labels):
            result = classify(img, self.config)
            cmp_list.append(result == label)
        accuracy = sum(cmp_list)/float(len(cmp_list))
        self.eval = self._fitness(accuracy)
        return self.eval
    
    
    def _fitness(self, accuracy):
        return 0.95*accuracy - 0.05*self._count_conditions()
    

    def _count_conditions(self):
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
        return len(valid_con)
    
    

def make_init_population():
    pass