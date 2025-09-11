#!/usr/bin/python
import random

class Environment:
    def __init__(self):
        pass

    def penalty(self, M):
        if M == 0 or M == 1 or M == 2 or M == 3:
            if random.random() < M * 0.2:
                return False
            else:
                return True
        elif M == 4 or M == 5:
            if random.random() < 0.6 - (M - 3) * 0.2:
                return False
            else:
                return True

class Tsetlin:
    def __init__(self, n):
        # n is the number of states per action
        self.n = n
        # Initial state selected randomly
        self.state = random.choice([self.n, self.n + 1])

    def reward(self):
        if self.state <= self.n and self.state > 1:
            self.state -= 1
        elif self.state > self.n and self.state < 2 * self.n:
            self.state += 1

    def penalize(self):
        if self.state <= self.n:
            self.state += 1
        elif self.state > self.n:
            self.state -= 1

    def makeDecision(self):
        if self.state <= self.n:
            return 1
        else:
            return 2


# Main execution
env = Environment()
num_automata = 5
automata = [Tsetlin(10) for _ in range(num_automata)]  # Create 5 Tsetlin Automata
total_iterations = 100000
final_decisions=[]

for iteration in range(total_iterations):
    # All 5 automata make decisions
    decisions = []
    for automaton in automata:
        action = automaton.makeDecision() # 1 = "No" and 2 = "Yes"
        decisions.append(action)
    
    # Count "Yes" actions
    M = decisions.count(2)    

    final_decisions.append(decisions)

    # Apply rewards / penalties to each automaton
    for i, automaton in enumerate(automata):
        penalty = env.penalty(M)
        
        if penalty:
            automaton.penalize()
        else:
            automaton.reward()
    
yes_count = 0
for decision in final_decisions:
    yes_count += decision.count(2)
print(f"Final 'Yes' actions: {yes_count/len(final_decisions)}")
