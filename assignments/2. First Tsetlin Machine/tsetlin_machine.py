import json
import random as random

# 1) Load data and produce boolean literals (like cars/planes)
with open("assignments/2. First Tsetlin Machine/breast_cancer_dataset.json") as f:
    raw = json.load(f)

with open("assignments/2. First Tsetlin Machine/defined_rules.json") as f:
    defined_rules = json.load(f)

def to_booleans(p):
    return {
        'Deg_malig_3': p.get('Deg_malig', 0) == 3,
        'Menopause_lt40': p.get('Menopause') == 'lt40',
        'Inv_nodes_0_2': p.get('Inv_nodes') == '0-2',
        'label_is_recurrence': p.get('Recurrence') == 'yes'
    }

categories = ['Deg_malig_3', 'Menopause_lt40', 'Inv_nodes_0_2']
patients = [to_booleans(p) for p in raw]

# 2) Chapter_1-style primitives
def evaluate_condition(observation, condition):
    truth_value_of_condition = True
    for feature in categories:
        if feature in condition and observation[feature] == False:
            truth_value_of_condition = False
            break
        if 'NOT ' + feature in condition and observation[feature] == True:
            truth_value_of_condition = False
            break
    return truth_value_of_condition

class Memory:
    def __init__(self, forget_value, memorize_value, memory):
        self.memory = memory
        self.forget_value = forget_value
        self.memorize_value = memorize_value
    
    def get_memory(self):
        return self.memory
    
    def get_literals(self):
        return list(self.memory.keys())
    
    def get_condition(self):
        condition = []
        for literal in self.memory:
            if self.memory[literal] >= 6:
                condition.append(literal)
        return condition
        
    def memorize(self, literal):
        if random.random() <= self.memorize_value and self.memory[literal] < 10:
            self.memory[literal] += 1
            
    def forget(self, literal):
        if random.random() <= self.forget_value and self.memory[literal] > 1:
            self.memory[literal] -= 1
            
    def memorize_always(self, literal):
        if self.memory[literal] < 10:
            self.memory[literal] += 1

def type_i_feedback(observation, memory):
    remaining_literals = memory.get_literals()
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in categories:
            if observation[feature] == True:
                memory.memorize(feature)
                remaining_literals.remove(feature)
            else:
                memory.memorize('NOT ' + feature)
                remaining_literals.remove('NOT ' + feature)
    for literal in remaining_literals:
        memory.forget(literal)

def type_ii_feedback(observation, memory):
    if evaluate_condition(observation, memory.get_condition()) == True:
        for feature in categories:
            if observation[feature] == False:
                memory.memorize_always(feature)
            else:
                memory.memorize_always('NOT ' + feature)

# 3) Two sets of rules that vote (like car/plane rules)
def classify(observation, recurrence_rules, nonrec_rules):
    vote_sum = 0
    for rule in recurrence_rules:
        if evaluate_condition(observation, rule.get_condition()):
            vote_sum += 1
    for rule in nonrec_rules:
        if evaluate_condition(observation, rule.get_condition()):
            vote_sum -= 1
    return 'Recurrence' + str("      Votes:  " + str(vote_sum)) if vote_sum >= 0 else 'Non-Recurrence' + str("  Votes: " + str(vote_sum))

def main():
    # Initialize memories at 5 for all literals
    NUM_RECURRENCE_RULES = 1
    NUM_NONREC_RULES = 1
    FORGET_VALUE = 0.8
    MEMORIZE_VALUE = 0.2

    # Use defined rules if True, otherwise train rules from scratch
    USE_DEFINED_RULES = False
    DEFINED_RULES = defined_rules

    if USE_DEFINED_RULES:
        recurrence_rules = [Memory(FORGET_VALUE, MEMORIZE_VALUE, dict(rule)) for rule in DEFINED_RULES if rule['label_is_recurrence']]
        nonrec_rules = [Memory(FORGET_VALUE, MEMORIZE_VALUE, dict(rule)) for rule in DEFINED_RULES if not rule['label_is_recurrence']]
    else:
        init_mem = {
            'Deg_malig_3':5, 'NOT Deg_malig_3':5,
            'Menopause_lt40':5, 'NOT Menopause_lt40':5,
            'Inv_nodes_0_2':5, 'NOT Inv_nodes_0_2':5
        }
        recurrence_rules = [Memory(FORGET_VALUE, MEMORIZE_VALUE, dict(init_mem)) for _ in range(NUM_RECURRENCE_RULES)]
        nonrec_rules = [Memory(FORGET_VALUE, MEMORIZE_VALUE, dict(init_mem)) for _ in range(NUM_NONREC_RULES)]

        # 4) Mix Type I and II
        for i in range(1000):
            observation = random.choice(patients)
            if observation['label_is_recurrence']:
                for rule in recurrence_rules:
                    type_i_feedback(observation, rule)
            else:
                for rule in nonrec_rules:
                    type_ii_feedback(observation, rule)

    # 5) Print learned rules and quick predictions
    print("Recurrence rules:")
    for r in recurrence_rules:
        print("IF " + " AND ".join(r.get_condition()) + " THEN Recurrence")
    print("Non-Recurrence rules:")
    for r in nonrec_rules:
        print("IF " + " AND ".join(r.get_condition()) + " THEN Non-Recurrence")

    print("\nPredictions:")
    for i, observation in enumerate(patients, start=1):
        print(f'Patient {i}:', classify(observation, recurrence_rules, nonrec_rules))

if __name__ == "__main__":
    main()

