from qiskit import QuantumCircuit

def hidden_string_oracle(secret: str, bias: int = 0) -> QuantumCircuit:
    """bit oracle for f(x) = s * x XOR bias"""

    if any(bit not in "01" for bit in secret):
        raise ValueError("message must be bitstring")
    n = len(secret)
    qc = QuantumCircuit(n+1, name=f"s={secret}")

    for i, bit in enumerate(reversed(secret)):
        if bit == "1":
            qc.cx(i, n)

    if bias == 1:
        qc.x(n)

    return qc

def classical_f(secret: str, bias: int=0):
    s = int(secret, 2)

    def f(x: int) -> int:
        return (bin(s & x).count("1") + bias) % 2

    return f