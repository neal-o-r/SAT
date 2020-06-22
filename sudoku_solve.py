from props import Term, Circuit, Solution, Assignment
from pycosat import itersolve
from parse import read_file, make_circ
from dpll import dpll
from typing import List
from sudoku_circ import show_string, assignment_to_str


def dpll_solve(sudo: Circuit) -> Solution:
    return dpll(sudo)


def pycosat_solve(circ: Circuit) -> Solution:
    variables = {t.variable for c in circ for t in c}
    to_sym = dict(zip(variables, range(1, len(variables) + 1)))
    from_sym = {v: k for k, v in to_sym.items()}

    sym = []
    for c in circ:
        sym.append([to_sym[t.variable] if t.sign else -1 * to_sym[t.variable]
            for t in c])

    sol = next(itersolve(sym), False)
    if sol:
        return True, {from_sym[abs(s)] : s > 0 for s in sol}
    return False, {}


if __name__ == "__main__":
    sudo = make_circ(read_file("./circuits/sudoku_circuit.txt"))

    sol = pycosat_solve(sudo)




