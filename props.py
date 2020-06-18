from __future__ import annotations
from typing import List, Tuple, Dict


class Term:
    def __init__(self, name: str):
        self.name = name
        self.variable = name.split("¬")[-1]
        self.sign = not (name.startswith("¬"))

    def __repr__(self) -> str:
        return self.name

    def __eq__(self, b: Term) -> bool:
        return b.name == self.name

    def __mul__(self, i: int) -> Term:
        return self if i > 0 else Term("¬" * self.sign + self.variable)

    def __rmul__(self, i: int) -> Term:
        return self.__mul__(i)

    def __neg__(self) -> Term:
        return self.__mul__(-1)

    def __hash__(self) -> int:
        return hash(self.name)

    def assign(self, b: bool) -> bool:
        return b if self.sign else not (b)


Clause = Tuple[Term, ...]
Circuit = List[Clause]
Assignment = Dict[str, bool]
Solution = Tuple[bool, Assignment]
