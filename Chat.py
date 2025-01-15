from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram

def generate_quantum_key(length=10):
    key = ""
    simulator = AerSimulator()
    
    for _ in range(length):
        # Quantum circuit for key generation
        circuit = QuantumCircuit(2, 2)
        circuit.h(0)  # Hadamard gate to create superposition
        circuit.cx(0, 1)  # CNOT gate to entangle
        circuit.measure([0, 1], [0, 1])  # Measure to collapse the state
        
        # Run the circuit on the simulator
        result = simulator.run(circuit, shots=1).result()
        counts = result.get_counts(circuit)
        
        # Extract a bit from the measurement result to form the key
        measured_bit = list(counts.keys())[0][0]  # Taking the first bit of the first key
        key += measured_bit
        
    return key

def xor_encrypt_decrypt(message, key):
    encrypted_decrypted_chars = []
    for i in range(len(message)):
        key_char = key[i % len(key)]
        encrypted_decrypted_char = chr(ord(message[i]) ^ ord(key_char))
        encrypted_decrypted_chars.append(encrypted_decrypted_char)
    return ''.join(encrypted_decrypted_chars)

key = generate_quantum_key(10)
print(f"Generated key: {key}")

message = "Hello, Bob!"
encrypted_message = xor_encrypt_decrypt(message, key)
print(f"Encrypted message: {encrypted_message}")

decrypted_message = xor_encrypt_decrypt(encrypted_message, key)
print(f"Decrypted message: {decrypted_message}")
