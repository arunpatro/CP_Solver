import sys
import numpy as np


class CP_Model:
    def __init__(self, variables, domains, constraints=[]):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints

    def choose(self, search_space, search_strategy="variable/value"):
        if search_strategy == "variable/value":
            var_candidates = [
                (i, len(search_space[i]))
                for i in range(len(self.variables))
                if len(search_space[i]) > 1
            ]
            if var_candidates:
                var_candidates.sort(key=lambda x: x[1])
                val_candidates = search_space[
                    var_candidates[0][0]
                ]  # choose the one with the smallest domain and smalles value
                return (var_candidates[0], val_candidates[0])
            else:
                return None

    def get_subset(self, search_space, choice):
        # strong choice
        for i, domain in enumerate(search_space):
            if i == choice[0]:
                search_space[choice[0]] = [choice[1]]  # split state and search_space and detect state NA ship via Numpy NP
            else:
                domain.remove(choice[1]) # not required, as will be cleaned by propogation constraints

        return search_space

    def get_options(self, search_space, search_strategy="variable/value"):
        if search_strategy == "variable/value":
            var_candidates = [
                (i, len(search_space[i]))
                for i in range(len(self.variables))
                if len(search_space[i]) > 1
            ]
            if var_candidates:
                var_candidates.sort(key=lambda x: x[1])
                options = [(var, val) for var, _ in var_candidates for val in search_space[var]]
                return options
            else:
                return []

    def feasible(self, search_space):
        # all domains must have atleast 1 value, doesn't signal solution is found
        lens = []
        for d in search_space:
            l = len(d)
            if l == 0:
                return False
            lens.append(l)
        
        if sum(lens) == len(lens):
            return False, search_space, "Solution Found"
                
        return True

    def propogate_constraints(self, search_space):
        while self.feasible(search_space):
            pruning_counter = 0
            for constraint in self.constraints: # apply constraint to valid domains
                var1, var2 = constraint
                d1, d2 = search_space[var1], search_space[var2]
                l1, l2 = len(d1), len(d2)

                if l1 == 1:
                    d2 = [val for val in d2 if val != d1[0]]
                elif l2 == 1:
                    d1 = [val for val in d1 if val != d2[0]]

                pruning_counter += l1 + l2 - len(d1) - len(d2)
            
            if pruning_counter == 0:
                break
        
        return search_space

    def recur(search_space):
        # all domains must have atleast 1 value, doesn't signal solution is found

        if search_space == []:
            return []

        for d in search_space:
            if not d:
                return False

        lens = [len(d) for d in search_space]
        if sum(lens) == len(search_space):
            return search_space, "Solution Found"

        return []

        return search_space

    def solve(self):
        search_space = self.domains
        while self.feasible(search_space): # and solution not found
            # self.propogate_constraints(search_space)
            options = self.get_options(search_space)
            for option in options:
                search_space = self.get_subset(search_space, option)
                while self.feasible(search_space):
                    search_space = self.propogate_constraints(search_space)
                    if self.found_solution(solution)

            # make a choice
            # that is most likely to fail - smallest domain i.e. most constrained
            # break symmetry - hard or soft via domain splitting
            # dont choose variable with domain size 1
            print(*zip(self.variables, self.search_space), sep="\n")

            # pruning


if __name__ == "__main__":
    N_Queen = 10

    # these are row variables
    variables = [i for i in range(N_Queen)]
    domains = [[i for i in range(N_Queen)] for _ in range(N_Queen)]

    constraints = [(i, j) for i in range(N_Queen) for j in range(i)]

    model = CP_Model(variables, domains, constraints)
    model.solve()
