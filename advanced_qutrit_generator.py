"""
Advanced Quantum Random Number Generator - Qiskit Version with Visualization
This implements a simulated version of higher-dimensional quantum systems
with real-time visualization of the qutrit measurements
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
import time
import argparse

# Import our provider initialization and visualizer
from quantum_rings_provider import initialize_quantum_backend
from quantum_visualizer import QuantumVisualizer

def generate_single_qutrit(use_hardware=False):
    """
    Generate a single qutrit random value in {0,1,2}
    
    Args:
        use_hardware: Whether to use hardware acceleration
        
    Returns:
        int: Random value in {0,1,2}
    """
    # Choose the backend
    if use_hardware:
        backend = initialize_quantum_backend()
    else:
        backend = AerSimulator()
    
    # Create a circuit with 2 qubits to simulate a qutrit
    qc = QuantumCircuit(2, 2)
    
    # Apply Hadamard gates to create superposition
    qc.h(0)
    qc.h(1)
    
    # Measure both qubits
    qc.measure([0, 1], [0, 1])
    
    # Run the circuit
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Get the binary outcome (e.g., '00', '01', '10', or '11')
    outcome = list(counts.keys())[0]
    
    # Map the 2-qubit state to a value in {0,1,2}
    # We'll map: '00' -> 0, '01' -> 1, '10' -> 2, '11' -> 0 (recycled)
    if outcome == '00':
        qutrit_value = 0
    elif outcome == '01':
        qutrit_value = 1
    elif outcome == '10':
        qutrit_value = 2
    else:  # '11'
        qutrit_value = 0  # Recycle as 0 to simulate a 3-level system
    
    return qutrit_value

def run_experiment(num_samples=100, use_hardware=False, visualize=True, delay=0.1):
    """
    Run a qutrit random number generation experiment with visualization
    
    Args:
        num_samples: Number of qutrit values to generate
        use_hardware: Whether to use hardware acceleration
        visualize: Whether to show real-time visualization
        delay: Delay between measurements (seconds)
    """
    # Initialize visualizer if requested
    visualizer = None
    if visualize:
        visualizer = QuantumVisualizer()
        title = "Hardware-Accelerated Qutrit Generator" if use_hardware else "Qutrit Generator Simulation"
        # Indicate this is for qutrit visualization (3-level system)
        visualizer.start_visualization(title=title, is_qutrit=True)
    
    results = []
    hardware_label = "hardware" if use_hardware else "software"
    
    try:
        print(f"\nGenerating {num_samples} qutrit random values using {hardware_label}...")
        
        for i in range(num_samples):
            # Generate a single qutrit value
            outcome = generate_single_qutrit(use_hardware)
            results.append(outcome)
            
            # Update visualizer if available
            if visualizer:
                visualizer.add_result(outcome)
            
            # Progress update
            if (i+1) % 10 == 0:
                print(f"Completed {i+1}/{num_samples} measurements")
            
            # Small delay for visualization
            if visualize and delay > 0:
                time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\nExperiment interrupted by user")
    
    finally:
        # Calculate and display statistics
        if results:
            analyze_results(results)
        
        # Save and close visualization
        if visualize and visualizer:
            filename = f"qutrit_generator_{hardware_label}.png"
            visualizer.save_visualization(filename)
            time.sleep(1)  # Give time for save to complete
            visualizer.stop_visualization()

def analyze_results(results):
    """
    Analyze the qutrit measurement results
    
    Args:
        results: List of qutrit values (0, 1, or 2)
    """
    # Count occurrences
    zeros = results.count(0)
    ones = results.count(1)
    twos = results.count(2)
    total = len(results)
    
    print(f"\n==== Results Summary ====")
    print(f"Total measurements: {total}")
    print(f"Value 0: {zeros} ({zeros/total:.4f})")
    print(f"Value 1: {ones} ({ones/total:.4f})")
    print(f"Value 2: {twos} ({twos/total:.4f})")
    
    # Calculate bias from ideal (should be 1/3 for each outcome)
    bias_0 = abs(zeros/total - 1/3)
    bias_1 = abs(ones/total - 1/3)
    bias_2 = abs(twos/total - 1/3)
    avg_bias = (bias_0 + bias_1 + bias_2) / 3
    
    print(f"\nBias Analysis:")
    print(f"Value 0 bias: {bias_0:.4f}")
    print(f"Value 1 bias: {bias_1:.4f}")
    print(f"Value 2 bias: {bias_2:.4f}")
    print(f"Average bias: {avg_bias:.4f}")
    
    # Calculate runs
    run_lengths = []
    current_run = 1
    
    for i in range(1, len(results)):
        if results[i] == results[i-1]:
            current_run += 1
        else:
            run_lengths.append(current_run)
            current_run = 1
    
    # Add the last run
    run_lengths.append(current_run)
    
    print(f"\nRun Analysis:")
    print(f"Longest run: {max(run_lengths)}")
    print(f"Average run length: {sum(run_lengths)/len(run_lengths):.2f}")
    
    # Theoretical average run length for fair qutrit should be 1.5
    theoretical_avg = 1.5
    run_deviation = abs(sum(run_lengths)/len(run_lengths) - theoretical_avg)
    print(f"Run length deviation from theoretical: {run_deviation:.4f}")

if __name__ == "__main__":
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Quantum Qutrit Generator with Visualization')
    parser.add_argument('--samples', type=int, default=100, help='Number of qutrit values to generate')
    parser.add_argument('--hardware', action='store_true', help='Use hardware acceleration')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between measurements (seconds)')
    
    args = parser.parse_args()
    
    # Run the experiment
    run_experiment(
        num_samples=args.samples,
        use_hardware=args.hardware,
        visualize=not args.no_viz,
        delay=args.delay
    )