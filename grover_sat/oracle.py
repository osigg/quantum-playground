from qiskit import QuantumCircuit

""" checker oracle from grovers algorithm on a small 3-SAT formula """


VARIABLES = ["a", "b", "c"]

CLAUSES = [
    [("a", True), ("b", True)],             # a or b
    [("a", False), ("c", True)],            # NOT a OR c
    [("b", False), ("c", False)],           # NOT b OR NOT c
]

def var_qubit(var):
    """ map a variables to its qubit 
        allows to measure bitstrings as "abc"

        *qubit 0 is rightmost bit
    
    """
    return len(VARIABLES) - VARIABLES.index(var) - 1


def num_qubits():
    """ number of qubits needed for the oracle """
    return len(VARIABLES) + len(CLAUSES) + 1  # variables + clauses + output qubit

def evaluate(bits):
    """ does abc satisfy formula?? """
    values = {v: bits[i] == "1" for i, v in enumerate(VARIABLES)}
    return all(any(values[v] == pos for v, pos in clause) for clause in CLAUSES)

def compute_clauses(qc, clause, ancilla):
    """ transforms OR using De Morgan's law into AND and NOT gates"""
    controls = [var_qubit(v) for v, _ in clause]
    flips = [var_qubit(v) for v, pos in clause if pos]

    for q in flips:
        qc.x(q)
    qc.mcx(controls, ancilla)       # ancilla = AND of all variables in clause
    qc.x(ancilla)                   # ancilla = NOT of AND = OR of all variables in clause
    for q in flips:
        qc.x(q)

def checker_oracle(uncompute=True):
    """ phase oracle for the 3-SAT formula """
    n, m = len(VARIABLES), len(CLAUSES)
    ancillas = list(range(n, n + m))    # ancilla qubits for each clause
    output = n+m                        # output qubit for the oracle

    qc = QuantumCircuit(num_qubits(), name="checker")

    #1 compute each clasue onto ancilla
    for clause, anc in zip(CLAUSES, ancillas):
        compute_clauses(qc, clause, anc)

    #2 copy AND of all clauses onto output qubit
    qc.mcx(ancillas, output)

    #3 uncompute each clause to reset ancilla qubits
    if uncompute:
        for clause, anc in reversed(list(zip(CLAUSES, ancillas))):
            compute_clauses(qc, clause, anc)

    return qc


def check_oracle():
    """ test the oracle by checking all possible bitstrings """
    from qiskit.quantum_info import Statevector

    n = len(VARIABLES)
    oracle = checker_oracle()
    failures = []

    for i in range(2**n):
        bits = format(i, f"0{n}b")
        qc = QuantumCircuit(num_qubits())
        for v, bit in zip(VARIABLES, bits):
            if bit == "1":
                qc.x(var_qubit(v))
        qc.compose(oracle, inplace=True)

        # classical input --> result single basis state
        out = Statevector(qc).probabilities_dict()
        (state,) = [s for s, p in out.items() if p > 0.5]
        
        # output is: 'out anc abc'
        got_anc = state[1:1+len(CLAUSES)]
        got_out = state[0]
        got_in = state[1+len(CLAUSES):]
        want_out = "1" if evaluate(bits) else "0"

        if got_in != bits or got_anc != "0" * len(CLAUSES) or got_out != want_out:
            failures.append((bits, state))
        
    return failures


if __name__ == "__main__":
    fails = check_oracle()
    print("oracle check:", "PASS" if not fails else f"FAIL {fails}")
    print("satisfying:", [format(i, "03b") for i in range(8) if evaluate(format(i, "03b"))])
