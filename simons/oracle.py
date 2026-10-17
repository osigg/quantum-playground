from qiskit import QuantumCircuit


def simon_oracle(s: str) -> QuantumCircuit:
    """bit oracle which: U|x>|y> = |x> |y XOR f(x)>"""

    n = len(s) 
    qc = QuantumCircuit(2*n, name=f"U_f(s={s})")
    bits = s[::-1]

    # copy x onto output
    for i in range(n):
        qc.cx(i, n+i)

    # when x_j = 1, xor s into the output
    if "1" in bits:
        j = bits.index("1")
        for i in range(n):
            if bits[i] == "1":
                qc.cx(j, n+i)

    return qc