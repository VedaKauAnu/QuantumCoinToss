# Save as simple_test.py
from quantum_visualizer import QuantumVisualizer
import time
import random
import matplotlib.pyplot as plt  # Add this import

# Create visualizer
viz = QuantumVisualizer()
viz.start_visualization()

# Add results one by one
for i in range(20):
    result = random.randint(0, 1)
    viz.add_result(result)
    print(f"Added result: {result}")
    plt.pause(0.5)  # Force update

print("Test complete")
plt.pause(10)  # Keep window open for 10 seconds