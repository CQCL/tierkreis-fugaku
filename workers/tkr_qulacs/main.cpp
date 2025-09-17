#include <iostream>
#include <cppsim/state.hpp>
#include <cppsim/circuit.hpp>
#include <cppsim/observable.hpp>
#include <cppsim/gate_factory.hpp>
#include <cppsim/gate_merge.hpp>

int main(){
    QuantumState state(2);
    state.set_computational_basis(0b00);

    QuantumCircuit circuit(2);
    circuit.add_H_gate(0);
    circuit.add_CNOT_gate(0,1);
    circuit.update_quantum_state(&state);

    std::cout << state << std::endl;

    Observable observable(2);
    observable.add_operator(1.0, "Z 1 X 0");

    auto value = observable.get_expectation_value(&state);
    std::cout << value << std::endl;

    return 0;
}
