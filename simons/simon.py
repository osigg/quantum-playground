from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler
from qiskit.quantum_info import Statevector
 
from oracle import simon_oracle


def simon_circuit(s: str) -> QuantumCircuit:
    n = len(s)
    qc = QuantumCircuit(2*n, n)
    qc.h(range(n))
    qc.barrier()
    qc.compose(simon_oracle(s), inplace=True)
    qc.barrier()
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def query_f(s: str, x: str) -> str:
    """ classical query, passes |x>|0> through oracle (read f(x))"""
    n = len(s)
    qc = QuantumCircuit(2*n)
    for i, bit in enumerate(reversed(x)):
        if bit == "1":
            qc.x(i)
    qc.compose(simon_oracle(s), inplace=True)
    (outcome,) = Statevector(qc).probabilities_dict()
    return outcome[:n]

def gf2_rref(rows: list[list[int]], n: int) -> tuple[list[list[int]], list[int]]:
    """Gauss-Jordan elimination mod 2. Returns (reduced rows, pivot columns).
 
    Same as ordinary elimination, except subtraction is XOR and there's no
    scaling: every nonzero entry is already 1.
    """

    rows = [r[:] for r in rows]
    pivots: list[int] = []
    for col in range(n):
        r0 = len(pivots)
        pivot = next((r for r in range(r0, len(rows)) if rows[r][col]), None)
        if pivot is None:
            continue
        rows[r0], rows[pivot] = rows[pivot], rows[r0]
        for r in range(len(rows)):
            if r != r0 and rows[r][col]:
                rows[r] = [a ^ b for a, b in zip(rows[r], rows[r0])]
        pivots.append(col)
    return rows[: len(pivots)], pivots

def solve_null_space(rows: list[list[int]], n: int) -> list[int]:
    """ return nonzero s with y . s = 0(mod2) for every row in y"""

    reduced, pivots = gf2_rref(rows, n)
    free = next(c for c in range(n) if c not in pivots)
    s = [0] * n
    s[free] = 1

    for row, col in zip(reduced, pivots):
        s[col] = row[free]
    return s

def run_simon(s: str, max_queries: int = 100) -> tuple[str, int]:
    """query until pin down s"""
    n = len(s)
    sampler = StatevectorSampler()
    qc = simon_circuit(s)
    rows: list[list[int]] = []
    queries = 0

    while len(rows) < n-1:
        if queries == max_queries:
            raise RuntimeError("did not converge")

        counts = sampler.run([qc], shots = 1).result()[0].data.c.get_counts()
        queries += 1
        row = [int(b) for b in next(iter(counts))]
        if len(gf2_rref(rows + [row], n)[1]) > len(rows):
            rows.append(row)

    candidate = "".join(map(str, solve_null_space(rows, n)))

    if query_f(s, "0" * n) == query_f(s, candidate):
        return candidate, queries
    return "0" * n, queries


if __name__ == "__main__":
    for s in ["11", "110", "1011", "10010", "01101", "000"]:
        answer, queries = run_simon(s)
        status = "OK" if answer == s else "BAD"
        print(f"{status} s={s} found={answer} queries={queries}")
    print(simon_circuit("110").draw(output="text"))