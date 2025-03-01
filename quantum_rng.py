from qiskit import QuantumCircuit, Aer, execute

def generate_random_bits(num_bits=8):
    # Create a circuit with num_bits qubits
    qc = QuantumCircuit(num_bits, num_bits)
    
    # Apply H-gate to all qubits
    for i in range(num_bits):
        qc.h(i)
    
    # Measure all qubits
    qc.measure(range(num_bits), range(num_bits))
    
    # Execute the circuit
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=1).result()
    counts = list(result.get_counts().keys())[0]
    
    # Convert binary string to integer
    random_number = int(counts, 2)
    
    return counts, random_number

# Generate 8-bit random number
binary, number = generate_random_bits(8)
print(f"Random 8-bit string: {binary}")
print(f"Random number (0-255): {number}")

# Generate multiple random numbers
print("\nGenerating 10 random numbers (0-255):")
for _ in range(10):
    _, num = generate_random_bits(8)
    print(num, end=" ")