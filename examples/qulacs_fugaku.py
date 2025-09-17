import os
from pathlib import Path
from sys import argv
from typing import Literal
from uuid import UUID
from tierkreis import run_graph
from tierkreis.controller import resume_graph
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
storage = FileStorage(UUID(int=105))
uv = UvExecutor(WORKERS_DIR, storage.logs_path)
command = (
    ". /vol0004/apps/oss/spack/share/spack/setup-env.sh && "
    "spack load /slvpnrm && "  # load boost@1.83.0%fj@4.10.0 arch=linux-rhel8-a64fx
    "OMP_NUM_THREADS=12 UV_PROJECT_ENVIRONMENT=compute_venv mpiexec -np ${PJM_MPI_PROC} uv run main.py"
)


def graph():
    g = GraphBuilder(EmptyModel, TKR[list[BackendResult]])
    circuits = g.task(example_circuit_list())
    compiled_circuits = g.task(compile(circuits, g.const(2)))
    results = g.task(submit(compiled_circuits, g.const(10000)))
    g.outputs(results)
    return g


def pjsub_uv_executor(group_name: str, logs_path: Path) -> PJSUBExecutor:
    spec = JobSpec(
        job_name="tkr_symbolic_ciruits",
        account=group_name,
        command=command,
        resource=ResourceSpec(nodes=1, memory_gb=None, gpus_per_node=None),
        walltime="00:15:00",
        mpi=MpiSpec(max_proc_per_node=4),
        output_path=Path("./output"),
        error_path=Path("./errors"),
        environment={"PJM_LLIO_GFSCACHE": "/vol0004"},
        include_no_check_directory_flag=True,
    )
    return PJSUBExecutor(WORKERS_DIR, logs_path, spec)


def main(group_name: str, resume: bool):
    executor = MultipleExecutor(
        uv,
        {"pjsub": pjsub_uv_executor(group_name, storage.logs_path)},
        {"tkr_qulacs": "pjsub"},
    )
    if resume:
        resume_graph(storage, executor, polling_interval_seconds=2)
    else:
        storage.clean_graph_files()
        run_graph(storage, executor, graph().get_data(), {}, polling_interval_seconds=2)
    print(len(read_outputs(graph().get_data(), storage)))  # type: ignore


if __name__ == "__main__":
    resume = False if len(argv) < 3 else argv[2].lower() == "true"
    main(argv[1], resume)
