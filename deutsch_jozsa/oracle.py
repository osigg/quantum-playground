import random

from qiskit import QuantumCircuit

def constant_oracle(n: int, value: int) -> QuantumCircuit:
    """f(x) = value for every x, 0...n-1 are x, n is output y"""
    qc = QuantumCircuit(n + 1, name=f"const_{value}")
    if value == 1:
        qc.x(n)
    return qc


def parity_oracle(n: int, mask: str) -> QuantumCircuit:
    """f(x) = (mask . x) mod 2, balanced when mask has at least one 1"""

    if len(mask) != n or "1" not in mask:
        raise ValueError("mask must be n bits with at least one 1")
    qc = QuantumCircuit(n+1, name = f"parity_{mask}")

    for i, bit in enumerate(reversed(mask)):
        if bit == "1":
            qc.cx(i, n)
    return qc


def truth_table_oralce(n: int, ones: list[int]) -> QuantumCircuit:
    """f(x) = 1 for the ints in 'ones' """
    qc = QuantumCircuit(n+1, name="truth_table")
    for x in ones:
        zero_qubits = [i for i in range(n) if not (x >> i) & 1]
        for q in zero_qubits:
            qc.x(q)
        qc.mcx(list(range(n)), n)
        for q in zero_qubits:
            qc.x(q)
    return qc


def random_balanced_oracle(n: int, seed: int | None = None) -> QuantumCircuit:
    """balanced function where half are 0 half are 1"""
    rng = random.Random(seed)
    ones = rng.sample(range(2**n), 2**(n-1))
    return truth_table_oralce(n, ones)