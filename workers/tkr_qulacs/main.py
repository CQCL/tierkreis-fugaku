import os
from sys import argv
from typing import Sequence
from tierkreis import Worker
from pytket._tket.circuit import Circuit
from pytket.backends.backendresult import BackendResult
from pytket.extensions.qulacs.backends.qulacs_backend import QulacsBackend

worker = Worker("tkr_qulacs")


@worker.task()
def compile(circuits: Sequence[Circuit], optimisation_level: int) -> list[Circuit]:
    print(os.environ.get("OMP_NUM_THREADS"))
    return QulacsBackend().get_compiled_circuits(circuits, optimisation_level)


@worker.task()
def submit(circuits: Sequence[Circuit], n_shots: int) -> list[BackendResult]:
    print(os.environ.get("OMP_NUM_THREADS"))
    return QulacsBackend().run_circuits(circuits, n_shots, False)


if __name__ == "__main__":
    worker.app(argv)
