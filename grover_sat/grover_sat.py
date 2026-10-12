import math

from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.primitives import StatevectorSampler

from oracle import CLAUSES, VARIABLES, checker_oracle, evaluate, num_qubits

def diffuser(n):
    """ reflect about the uniform state on n qubits """
    qc = QuantumCircuit(n, name="diffuser")
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # multi-controlled X
    qc.h(n-1)
    qc.x(range(n))
    qc.h(range(n))
    return qc

def num_solutions():
    n = len(VARIABLES)
    return sum(evaluate(format(i, f"0{n}b")) for i in range(2**n))


def optimal_iterations(n, m):
    """ compute the optimal number of Grover iterations """
    theta = math.asin(math.sqrt(m / 2**n))
    return max(1, round(math.pi / (4 * theta) - 0.5))

def grover_sat_circuit(iterations=None, uncompute = True):
    n = len(VARIABLES)
    total = num_qubits()
    output = total - 1
    search = list(range(n))


    if iterations is None:
        iterations = optimal_iterations(n, num_solutions())

    qr = QuantumRegister(total, name="q")
    cr = ClassicalRegister(n, name="c")
    qc = QuantumCircuit(qr, cr)

    qc.h(search)  # initialize search qubits to uniform superposition
    qc.x(output)  # initialize output qubit to |1>
    qc.h(output)  # put output qubit into superposition

    oracle = checker_oracle(uncompute=uncompute)
    diff = diffuser(n)

    # grover iteration
    for _ in range (iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diff, qubits=search, inplace=True)

    qc.measure(search, cr)
    return qc, iterations

def run(uncompute = True, shots = 2048):
    qc, k = grover_sat_circuit(uncompute=uncompute)
    result = StatevectorSampler().run([qc], shots=shots).result()
    counts = result[0].data.c.get_counts()
    return k, dict(sorted(counts.items(), key=lambda kv: -kv[1]))

if __name__ == "__main__":
    print("formula clauses:", CLAUSES)
    print("solutions M =", num_solutions(), "out of N =", 2 ** len(VARIABLES))
 
    for uncompute in (True, False):
        k, counts = run(uncompute=uncompute)
        hits = sum(c for s, c in counts.items() if evaluate(s))
        label = "with uncompute" if uncompute else "WITHOUT uncompute"
        print(f"\n{label}: {k} iteration(s)")
        for state, c in counts.items():
            mark = "  <- satisfies" if evaluate(state) else ""
            print(f"  {state}: {c}{mark}")
        print(f"  success rate: {hits / sum(counts.values()):.1%}")