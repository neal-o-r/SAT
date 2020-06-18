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


def rm_clse(circ: Circuit, trm: Term) -> Circuit:
    # remove all clauses containg a term
    return [clse for clse in circ if trm not in clse]


def rm_term(circ: Circuit, trm: Term) -> Circuit:
    # remove a term from all clauses
    return [tuple(t for t in clse if t != trm) for clse in circ]


def pure_literal_resolution(circ: Circuit) -> (Assignment, Circuit):
    terms = [t for clse in circ for t in clse]
    # get terms that only have one sign in the circuit
    pures = {t for t in terms if -t not in terms}

    # assign them to make the positive
    assigns = {p.variable: p.sign for p in pures}
    new_circ = circ.copy()
    # remove clauses that contain them
    for p in pures:
        new_circ = rm_clse(new_circ, p)

    return assigns, new_circ


def unit_clause_resolution(
    circ: Circuit, assigns: Assignment = {}
) -> (Assignment, Circuit):

    # if there are no unit clauses return
    # be careful, pruning units can create empty clauses
    # but these should be removed, rather than being
    # used to indicate a contradiction
    circ = [c for c in circ if c != ()]
    if all(len(clse) > 1 for clse in circ):
        return assigns, circ

    # get units and assign them
    units = {clse[0] for clse in circ if len(clse) == 1}
    assigns = {**assigns, **{u.variable: u.sign for u in units}}
    new_circ = circ.copy()
    for u in units:
        #remove the units, both positive and negative
        s = 1 if u.sign else -1
        new_circ = rm_term(rm_clse(new_circ, s *u ), -1 * s * u)

    # call recursively, since removing units may make new units
    return unit_clause_resolution(new_circ, assigns)


def dpll(circ: Circuit, assigns: Assignment = {}) -> Solution:

    if len(circ) is 0:
        return True, assigns

    if any(len(clse) is 0 for clse in circ):
        return False, {}

    v = Term(circ[0][0].variable)

    pure_a, pure_circ = pure_literal_resolution(circ)
    unit_a, resolved_circ = unit_clause_resolution(pure_circ)

    assigns = {**assigns, **pure_a, **unit_a}

    new_circ = rm_term(rm_clse(resolved_circ, v), -v)
    sat, pot_assign = dpll(new_circ, {**assigns, **{v.variable: True}})
    if sat:
        return sat, pot_assign

    new_circ = rm_term(rm_clse(resolved_circ, -v), v)
    sat, pot_assign = dpll(new_circ, {**assigns, **{v.variable: False}})
    if sat:
        return sat, pot_assign

    return False, {}


def simple_dpll(circ: Circuit, assigns: Assignment = {}) -> Solution:

    if len(circ) is 0:
        return True, assigns

    if any(len(clse) is 0 for clse in circ):
        return False, {}

    v = Term(circ[0][0].variable)

    new_circ = rm_term(rm_clse(circ, v), -v)
    sat, pot_assign = simple_dpll(new_circ, {**assigns, **{v.variable: True}})
    if sat:
        return sat, pot_assign

    new_circ = rm_term(rm_clse(circ, -v), v)
    sat, pot_assign = simple_dpll(new_circ, {**assigns, **{v.variable: False}})
    if sat:
        return sat, pot_assign

    return False, {}


if __name__ == "__main__":

    circ = random_circuit(10, 10)
    se = exhaustive_search(circ)
    #sd = dpll(circ)
