from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

from oracle import FUNCTIONS, deutsch_oracle

def deutsch_circuit(name: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, 1)


    # ancilla
    qc.x(1)
    qc.h(1)

    # input
    qc.h(0)

    qc.compose(deutsch_oracle(name), inplace=True)

    qc.h(0)
    qc.measure(0, 0)
    return qc


if __name__ == "__main__":
    sampler = StatevectorSampler()

    for name, truth_table in FUNCTIONS.items():
        qc = deutsch_circuit(name)
        counts = sampler.run([qc], shots = 1024).result()[0].data.c.get_counts()

        answer = "constant" if counts.get("0",0) == 1024 else "balanced"
        expected = "constant" if truth_table[0] == truth_table[1] else "balanced"
        print(f"{name:11s} f={truth_table} counts = {counts} -> {answer:8s} (expected: {expected})")

    print()
    print(deutsch_circuit("identity").draw())
    