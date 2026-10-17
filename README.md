# quantum-playground

Quantum algorithms and their Oracles implemented from scratch in Qiskit. Every oracle and diffuser is built
gate by gate so the mechanism is visible, and every oracle is checked against its unitary matrix.

## Algorithms

| Folder | Problem | Speedup | Verified result |
|---|---|---|---|
| [`grover/`](grover/) | Find a marked item among N = 2^n | ~sqrt(N) queries vs N/2 | `1010`: 92.3%|
| [`deutsch/`](deutsch/) | Is f: {0,1} -> {0,1} constant or balanced? | 1 query vs 2 | Correct on all 4 oracles, 1024/1024 shots |

## Setup

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Use `python -m pip`, not bare `pip`. If Anaconda's `(base)` is also active,
bare `pip` installs into conda instead of the venv.

## Running

```powershell
cd grover
python grover.py
```

## Layout

Each algorithm gets its own folder with two files:

- `oracle.py`: the problem (the black-box function being queried)
- `<algorithm>.py`: the method that solves it

```
quantum-playground/
  grover/     oracle.py, grover.py
  deutsch/    oracle.py, deutsch.py
```

## Notes

- **Endianness.** Qiskit's qubit 0 is the rightmost bit of a bitstring, so
  oracles reverse the target. Palindromes like `101` hide this bug; tests use
  asymmetric targets like `1010`.
- **Oracle check.** A correct phase oracle is diagonal with +-1 entries, -1
  only at the target. An all-zero diagonal means an X gate was never uncomputed.

## Roadmap

Simon next, then QFT/QPE, and Shor.
Longer term: randomized benchmarking and error-correction experiments.