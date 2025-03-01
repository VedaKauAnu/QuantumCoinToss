import matplotlib.pyplot as plt
import numpy as np
from qiskit import QuantumCircuit, Aer, execute

def run_experiment(num_angles=10, shots_per_angle=1000):
    angles = np.linspace(0, np.pi, num_angles)
    prob_ones = []
    
    for angle in angles:
        qc = QuantumCircuit(1, 1)
        qc.ry(angle, 0)
        qc.measure(0, 0)
        
        simulator = Aer.get_backend('qasm_simulator')
        result = execute(qc, simulator, shots=shots_per_angle).result()
        counts = result.get_counts()
        
        # Calculate probability of measuring 1
        prob_1 = counts.get('1', 0) / shots_per_angle
        prob_ones.append(prob_1)
    
    return angles, prob_ones

# Run the experiment
angles, prob_ones = run_experiment()

# Plot the results
plt.figure(figsize=(10, 6))
plt.plot(angles, prob_ones, 'bo-')
plt.plot(angles, np.sin(angles/2)**2, 'r-', label='Theoretical: sin²(θ/2)')
plt.xlabel('Rotation Angle (radians)')
plt.ylabel('Probability of Measuring |1⟩')
plt.title('Quantum Coin Bias vs. Rotation Angle')
plt.grid(True)
plt.legend()
plt.savefig('quantum_coin_bias.png')
plt.show()