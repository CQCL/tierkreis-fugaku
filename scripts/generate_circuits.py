import json
from pathlib import Path
from pytket._tket.circuit import Circuit

REPO_DIR = Path(__file__).parent.parent


def get_circ_1() -> Circuit:
    circ = Circuit(4)
    circ.X(0)
    circ.CX(1, 3)
    circ.Z(3)
    return circ


def get_circ_2() -> Circuit:
    circ = Circuit(2)
    circ.Rx(0.5, 0)
    circ.CRz(0.3, 1, 0)
    return circ


FILES_FOR_CIRCUITS = [REPO_DIR / "workers" / "tkr_qulacs" / "test" / "circuits"]


def generate_list_of_circuits(circuits_path: Path):
    dict_1 = get_circ_1().to_dict()  # type: ignore
    dict_2 = get_circ_2().to_dict()  # type: ignore
    with open(circuits_path, "w+") as fh:
        json.dump([dict_1, dict_2], fh)


def generate_circuits():
    [generate_list_of_circuits(x) for x in FILES_FOR_CIRCUITS]


if __name__ == "__main__":
    generate_circuits()
