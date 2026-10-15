import random

from qiskit import QuantumCircuit
from qiskit.primitives import StatevectorSampler

from oracle import classical_f, hidden_string_oracle

def bv_circuit(oracle: QuantumCircuit) -> QuantumCircuit:
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)

    # output
    qc.x(n)
    qc.h(n)

    # every input
    qc.h(range(n))

    qc.compose(oracle, inplace=True)

    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc

def quantum_recovery(secret: str, bias: int = 0, shots: int = 1024) -> tuple[str, dict]:
    qc = bv_circuit(hidden_string_oracle(secret, bias))
    counts = StatevectorSampler().run([qc], shots = shots).result()[0].data.c.get_counts()
    return max(counts, key=counts.get), counts

def classical_recovery(f, n:int) -> tuple[str, int]:
    queries = 1
    bias = f(0)
    bits = []

    for i in range(n):
        bits.append(f(1 << i) ^ bias)
        queries += 1
    return "".join(str(b) for b in reversed(bits)), queries

if __name__ == "__main__":
    rng = random.Random(0)
    secrets = ["1011", "0001", "0000", "1111"]
    secrets += ["".join(rng.choice("01") for _ in range(n)) for n in (6,8,10)]

    all_ok = True
    for secret in secrets:
        for bias in (0,1):
            found, counts = quantum_recovery(secret, bias)
            c_found, c_queries = classical_recovery(classical_f(secret, bias), len(secret))
            ok = found == secret and len(counts) == 1 and c_found == secret
            all_ok &= ok
            print(f"secret={secret:10s} bias={bias}  quantum={found} (1 query)  "
                  f"classical={c_found} ({c_queries} queries)  [{'ok' if ok else 'WRONG'}]")

    print("\nALL OK" if all_ok else "\nFAILURES ABOVE")
    print()
    print(bv_circuit(hidden_string_oracle("1011")).draw())