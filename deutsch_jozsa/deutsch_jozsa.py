from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

from oracle import constant_oracle, parity_oracle, random_balanced_oracle


def deutsch_jozsa_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n+1, n)

    # output qubit
    qc.x(n)
    qc.h(n)

    # all inputs
    qc.h(range(n))

    qc.compose(oracle, inplace=True)

    # read inputs only
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def classify(counts: dict[str, int], n: int) ->str:
    return "constant" if set(counts) == {"0" * n} else "balanced"

if __name__ == "__main__":
    n = 4
    shots = 1024
    sampler = StatevectorSampler()

    cases = [
        ("constant", constant_oracle(n, 0)),
        ("constant", constant_oracle(n, 1)),
        ("balanced", parity_oracle(n, "1011")),
        ("balanced", parity_oracle(n, "0001")),
        ("balanced", random_balanced_oracle(n, seed=7)),
        ("balanced", random_balanced_oracle(n, seed=42)),
    ]


    for expected, oracle in cases:
        qc = deutsch_jozsa_circuit(oracle)
        counts = sampler.run([qc], shots=shots).result()[0].data.c.get_counts()
        answer = classify(counts, n)
        status = "ok" if answer == expected else "WRONG"
        print(f"{oracle.name:12s} counts={counts}  -> {answer:8s} [{status}]")

    print()
    print(deutsch_jozsa_circuit(parity_oracle(n, "1011")).draw())