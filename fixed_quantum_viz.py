# Save as fixed_quantum_viz.py
from quantum_visualizer import QuantumVisualizer
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import matplotlib.pyplot as plt
import time

# Create visualizer
viz = QuantumVisualizer()
viz.start_visualization()

# Run 20 actual quantum tosses
simulator = AerSimulator()

for i in range(20):
    # Create quantum circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate
    qc.measure(0, 0)
    
    # Run on simulator
    job = simulator.run(qc, shots=1)
    outcome = list(job.result().get_counts().keys())[0]
    result = int(outcome)
    
    # Add to visualizer
    viz.add_result(result)
    print(f"Quantum toss {i+1}: {result}")
    
    # Force render update
    plt.pause(0.3)

# Save visualization
print("Saving visualization...")
viz.save_visualization("fixed_quantum_viz.png")

# Keep window open
input("Press Enter to close...")