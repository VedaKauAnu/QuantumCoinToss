import numpy as np
from qiskit import QuantumCircuit, Aer, execute

def biased_quantum_coin(bias_angle, shots=1000):
    """
    Create a biased quantum coin by applying Ry rotation.
    bias_angle: angle in radians to control bias
                0 = all 0s, π = all 1s, π/2 = fair coin
    """
    qc = QuantumCircuit(1, 1)
    
    # Apply Ry rotation for bias
    qc.ry(bias_angle, 0)
    
    # Measure
    qc.measure(0, 0)
    
    # Run simulation
    simulator = Aer.get_backend('qasm_simulator')
    result = execute(qc, simulator, shots=shots).result()
    counts = result.get_counts()
    
    # Calculate probabilities
    prob_0 = counts.get('0', 0) / shots
    prob_1 = counts.get('1', 0) / shots
    
    return counts, prob_0, prob_1

# Test with different bias values
for angle in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
    counts, p0, p1 = biased_quantum_coin(angle)
    print(f"Angle: {angle:.2f} radians")
    print(f"Counts: {counts}")
    print(f"Probability of 0: {p0:.4f}, Probability of 1: {p1:.4f}")
    print("-" * 30)