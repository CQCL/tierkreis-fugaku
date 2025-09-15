interface sqcsub {
    submit(
        nqubits: integer,
        nshots: integer,
        ifile: bytes,
        iformat: string,
        oformat: string,
        qpu: string,
    ): bytes;
}
