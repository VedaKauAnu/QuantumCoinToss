from quantum_visualizer import QuantumVisualizer
import time
import random

viz = QuantumVisualizer()
viz.start_visualization()

# Add some data manually
for i in range(10):
    viz.add_result(0)  # Add some zeros
    time.sleep(0.5)
for i in range(10):
    viz.add_result(1)  # Add some ones
    time.sleep(0.5)

# Keep the window open
input("Press Enter to close...")
viz.stop_visualization()