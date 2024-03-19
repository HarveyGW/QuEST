from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

# Create a Quantum Circuit acting on a quantum register of two qubits
circuit = QuantumCircuit(2, 2)

# Apply a Hadamard gate to qubit 0. This puts it into a superposition state.
circuit.h(0)

# Apply a CNOT gate controlled by qubit 0 and targeted on qubit 1. This entangles them.
circuit.cx(0, 1)

# Map the quantum measurement to the classical bits
circuit.measure([0, 1], [0, 1])

# Use Aer's qasm_simulator
simulator = AerSimulator()

# Execute the circuit on the qasm simulator
result = simulator.run(circuit, shots=1000).result()

# Returns counts
counts = result.get_counts(circuit)
print("\nTotal count for 00 and 11 are:", counts)

# Plot a histogram
plot_histogram(counts)
