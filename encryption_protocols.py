from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import qiskit
import qiskit_aer
import numpy as np
import time


def rsa_encryption():
    start_time = time.time()
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    rsa_gen_time = time.time() - start_time

    message = "This is a test paragraph for RSA encryption. It is a very long message. And consists of multiple sentences. Please ignore the content."
    cipher = PKCS1_OAEP.new(RSA.import_key(public_key))
    start_time = time.time()
    encrypted_message = cipher.encrypt(message.encode())
    rsa_enc_time = time.time() - start_time

    cipher = PKCS1_OAEP.new(RSA.import_key(private_key))
    start_time = time.time()
    decrypted_message = cipher.decrypt(encrypted_message).decode()
    rsa_dec_time = time.time() - start_time

    return rsa_gen_time + rsa_enc_time


def bb84(n_bits=20):
    start_time = time.time()
    alice_bits = np.random.randint(2, size=n_bits)
    alice_bases = np.random.randint(2, size=n_bits)
    bob_bases = np.random.randint(2, size=n_bits)
    circuit = qiskit.QuantumCircuit(n_bits, n_bits)

    for i in range(n_bits):
        if alice_bases[i] == 1:
            circuit.h(i)
        if alice_bits[i] == 1:
            circuit.x(i)

    for i in range(n_bits):
        if bob_bases[i] == 1:
            circuit.h(i)
        circuit.measure(i, i)

    simulator = qiskit_aer.AerSimulator()
    result = simulator.run(circuit, shots=1000).result()
    measurements = result.get_counts(circuit)
    bob_bits = [int(bit) for bit in measurements][::-1]
    alice_key = [alice_bits[i] for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    bob_key = [bob_bits[i] for i in range(n_bits) if alice_bases[i] == bob_bases[i]]
    bb84_time = time.time() - start_time

    return bb84_time


def e91(n_pairs=10): 
    start_time = time.time()
    circuit = qiskit.QuantumCircuit(2 * n_pairs, 2 * n_pairs)

    for i in range(0, 2 * n_pairs, 2):
        circuit.h(i)
        circuit.cx(i, i + 1)

    angles_alice = np.pi / 4
    angles_bob = np.pi / 8

    for i in range(0, 2 * n_pairs, 2):
        circuit.ry(angles_alice, i)
        circuit.ry(angles_bob, i + 1)
        circuit.measure([i, i + 1], [i, i + 1])

    simulator = qiskit_aer.AerSimulator(
        method="automatic"
    )  # Use the automatic method to let Aer choose the best simulation method
    result = simulator.run(circuit, shots=1000).result()
    measurements = result.get_counts(circuit)
    e91_time = time.time() - start_time

    return e91_time
