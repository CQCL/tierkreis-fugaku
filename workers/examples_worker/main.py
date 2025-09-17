from pathlib import Path
from sys import argv
from tierkreis import Worker
from pytket._tket.circuit import Circuit
from pytket.qasm.qasm import circuit_from_qasm

worker = Worker("examples_worker")


@worker.task()
def example_circuit_list() -> list[Circuit]:
    circ1 = Circuit(4)
    circ1.X(0)
    circ1.CX(1, 3)
    circ1.Z(3)

    circ2 = circuit_from_qasm(Path(__file__).parent / "circuit.qasm")

    return [circ2]


if __name__ == "__main__":
    worker.app(argv)
