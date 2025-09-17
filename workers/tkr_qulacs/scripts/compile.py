from pathlib import Path

from pytket.qasm.qasm import circuit_from_qasm, circuit_to_qasm
from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend

circuit_file = Path(__file__).parent.parent / "circuit.qasm"
circuit = circuit_from_qasm(circuit_file, maxwidth=100)

compiled_circuit = QulacsBackend().get_compiled_circuit(circuit, 2)
compiled_file = Path(__file__).parent.parent / "compiled_circuit.qasm"

circuit_to_qasm(compiled_circuit, str(compiled_file), maxwidth=100)
