from sys import argv
from typing import Sequence
from tierkreis import Worker
from pytket._tket.circuit import Circuit
from pytket.backends.backendresult import BackendResult
from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend

worker = Worker("qulacs")


@worker.task()
def compile(circuits: Sequence[Circuit], optimisation_level: int) -> list[Circuit]:
    return QulacsBackend().get_compiled_circuits(circuits, optimisation_level)


@worker.task()
def submit(circuits: Sequence[Circuit], n_shots: int) -> list[BackendResult]:
    return QulacsBackend().run_circuits(circuits, n_shots)


if __name__ == "__main__":
    worker.app(argv)
