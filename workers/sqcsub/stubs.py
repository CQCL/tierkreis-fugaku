"""Code generated from sqcsub namespace. Please do not edit."""

from typing import NamedTuple
from tierkreis.controller.data.models import TKR


class submit(NamedTuple):
    nqubits: TKR[int]  # noqa: F821 # fmt: skip
    nshots: TKR[int]  # noqa: F821 # fmt: skip
    ifile: TKR[bytes]  # noqa: F821 # fmt: skip
    iformat: TKR[str]  # noqa: F821 # fmt: skip
    oformat: TKR[str]  # noqa: F821 # fmt: skip
    qpu: TKR[str]  # noqa: F821 # fmt: skip

    @staticmethod
    def out() -> type[TKR[bytes]]:  # noqa: F821 # fmt: skip
        return TKR[bytes]  # noqa: F821 # fmt: skip

    @property
    def namespace(self) -> str:
        return "sqcsub"
