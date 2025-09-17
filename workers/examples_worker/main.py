from sys import argv
from tierkreis import Worker
from pytket._tket.circuit import Circuit

worker = Worker("examples_worker")


@worker.task()
def example_circuit_list() -> list[Circuit]:
    circ1 = Circuit(4)
    circ1.X(0)
    circ1.CX(1, 3)
    circ1.Z(3)

    circ2 = Circuit(2)
    circ2.Rx(0.5, 0)
    circ2.CRz(0.3, 1, 0)

    return [circ1, circ2] * 100


if __name__ == "__main__":
    worker.app(argv)
