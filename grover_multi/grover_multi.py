import math

from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector

from oracle import phase_oracle


def diffuser(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n, name = "diffuser")
    qc.h(range(n))
    qc.compose(phase_oracle(["0" * n]), inplace=True)
    qc.h(range(n))
    return qc

def num_iterations(n: int, m: int) -> int:
    theta = math.asin(math.sqrt(m / 2**n))
    return round((math.pi / 2 - theta) / (2 * theta))


def grover_multi_circuit(targets: list[str], iterations:int | None = None) -> QuantumCircuit:
    n = len(targets[0])
    k = num_iterations(n, len(targets)) if iterations is None else iterations
    qc = QuantumCircuit(n)
    qc.h(range(n))
    for _ in range(k):
        qc.barrier()
        qc.compose(phase_oracle(targets), inplace=True)
        qc.compose(diffuser(n), inplace=True)
    return qc

def success_probability(targets: list[str], iterations: int | None = None) -> float:
    probs = Statevector(grover_multi_circuit(targets, iterations)).probabilities_dict()
    return sum(probs.get(t, 0.0) for t in targets)


if __name__ == "__main__":
    print(grover_multi_circuit(["011", "110"]).draw(output="text"))
    print()

    cases = [
        ["1010"],                                   # M=1,  N=16
        ["1010", "0110"],                           # M=2,  N=16
        ["0001", "0110", "1011", "1100"],           # M=4,  N=16 (M = N/4)
        ["011", "110"],                             # M=2,  N=8  (M = N/4)
        ["101", "010", "111"],                      # M=3,  N=8
        ["00", "11"],                               # M=2,  N=4  (M = N/2)
    ]
    print(f"{'N':>3} {'M':>3} {'k':>3} {'P(success)':>11} {'random guess':>13}")
    for targets in cases:
        n, m = len(targets[0]), len(targets)
        k = num_iterations(n, m)
        p = success_probability(targets)
        print(f"{2**n:>3} {m:>3} {k:>3} {p:>11.3f} {m / 2**n:>13.3f}")

    # Overshoot: probability is a sine wave in k, not a ramp.
    print()
    print("target 1010, success probability vs iterations:")
    for k in range(8):
        p = success_probability(["1010"], iterations=k)
        print(f"  k={k}  {p:.3f}  {'#' * round(40 * p)}")