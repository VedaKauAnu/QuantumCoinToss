from QuantumRingsLib.core import QuantumSimulator
from QuantumRingsLib.gates import HadamardGate, MeasurementGate

def quantum_rings_coin_toss(num_tosses=1):
    # Initialize the simulator
    simulator = QuantumSimulator(num_qubits=1)
    
    results = []
    for _ in range(num_tosses):
        # Reset to initial state |0⟩
        simulator.reset()
        
        # Apply Hadamard gate
        simulator.apply_gate(HadamardGate(), qubit_indices=[0])
        
        # Measure the qubit
        result = simulator.measure(qubit_indices=[0])
        results.append(result[0])  # Get the first qubit's measurement
    
    return results

# Execute 10 coin tosses
tosses = quantum_rings_coin_toss(10)
print(f"10 quantum coin tosses: {tosses}")

# Calculate statistics
zeros = tosses.count(0)
ones = tosses.count(1)
print(f"Zeros: {zeros}, Ones: {ones}")