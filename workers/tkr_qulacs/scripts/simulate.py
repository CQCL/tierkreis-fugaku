from pathlib import Path
from time import time

from pytket.qasm.qasm import circuit_from_qasm
from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend

circuit_file = Path(__file__).parent.parent / "compiled_circuit.qasm"
circuit = circuit_from_qasm(circuit_file, maxwidth=100)
start = time()
print(f"Started at {start}")
compiled_circuit = QulacsBackend().run_circuits([circuit], 1)
end = time()

print(f"Time taken: {end-start}")
