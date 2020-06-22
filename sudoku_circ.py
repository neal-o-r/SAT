from itertools import combinations
from props import Term, Circuit, Assignment
from typing import List

grid = '''\
AA AB AC BA BB BC CA CB CC
AD AE AF BD BE BF CD CE CF
AG AH AI BG BH BI CG CH CI
DA DB DC EA EB EC FA FB FC
DD DE DF ED EE EF FD FE FF
DG DH DI EG EH EI FG FH FI
GA GB GC HA HB HC IA IB IC
GD GE GF HD HE HF ID IE IF
GG GH GI HG HH HI IG IH II
'''

values = list('123456789')

table = [row.split() for row in grid.splitlines()]
points = grid.split()
subsquares = dict()
for point in points:
    subsquares.setdefault(point[0], []).append(point)
# Groups:  rows   + columns           + subsquares
groups = table[:] + list(zip(*table)) + list(subsquares.values())


def exactly_one_of(elements: List[Term]) -> Circuit:
    neg = lambda x: -x
    lt = list(combinations(map(neg, elements), 2))
    return lt + [tuple(elements)]


def assignment_to_str(assigns: Assignment) -> str:
    sq_vals = {k[:2]: k[-1] for k, v in assigns.items() if v}
    nums = "".join(sq_vals[g] for g in grid.split())
    return nums


def show_string(sudoku: str):
    'Display grid from a string (values in row major order)'
    n = 3
    fmt = '|'.join(['%s' * n] * n)
    sep = '+'.join(['-'  * n] * n)
    for i in range(n):
        for j in range(n):
            offset = (i * n + j) * n**2
            print(fmt % tuple(sudoku[offset:offset+n**2]))
        if i != n - 1:
            print(sep)


if __name__ == "__main__":

    circ = []

    for point in points:
        circ += exactly_one_of([Term(point + value) for value in values])

    for group in groups:
        for value in values:
            circ += exactly_one_of([Term(point + value) for point in group])


    sudoku = '53..7....6..195....98....6.8...6...34..8.3..17...2...6.6....28....419..5....8..79'
    for p, s in zip(points, sudoku):
        if s is not ".":
            circ.append((Term(p + s), ))

    with open("sudoku/sudoku_circuit.txt", "w") as f:
        for c in circ:
            f.write(" ".join(map(str, c)) + "\n")
