import math
from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

from oracle import phase_oracle


def diffuser(n: int) -> QuantumCircuit:
    """ reflect every amplitude about the average amplitude """
    qc = QuantumCircuit(n, name = "diffuser")

    qc.h(range(n))
    qc.x(range(n))

    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # multi-controlled X gate
    qc.h(n-1)

    qc.x(range(n))
    qc.h(range(n))

    return qc


def grover_circuit(target: str) -> QuantumCircuit:
    n = len(target)
    iterations = math.floor(math.pi / 4 * math.sqrt(2**n))

    qc = QuantumCircuit(n)
    qc.h(range(n))

    oracle = phase_oracle(target)
    diff = diffuser(n)
    for _ in range(iterations):
        qc.compose(oracle, inplace=True)
        qc.compose(diff, inplace=True)

    qc.measure_all()
    return qc


if __name__ == "__main__":
    target = "1010"
    qc = grover_circuit(target)
    print(qc.draw())

    shots = 2048
    result = StatevectorSampler().run([qc], shots=shots).result()
    counts = result[0].data.meas.get_counts()

    for state, count in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"{state}: {count:5d}  ({count / shots:.1%})")

