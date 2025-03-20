"""
Quantum Coin Toss Implementation with Real-time Visualization
Optimized version with batched coin tosses for better efficiency
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np
import time
import argparse
import matplotlib.pyplot as plt

# Import our provider initialization and visualizer
from quantum_rings_provider import initialize_quantum_backend
from quantum_visualizer import QuantumVisualizer

def batched_quantum_coin_toss(batch_size, use_hardware=False):
    """
    Perform multiple quantum coin tosses using a single circuit
    
    Args:
        batch_size: Number of coin tosses to perform in this batch
        use_hardware: Whether to use the hardware accelerator backend
        
    Returns:
        list: List of 0s and 1s representing coin toss outcomes
    """
    # Initialize the backend
    backend = initialize_quantum_backend() if use_hardware else AerSimulator()
    
    # Create a quantum circuit with 1 qubit and batch_size classical bits
    qc = QuantumCircuit(1, batch_size)
    
    # Perform the tosses
    for i in range(batch_size):
        # Apply Hadamard gate to create superposition
        qc.h(0)
        
        # Measure the qubit into the current classical bit
        qc.measure(0, i)
        
        # Reset the qubit if this isn't the last toss
        if i < batch_size - 1:
            qc.reset(0)
    
    # Run the circuit
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Parse the bitstring (comes in reverse order)
    bit_string = list(counts.keys())[0]
    
    # Convert to list of integers
    toss_results = [int(bit) for bit in bit_string]
    
    return toss_results

def run_experiment(num_tosses=100, use_hardware=False, visualize=True, delay=0.1, batch_size=10):
    """
    Run a series of quantum coin tosses with batched circuits and visualization
    
    Args:
        num_tosses: Total number of coin tosses to perform
        use_hardware: Whether to use hardware acceleration
        visualize: Whether to show real-time visualization
        delay: Delay between visualization updates (seconds)
        batch_size: Number of tosses to include in each circuit
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
        print(f"Using batch size of {batch_size} tosses per circuit")
        
        # Process tosses in batches
        remaining_tosses = num_tosses
        while remaining_tosses > 0:
            # Determine current batch size
            current_batch = min(batch_size, remaining_tosses)
            
            # Get a batch of results
            batch_results = batched_quantum_coin_toss(current_batch, use_hardware)
            
            # Process each result for visualization
            for outcome in batch_results:
                results.append(outcome)
                
                # Update visualizer if available
                if visualizer:
                    visualizer.add_result(outcome)
                
            # Progress update
            tosses_done = len(results)
            if tosses_done % 10 == 0 or tosses_done == num_tosses:
                print(f"Completed {tosses_done}/{num_tosses} tosses")
            
            # Update remaining tosses
            remaining_tosses = num_tosses - len(results)
            
            # Small delay for visualization
            if visualize and delay > 0:
                plt.pause(delay)  # Force update the plot
    
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
            print("Visualization saved. Close the window to exit...")
            visualizer.stop_visualization()

if __name__ == "__main__":
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Quantum Coin Toss Simulator with Visualization')
    parser.add_argument('--tosses', type=int, default=100, help='Number of coin tosses to perform')
    parser.add_argument('--batch-size', type=int, default=10, help='Number of tosses per circuit')
    parser.add_argument('--hardware', action='store_true', help='Use hardware acceleration')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between tosses (seconds)')
    
    args = parser.parse_args()
    
    # Run the experiment
    run_experiment(
        num_tosses=args.tosses,
        use_hardware=args.hardware,
        visualize=not args.no_viz,
        delay=args.delay,
        batch_size=args.batch_size
    )