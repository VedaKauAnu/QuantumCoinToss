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
    
    Args:
        error_rate: Probability of bit-flip errors
        
    Returns:
        NoiseModel: A Qiskit noise model
    """
    # Create an empty noise model
    noise_model = NoiseModel()
    
    # Add bit-flip error to the noise model
    # This simulates errors that would occur on real quantum hardware
    noise_model.add_all_qubit_quantum_error(
        error_rate, "measure"
    )
    
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
    Run a complete experiment with two visualizers for comparison
    
    Args:
        num_tosses: Number of coin tosses to perform
        use_hardware: Whether to use hardware acceleration
        error_rate: Error rate for the noise model
        visualize: Whether to show real-time visualization
        delay: Delay between tosses (seconds)
    """
    # Initialize backend
    if use_hardware:
        backend = initialize_quantum_backend()
        # Add noise to simulate real quantum hardware
        noise_model = create_noise_model(error_rate)
        backend.set_options(noise_model=noise_model)
        print(f"Using hardware acceleration (simulated with {error_rate:.1%} error rate)")
    else:
        backend = AerSimulator()
        print("Using software simulation")
    
    # Initialize visualizers if requested
    raw_visualizer = None
    mitigated_visualizer = None
    
    if visualize:
        raw_visualizer = QuantumVisualizer()
        raw_title = "Raw Quantum Coin Tosses" + (" (with noise)" if use_hardware else "")
        
        mitigated_visualizer = QuantumVisualizer()
        mitigated_title = "Error-Mitigated Quantum Coin Tosses"
        
        # Start visualizers in separate threads to allow them to run concurrently
        threading.Thread(target=raw_visualizer.start_visualization, 
                         args=(raw_title,)).start()
        time.sleep(1)  # Small delay to space out the windows
        threading.Thread(target=mitigated_visualizer.start_visualization, 
                         args=(mitigated_title,)).start()
        time.sleep(1)  # Give windows time to initialize
    
    # Storage for results
    raw_results = []
    mitigated_results = []
    
    try:
        print(f"\nPerforming {num_tosses} quantum coin tosses with and without error mitigation...")
        
        for i in range(num_tosses):
            # Perform raw toss
            raw_outcome = single_coin_toss(backend, with_mitigation=False)
            raw_results.append(raw_outcome)
            if raw_visualizer:
                raw_visualizer.add_result(raw_outcome)
            
            # Perform mitigated toss
            mitigated_outcome = single_coin_toss(backend, with_mitigation=True)
            mitigated_results.append(mitigated_outcome)
            if mitigated_visualizer:
                mitigated_visualizer.add_result(mitigated_outcome)
            
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
            time.sleep(1)  # Give time for saves to complete
            
            # We don't explicitly stop visualizers to allow user to continue viewing
            # They will close when the user closes the windows

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