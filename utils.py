"""
Utility functions for working with SAT
(from Ray Hettinger https://rhettinger.github.io/)
"""
from itertools import combinations
from functools import lru_cache

@lru_cache(maxsize=None)
def neg(element) -> 'element':
    'Negate a single element'
    return element[1:] if element.startswith('~') else '~' + element

def from_dnf(groups) -> 'cnf':
    'Convert from or-of-ands to and-of-ors'
    cnf = {frozenset()}
    for group in groups:
        nl = {frozenset([literal]) : neg(literal) for literal in group}
        # The "clause | literal" prevents dup lits: {x, x, y} -> {x, y}
        # The nl check skips over identities: {x, ~x, y} -> True
        cnf = {clause | literal for literal in nl for clause in cnf
              if nl[literal] not in clause}
        # The sc check removes clauses with superfluous terms:
        #     {{x}, {x, z}, {y, z}} -> {{x}, {y, z}}
        # Should this be left until the end?
        sc = min(cnf, key=len)          # XXX not deterministic
        cnf -= {clause for clause in cnf if clause > sc}
    return list(map(tuple, cnf))

class Q:
    'Quantifier for the number of elements that are true'
    def __init__(self, elements):
        self.elements = tuple(elements)
    def __lt__(self, n: int) -> 'cnf':
        return list(combinations(map(neg, self.elements), n))
    def __le__(self, n: int) -> 'cnf':
        return self < n + 1
    def __gt__(self, n: int) -> 'cnf':
        return list(combinations(self.elements, len(self.elements)-n))
    def __ge__(self, n: int) -> 'cnf':
        return self > n - 1
    def __eq__(self, n: int) -> 'cnf':
        return (self <= n) + (self >= n)
    def __ne__(self, n) -> 'cnf':
        raise NotImplementedError
    def __repr__(self) -> str:
        return f'{self.__class__.__name__}(elements={self.elements!r})'

def all_of(elements) -> 'cnf':
    'Forces inclusion of matching rows on a truth table'
    return Q(elements) == len(elements)

def some_of(elements) -> 'cnf':
    'At least one of the elements must be true'
    return Q(elements) >= 1

def one_of(elements) -> 'cnf':
    'Exactly one of the elements is true'
    return Q(elements) == 1

def basic_fact(element) -> 'cnf':
    'Assert that this one element always matches'
    return Q([element]) == 1

def none_of(elements) -> 'cnf':
    'Forces exclusion of matching rows on a truth table'
    return Q(elements) == 0
