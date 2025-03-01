"""
Quantum Coin Toss Implementation with Real-time Visualization
This version adds a real-time visualization of the quantum coin tosses
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import time
import argparse

# Import our provider initialization and visualizer
from quantum_rings_provider import initialize_quantum_backend
from quantum_visualizer import QuantumVisualizer

def quantum_coin_toss(use_hardware=False, visualizer=None):
    """
    Perform a single quantum coin toss
    
    Args:
        use_hardware: Whether to use the hardware accelerator backend
        visualizer: Optional visualizer to update with results
        
    Returns:
        int: 0 or 1 representing the coin toss outcome
    """
    # Initialize the backend
    if use_hardware:
        # Get the "hardware" backend (simulated in this implementation)
        backend = initialize_quantum_backend()
    else:
        # Use regular Qiskit simulator
        backend = AerSimulator()
    
    # Create a quantum circuit for a single coin toss
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate to create superposition
    qc.h(0)
    
    # Measure the qubit
    qc.measure(0, 0)
    
    # Run the circuit
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Extract the result (either '0' or '1')
    outcome = list(counts.keys())[0]
    
    # Convert to integer
    result = int(outcome)
    
    # Update visualizer if provided
    if visualizer:
        visualizer.add_result(result)
    
    return result

def run_experiment(num_tosses=100, use_hardware=False, visualize=True, delay=0.1):
    """
    Run a series of quantum coin tosses with visualization
    
    Args:
        num_tosses: Number of coin tosses to perform
        use_hardware: Whether to use hardware acceleration
        visualize: Whether to show real-time visualization
        delay: Delay between tosses (seconds)
    """
    # Initialize visualizer if requested
    visualizer = None
    if visualize:
        visualizer = QuantumVisualizer()
        title = "Hardware-Accelerated Quantum Coin Toss" if use_hardware else "Quantum Coin Toss Simulation"
        visualizer.start_visualization(title=title)
    
    results = []
    hardware_label = "hardware" if use_hardware else "software"
    
    try:
        print(f"\nPerforming {num_tosses} quantum coin tosses using {hardware_label}...")
        
        for i in range(num_tosses):
            # Perform a single toss
            outcome = quantum_coin_toss(use_hardware, visualizer)
            results.append(outcome)
            
            # Progress update
            if (i+1) % 10 == 0:
                print(f"Completed {i+1}/{num_tosses} tosses")
            
            # Small delay for visualization
            if visualize and delay > 0:
                time.sleep(delay)
    
    except KeyboardInterrupt:
        print("\nExperiment interrupted by user")
    
    finally:
        # Calculate and display statistics
        if results:
            zeros = results.count(0)
            ones = results.count(1)
            total = len(results)
            
            print(f"\n==== Results Summary ====")
            print(f"Total tosses: {total}")
            print(f"Zeros (Heads): {zeros} ({zeros/total:.4f})")
            print(f"Ones (Tails): {ones} ({ones/total:.4f})")
            
            # Calculate bias from ideal
            bias = abs(ones/total - 0.5)
            print(f"Bias from ideal: {bias:.4f}")
            
            # Calculate runs
            run_lengths = []
            current_run = 1
            for i in range(1, len(results)):
                if results[i] == results[i-1]:
                    current_run += 1
                else:
                    run_lengths.append(current_run)
                    current_run = 1
            run_lengths.append(current_run)
            
            print(f"Longest run: {max(run_lengths)}")
            print(f"Average run length: {sum(run_lengths)/len(run_lengths):.2f}")
        
        # Save and close visualization
        if visualize and visualizer:
            filename = f"quantum_toss_{hardware_label}.png"
            visualizer.save_visualization(filename)
            time.sleep(1)  # Give time for save to complete
            visualizer.stop_visualization()

if __name__ == "__main__":
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Quantum Coin Toss Simulator with Visualization')
    parser.add_argument('--tosses', type=int, default=100, help='Number of coin tosses to perform')
    parser.add_argument('--hardware', action='store_true', help='Use hardware acceleration')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between tosses (seconds)')
    
    args = parser.parse_args()
    
    # Run the experiment
    run_experiment(
        num_tosses=args.tosses,
        use_hardware=args.hardware,
        visualize=not args.no_viz,
        delay=args.delay
    )