#!/usr/bin/env bash

input_nqubits_value=$(cat $input_nqubits_file)
input_nshots_value=$(cat $input_nshots_file)
input_iformat_value=$(cat $input_iformat_file)
input_oformat_value=$(cat $input_oformat_file)
input_qpu_value=$(cat $input_qpu_file)

sqcsub --nqubits $input_nqubits_value \
    --nshots $input_nshots_value \
    --ifile $input_ifile_file \
    --iformat $input_iformat_value \
    --ofile $output_value_file \
    --oformat $input_oformat_value \
    --qpu $input_qpu_value