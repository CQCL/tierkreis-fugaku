from pathlib import Path
from sys import argv
from typing import Literal
from uuid import UUID
from tierkreis import run_graph
from tierkreis.controller.data.models import OpaqueType
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from tierkreis.executor import UvExecutor, PJSUBExecutor, MultipleExecutor
from tierkreis.hpc import JobSpec, ResourceSpec, MpiSpec
from tierkreis.builder import GraphBuilder
from tierkreis.models import EmptyModel, TKR

from workers.consts import WORKERS_DIR
from workers.examples_worker.stubs import example_circuit_list
from workers.tkr_qulacs.stubs import compile, submit

BackendResult = Literal[OpaqueType["pytket.backends.backendresult.BackendResult"]]


def graph():
    g = GraphBuilder(EmptyModel, TKR[list[BackendResult]])
    circuits = g.task(example_circuit_list())
    compiled_circuits = g.task(compile(circuits, g.const(2)))
    results = g.task(submit(compiled_circuits, g.const(30)))
    g.outputs(results)
    return g


storage = FileStorage(UUID(int=105), do_cleanup=True)
uv = UvExecutor(WORKERS_DIR, storage.logs_path)

command = (
    "export PJM_LLIO_GFSCACHE=/vol0004 && "
    ". /vol0004/apps/oss/spack/share/spack/setup-env.sh && "
    "spack load boost && "
    "env OMP_NUM_THREADS=10 UV_PROJECT_ENVIRONMENT=compute_venv uv run main.py"
)


def pjsub_uv_executor(group_name: str, logs_path: Path) -> PJSUBExecutor:
    spec = JobSpec(
        job_name="tkr_symbolic_ciruits",
        account=group_name,
        command=command,
        resource=ResourceSpec(nodes=5, memory_gb=None, gpus_per_node=None),
        walltime="00:15:00",
        mpi=MpiSpec(),
        output_path=Path(logs_path),
        error_path=Path(logs_path),
        environment={"PJM_LLIO_GFSCACHE": "/vol0004"},
        include_no_check_directory_flag=True,
    )
    return PJSUBExecutor(WORKERS_DIR, logs_path, spec)


def main(group_name: str):
    executor = MultipleExecutor(
        uv,
        {"pjsub": pjsub_uv_executor(group_name, storage.logs_path)},
        {"tkr_qulacs": "pjsub"},
    )
    run_graph(storage, executor, graph().get_data(), {})
    result = read_outputs(graph().get_data(), storage)
    print(result)


if __name__ == "__main__":
    main(argv[1])
