# Updated imports for modern Qiskit
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator  # New package for simulators
import matplotlib.pyplot as plt
import numpy as np

def quantum_coin_toss(shots=1):
    """
    Perform a quantum coin toss using a Hadamard gate
    Returns: Dictionary with counts of 0 and 1 outcomes
    """
    # Create a quantum circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate to create superposition
    # |0⟩ → (|0⟩ + |1⟩)/√2
    qc.h(0)
    
    # Measure the qubit in computational basis
    qc.measure(0, 0)
    
    # Create a simulator
    simulator = AerSimulator()
    
    # Run the circuit on the simulator (new method in Qiskit 1.0+)
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    return counts

def biased_quantum_coin(bias_angle, shots=1000):
    """
    Create a biased quantum coin by applying Ry rotation.
    bias_angle: angle in radians to control bias
               0 = all 0s, π = all 1s, π/2 = fair coin
    """
    qc = QuantumCircuit(1, 1)
    
    # Apply Ry rotation for bias
    # Ry(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
    qc.ry(bias_angle, 0)
    
    # Measure the qubit
    qc.measure(0, 0)
    
    # Create a simulator
    simulator = AerSimulator()
    
    # Run the circuit (new method)
    job = simulator.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate probabilities
    prob_0 = counts.get('0', 0) / shots
    prob_1 = counts.get('1', 0) / shots
    
    return counts, prob_0, prob_1

# Execute a single fair coin toss
print("\n--- Fair Quantum Coin Toss ---")
result = quantum_coin_toss(shots=1)
print(f"Single toss result: {result}")

# Multiple tosses to show probability distribution
multi_results = quantum_coin_toss(shots=1000)
print(f"1000 tosses distribution: {multi_results}")

# Test with different bias values
print("\n--- Biased Quantum Coin ---")
for angle in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
    counts, p0, p1 = biased_quantum_coin(angle)
    print(f"Angle: {angle:.2f} radians")
    print(f"Counts: {counts}")
    print(f"Probability of 0: {p0:.4f}, Probability of 1: {p1:.4f}")
    print("-" * 30)

# Generate a visualization
def plot_bias_experiment():
    """
    Run experiments with different rotation angles and plot the results
    against theoretical predictions
    """
    angles = np.linspace(0, np.pi, 20)
    prob_ones = []
    
    for angle in angles:
        _, _, p1 = biased_quantum_coin(angle, shots=500)
        prob_ones.append(p1)
    
    plt.figure(figsize=(10, 6))
    plt.plot(angles, prob_ones, 'bo-', label='Experimental')
    plt.plot(angles, np.sin(angles/2)**2, 'r-', label='Theoretical: sin²(θ/2)')
    plt.xlabel('Rotation Angle (radians)')
    plt.ylabel('Probability of Measuring |1⟩')
    plt.title('Quantum Coin Bias vs. Rotation Angle')
    plt.grid(True)
    plt.legend()
    plt.savefig('quantum_coin_bias.png')
    print("\nPlot saved as 'quantum_coin_bias.png'")

print("\n--- Running Visualization Experiment ---")
plot_bias_experiment()