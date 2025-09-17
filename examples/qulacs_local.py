from typing import Literal
from uuid import UUID
from tierkreis import run_graph
from tierkreis.builder import GraphBuilder
from tierkreis.models import EmptyModel, TKR
from tierkreis.controller.data.models import OpaqueType
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from tierkreis.executor import UvExecutor

from workers.consts import WORKERS_DIR
from workers.examples_worker.stubs import example_circuit_list
from workers.tkr_qulacs.stubs import compile, submit

BackendResult = Literal[OpaqueType["pytket.backends.backendresult.BackendResult"]]
storage = FileStorage(UUID(int=105), do_cleanup=True)
executor = UvExecutor(WORKERS_DIR, storage.logs_path)


def graph():
    g = GraphBuilder(EmptyModel, TKR[list[BackendResult]])
    circuits = g.task(example_circuit_list())
    compiled_circuits = g.task(compile(circuits, g.const(1)))
    results = g.task(submit(compiled_circuits, g.const(10000)))
    g.outputs(results)
    return g


if __name__ == "__main__":
    run_graph(storage, executor, graph().get_data(), {}, polling_interval_seconds=0.1)
    print(len(read_outputs(graph().get_data(), storage)))  # type: ignore
