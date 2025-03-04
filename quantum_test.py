# Save as quantum_test.py
import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Run 20 actual quantum tosses
results = []
simulator = AerSimulator()

for _ in range(20):
    # Create the quantum circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate
    qc.measure(0, 0)
    
    # Run on simulator
    job = simulator.run(qc, shots=1)
    outcome = list(job.result().get_counts().keys())[0]
    result = int(outcome)
    results.append(result)
    print(f"Quantum toss result: {result}")

# Plot the results (basic bar chart)
plt.figure(figsize=(8, 6))
plt.bar(['0 (Heads)', '1 (Tails)'], [results.count(0), results.count(1)])
plt.title("Quantum Coin Toss Results")
plt.savefig("quantum_test_results.png")
plt.show()