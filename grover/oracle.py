from qiskit import QuantumCircuit

def phase_oracle(target: str) -> QuantumCircuit:
    """ flip the phase of the target state, leave all others unchanged """
    n = len(target)
    qc = QuantumCircuit(n, name = "oracle")

    

    zero_qubits = [i for i, bit in enumerate(reversed(target)) if bit == "0"]
    for qubit in zero_qubits:
        qc.x(qubit)

    qc.h(n-1)
    qc.mcx(list(range(n-1)), n-1)  # multi-controlled X gate
    qc.h(n-1)

    for qubit in zero_qubits:
        qc.x(qubit)

    return qc