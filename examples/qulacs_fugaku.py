from pathlib import Path
from sys import argv
from typing import Literal
from uuid import UUID
from tierkreis import run_graph
from tierkreis.controller.data.models import OpaqueType
from tierkreis.storage import FileStorage, read_outputs  # type: ignore
from tierkreis.executor import UvExecutor, PJSUBExecutor, MultipleExecutor
from tierkreis.hpc import JobSpec, ResourceSpec, MpiSpec

from examples.qulacs_local import graph
from workers.consts import WORKERS_DIR

BackendResult = Literal[OpaqueType["pytket.backends.backendresult.BackendResult"]]


storage = FileStorage(UUID(int=105), do_cleanup=True)
uv = UvExecutor(WORKERS_DIR, storage.logs_path)


def pjsub_uv_executor(group_name: str, logs_path: Path) -> PJSUBExecutor:
    spec = JobSpec(
        job_name="tkr_symbolic_ciruits",
        account=group_name,
        command="env OMP_NUM_THREADS=10 UV_PROJECT_ENVIRONMENT=compute_venv uv run main.py",
        resource=ResourceSpec(nodes=5, memory_gb=None, gpus_per_node=None),
        walltime="00:15:00",
        mpi=MpiSpec(),
        output_path=Path(logs_path),
        error_path=Path(logs_path),
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
