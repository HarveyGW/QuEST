from qiskit import QuantumCircuit, execute, Aer
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import random_statevector
import numpy as np

def generate_entangled_pairs(bits):
    """Generate a list of entangled qubit pairs."""
    circuit = QuantumCircuit(2 * bits, 2 * bits)
    
    for i in range(bits):
        # Generate EPR pair
        circuit.h(i)
        circuit.cx(i, i + bits)
        
    return circuit

def measure_in_basis(circuit, bits, basis):
    """Measure qubits in the specified basis."""
    for i in range(2 * bits):
        if basis[i] == 'X':
            circuit.h(i)  # Change to X basis
        circuit.measure(i, i)

def shared_secret_key(bits=10):
    # Step 1: Generate entangled qubits
    entangled_circuit = generate_entangled_pairs(bits)
    
    # Step 2: Decide on measurement basis (same for simplicity)
    basis = ['Z' if np.random.rand() > 0.5 else 'X' for _ in range(2 * bits)]
    
    # Step 3: Add measurements to the circuit
    measure_in_basis(entangled_circuit, bits, basis)
    
    # Execute the circuit
    backend = Aer.get_backend('qasm_simulator')
    result = execute(entangled_circuit, backend, shots=1).result()
    counts = result.get_counts()
    
    # The measurement result is our shared secret key
    measurement_result = list(counts.keys())[0]
    
    # Split the key between Alice and Bob
    alice_key = measurement_result[:bits]
    bob_key = measurement_result[bits:]
    
    return alice_key, bob_key, basis

# Generate a shared secret key
alice_key, bob_key, basis = shared_secret_key()
print(f"Alice's key: {alice_key}")
print(f"Bob's key: {bob_key}")
print(f"Measurement Basis: {basis}")
