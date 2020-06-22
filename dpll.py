from props import Term, Clause, Circuit, Assignment, Solution
from typing import List, Tuple

Update = Tuple[Assignment, Circuit]


def rm_clse(circ: Circuit, trm: Term) -> Circuit:
    return [clse for clse in circ if trm not in clse]


def rm_term(circ: Circuit, trm: Term) -> Circuit:
    return [tuple(t for t in clse if t != trm) for clse in circ]


def pure_literal_resolution(circ: Circuit) -> Update:
    terms = [t for clse in circ for t in clse]
    pures = {t for t in terms if -t not in terms}

    assigns = {p.variable: p.sign for p in pures}
    new_circ = circ.copy()
    for p in pures:
        new_circ = rm_clse(new_circ, p)

    return assigns, new_circ


def unit_clause_resolution(circ: Circuit, assigns: Assignment = {}) -> Update:
    if all(len(clse) != 1 for clse in circ):
        return assigns, circ

    units = {clse[0] for clse in circ if len(clse) == 1}
    assigns = {**assigns, **{u.variable: u.sign for u in units}}

    new_circ = circ.copy()
    while len(units) > 0:
        u = list(units)[0]
        new_circ = rm_term(rm_clse(new_circ, u), -u)

        units = {clse[0] for clse in new_circ if len(clse) == 1}
        assigns = {**assigns, **{u.variable: u.sign for u in units}}

    return assigns, new_circ#unit_clause_resolution(new_circ, assigns)


def dpll(circ: Circuit, assigns: Assignment = {}) -> Solution:
    if len(circ) is 0:
        return True, assigns

    if any(len(clse) == 0 for clse in circ):
        return False, {}

    unit_a, unit_circ = unit_clause_resolution(circ)
    pure_a, resolved_circ = pure_literal_resolution(unit_circ)

    assigns = {**assigns, **pure_a, **unit_a}
    # did resolution solve the problem
    if len(resolved_circ) is 0:
        return True, assigns

    v = Term(circ[0][0].variable)

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

