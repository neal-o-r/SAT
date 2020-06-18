from props import Term, Circuit

def parse_txt(txt: str) -> list:
    return [s for s in txt.split('\n') if s != '' and not s.startswith('#')]


def make_sat(filename: str) -> Circuit:
    with open(filename) as f:
        txt = f.read()

    rules = parse_txt(txt)
    return [tuple(Term(t) for t in rule.split()) for rule in rules]



