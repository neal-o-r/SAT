from props import Term, Circuit


def read_file(filename: str) -> list:
    with open(filename) as f:
        txt = f.read()
    return {s for s in txt.split("\n") if s != "" and not s.startswith("#")}


def make_circ(txt: str) -> Circuit:
    return [tuple(Term(t) for t in clse.split()) for clse in txt]
