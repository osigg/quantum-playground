from qiskit import QuantumCircuit


# the 4 possible functions for 2 qubit truth table
FUNCTIONS = {
    "constant_0": (0,0),
    "constant_1": (1,1),
    "identity": (0,1),
    "negation": (1,0),
}

def deutsch_oracle(name: str) -> QuantumCircuit:
    qc = QuantumCircuit(2, name=name)
    if name == "constant_0":
        pass                            # f(x) = 0, do nothing
    elif name == "constant_1":
        qc.x(1)                         # f(x) = 1, flip the output qubit
    elif name == "identity":
        qc.cx(0,1)                      # f(x) = x, flip y when x is 1
    elif name == "negation":
        qc.cx(0, 1)                     # f(x) = NOT x, flip y when x is 0
        qc.x(1)


    return qc