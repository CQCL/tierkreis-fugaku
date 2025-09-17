import os
from pathlib import Path
from time import time

from pytket.qasm.qasm import circuit_from_qasm
from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend

circuit_file = Path(__file__).parent.parent / "compiled_circuit.qasm"
circuit = circuit_from_qasm(circuit_file, maxwidth=1000)
start = time()
print(f"Started at {start}")
n_shots = 1000
print(n_shots)

print(os.environ.get("OMP_NUM_THREADS"))
results = QulacsBackend().run_circuits([circuit], n_shots, False)
print(results)
end = time()

print(f"Time taken: {end-start}")
