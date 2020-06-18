from props import Term, Clause, Circuit, Assignment, Solution
from itertools import product
import random as rd
from typing import List, Tuple


def eval_clause(clse: Clause, assigns: Assignment) -> bool:
    return any([t.assign(assigns[t.variable]) for t in clse])


def eval_circuit(circ: Circuit, assigns: Assignment) -> bool:
    return all(eval_clause(clse, assigns) for clse in circ)


def random_circuit(n_vars: int, n_clause: int) -> Circuit:
    variables = [f"x_{i}" for i in range(n_vars)]
    circ = []
    for i in range(n_clause):
        vs = rd.choices(variables, k=3)
        signs = rd.choices([1, -1], k=3)

        circ.append(tuple(s * Term(v) for v, s in zip(vs, signs)))

    return circ


def exhaustive_search(circ: Circuit) -> Solution:
    variables = {term.variable for clse in circ for term in clse}

    for bools in product([True, False], repeat=len(variables)):
        assigns = dict(zip(variables, bools))
        if eval_circuit(circ, assigns):
            return True, assigns

    return False, {}


if __name__ == "__main__":

    circ = random_circuit(10, 10)
    se = exhaustive_search(circ)
