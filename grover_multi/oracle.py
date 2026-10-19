from qiskit import QuantumCircuit

def phase_oracle(targets: list[str]) -> QuantumCircuit:
    """ flip the phase of the target state, leave all others unchanged """
    n = len(targets[0])

    if n < 2: 
        raise ValueError("need at least 2 qubits")
    if any(len(t) != n for t in targets):
        raise ValueError("all targets must have same length")
    if len(set(targets)) != len(targets):
        raise ValueError("targets must be distinct")

    qc = QuantumCircuit(n, name = f"O({','.join(targets)})")
    for target in targets:
        zeros = [i for i, bit in enumerate(reversed(target)) if bit == "0"]
        if zeros:
            qc.x(zeros)
        qc.h(n-1)
        qc.mcx(list(range(n-1)), n-1)  # multi-controlled X gate
        qc.h(n-1)
        if zeros:
            qc.x(zeros)
    return qc

if __name__ == "__main__":
    import numpy as np
    from qiskit.quantum_info import Operator

    targets = ["0011", "1010", "1110"]
    diag = np.round(np.diag(Operator(phase_oracle(targets)).data).real).astype(int)
    print("diagonal:", diag)
    print("-1 at indices:", [i for i, d in enumerate(diag) if d == -1],
          " expected:", sorted(int(t, 2) for t in targets))