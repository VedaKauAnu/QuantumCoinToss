"""
Error-Mitigated Quantum Coin Implementation with Real-time Visualization
This version includes real-time visualization of both raw and mitigated results
"""
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_aer.noise import NoiseModel
import matplotlib.pyplot as plt
import numpy as np
import time
import argparse
import threading

# Import our provider initialization
from quantum_rings_provider import initialize_quantum_backend
from quantum_visualizer import QuantumVisualizer

def create_noise_model(error_rate=0.05):
    """
    Create a simple noise model to simulate quantum hardware noise
    """
    from qiskit.quantum_info import Kraus
    from qiskit_aer.noise import NoiseModel, QuantumError
    
    # Create bit flip error
    # For a bit flip with probability p, we have these Kraus operators:
    # K0 = sqrt(1-p) * identity, K1 = sqrt(p) * X gate
    p = error_rate
    k0 = [[1-p, 0], [0, 1-p]]
    k1 = [[0, p], [p, 0]]
    
    # Create the quantum error
    kraus_ops = [k0, k1]
    error = QuantumError(Kraus(kraus_ops))
    
    # Create a noise model using this error
    noise_model = NoiseModel()
    noise_model.add_all_qubit_quantum_error(error, ["measure"])
    
    return noise_model

def single_coin_toss(backend, with_mitigation=False):
    """
    Perform a single quantum coin toss
    
    Args:
        backend: Quantum backend to use
        with_mitigation: Whether to use error mitigation
        
    Returns:
        int: Result of the coin toss (0 or 1)
    """
    # Create quantum circuit
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate
    qc.measure(0, 0)  # Measurement
    
    if with_mitigation:
        # Run with 5 shots for error mitigation via repetition
        job = backend.run(qc, shots=5)
        result = job.result()
        counts = result.get_counts()
        
        # Majority vote (basic error mitigation technique)
        if '0' in counts and '1' in counts:
            if counts.get('0', 0) > counts.get('1', 0):
                return 0
            else:
                return 1
        else:
            # Only one outcome was measured
            outcome = list(counts.keys())[0]
            return int(outcome)
    else:
        # Standard single shot for raw result
        job = backend.run(qc, shots=1)
        result = job.result()
        counts = result.get_counts()
        outcome = list(counts.keys())[0]
        return int(outcome)

def run_experiment(num_tosses=100, use_hardware=False, error_rate=0.05, 
                  visualize=True, delay=0.1):
    """
    Run a complete experiment with simulated noise
    """
    # Initialize backend
    backend = initialize_quantum_backend() if use_hardware else AerSimulator()
    print(f"Using {'hardware (simulated)' if use_hardware else 'software'} simulation")
    
    # Initialize visualizers if requested
    raw_visualizer = None
    mitigated_visualizer = None
    
    if visualize:
        raw_visualizer = QuantumVisualizer()
        raw_title = "Raw Quantum Coin Tosses"
        
        mitigated_visualizer = QuantumVisualizer()
        mitigated_title = "Error-Mitigated Quantum Coin Tosses"
        
        raw_visualizer.start_visualization(raw_title)
        mitigated_visualizer.start_visualization(mitigated_title)
        time.sleep(1)  # Give windows time to initialize
    
    # Storage for results
    raw_results = []
    mitigated_results = []
    
    try:
        print(f"\nPerforming {num_tosses} quantum coin tosses with and without error mitigation...")
        print(f"Simulating {error_rate:.1%} error rate for hardware noise")
        
        for i in range(num_tosses):
            # 1. Create standard quantum circuit for ideal measurement
            qc = QuantumCircuit(1, 1)
            qc.h(0)  # Apply Hadamard gate
            qc.measure(0, 0)  # Measure
            
            # Run for ideal result
            job = backend.run(qc, shots=1)
            result = job.result()
            counts = result.get_counts()
            ideal_outcome = list(counts.keys())[0]
            ideal_bit = int(ideal_outcome)
            
            # 2. For raw result - add noise manually if hardware mode
            raw_bit = ideal_bit
            if use_hardware and np.random.random() < error_rate:
                # Manually flip the bit with probability error_rate
                raw_bit = 1 - raw_bit
            
            # 3. For mitigated result - use repeated measurements
            # Run 5 times and take majority vote
            if use_hardware:
                votes = []
                for _ in range(5):
                    # Get ideal outcome but manually add noise
                    vote = ideal_bit
                    if np.random.random() < error_rate:
                        vote = 1 - vote
                    votes.append(vote)
                
                # Take the majority vote
                mitigated_bit = 1 if votes.count(1) > votes.count(0) else 0
            else:
                # Without hardware noise, mitigated = ideal
                mitigated_bit = ideal_bit
            
            # Store results
            raw_results.append(raw_bit)
            if raw_visualizer:
                raw_visualizer.add_result(raw_bit)
                
            mitigated_results.append(mitigated_bit)
            if mitigated_visualizer:
                mitigated_visualizer.add_result(mitigated_bit)
            
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
        if raw_results and mitigated_results:
            analyze_results(raw_results, mitigated_results)
        
        # Save and close visualizations
        if visualize:
            if raw_visualizer:
                raw_visualizer.save_visualization("raw_quantum_toss.png")
            if mitigated_visualizer:
                mitigated_visualizer.save_visualization("mitigated_quantum_toss.png")
            
            print("Visualizations saved. Close the windows to continue...")

def analyze_results(raw_results, mitigated_results):
    """
    Analyze and compare raw vs mitigated results
    
    Args:
        raw_results: Results without error mitigation
        mitigated_results: Results with error mitigation
    """
    # Count outcomes
    raw_zeros = raw_results.count(0)
    raw_ones = raw_results.count(1)
    
    mitigated_zeros = mitigated_results.count(0)
    mitigated_ones = mitigated_results.count(1)
    
    total_raw = len(raw_results)
    total_mitigated = len(mitigated_results)
    
    # Calculate probabilities
    raw_prob_0 = raw_zeros / total_raw
    raw_prob_1 = raw_ones / total_raw
    
    mitigated_prob_0 = mitigated_zeros / total_mitigated
    mitigated_prob_1 = mitigated_ones / total_mitigated
    
    # Ideal probability for a fair coin is 0.5
    raw_bias = abs(raw_prob_0 - 0.5)
    mitigated_bias = abs(mitigated_prob_0 - 0.5)
    
    # Print analysis
    print("\n==== Result Analysis ====")
    print(f"Total samples: {total_raw}")
    print("\nRaw Results:")
    print(f"  Zeros: {raw_zeros} ({raw_prob_0:.4f})")
    print(f"  Ones: {raw_ones} ({raw_prob_1:.4f})")
    print(f"  Bias from ideal: {raw_bias:.4f}")
    
    print("\nMitigated Results:")
    print(f"  Zeros: {mitigated_zeros} ({mitigated_prob_0:.4f})")
    print(f"  Ones: {mitigated_ones} ({mitigated_prob_1:.4f})")
    print(f"  Bias from ideal: {mitigated_bias:.4f}")
    
    if raw_bias > 0:
        improvement = (raw_bias - mitigated_bias) / raw_bias * 100
        print(f"\nBias reduction: {improvement:.2f}%")
    
    # Calculate run statistics
    print("\n==== Run Statistics ====")
    
    # Calculate run lengths (sequences of the same outcome)
    raw_runs = calculate_runs(raw_results)
    mitigated_runs = calculate_runs(mitigated_results)
    
    print(f"Raw max run length: {max(raw_runs)}")
    print(f"Mitigated max run length: {max(mitigated_runs)}")

def calculate_runs(results):
    """Calculate run lengths in a sequence"""
    runs = []
    current_run = 1
    
    for i in range(1, len(results)):
        if results[i] == results[i-1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    
    # Add the last run
    runs.append(current_run)
    return runs

if __name__ == "__main__":
    # Add command line arguments
    parser = argparse.ArgumentParser(description='Error-Mitigated Quantum Coin Toss Simulator')
    parser.add_argument('--tosses', type=int, default=100, help='Number of coin tosses to perform')
    parser.add_argument('--hardware', action='store_true', help='Use hardware acceleration with noise')
    parser.add_argument('--error', type=float, default=0.05, help='Error rate (0.0-1.0) for hardware noise')
    parser.add_argument('--no-viz', action='store_true', help='Disable visualization')
    parser.add_argument('--delay', type=float, default=0.1, help='Delay between tosses (seconds)')
    
    args = parser.parse_args()
    
    # Run the experiment
    run_experiment(
        num_tosses=args.tosses,
        use_hardware=args.hardware,
        error_rate=args.error,
        visualize=not args.no_viz,
        delay=args.delay
    )