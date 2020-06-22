from props import Term, Circuit
from typing import Set

def read_file(filename: str) -> Set[str]:
    with open(filename) as f:
        txt = f.read()
    return {s for s in txt.split("\n") if s != "" and not s.startswith("#")}


def make_circ(txt: list) -> Circuit:
    return [tuple(Term(t) for t in clse.split()) for clse in txt]
