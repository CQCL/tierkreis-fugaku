interface sqcsub {
    submit(
        nqubits: integer,
        nshots: integer,
        ifile: string,
        iformat: string,
        ofile: string,
        oformat: string,
        qpu: string,
    ): bytes;
}
