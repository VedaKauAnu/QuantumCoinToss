from qiskit import QuantumCircuit
from quantum_rings_provider import initialize_quantum_backend, create_rings_backend
import numpy as np
import matplotlib.pyplot as plt

def single_quantum_coin_toss(use_hardware=False):
    """
    Perform a single quantum coin toss
    
    Args:
        use_hardware: Whether to use hardware acceleration via Quantum Rings
        
    Returns:
        int: 0 or 1 representing the coin toss outcome
    """
    # Choose the backend
    if use_hardware:
        backend = initialize_quantum_backend()
    else:
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
    
    # Create a quantum circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)
    
    # Apply Hadamard gate to create superposition
    qc.h(0)
    
    # Measure the qubit
    qc.measure(0, 0)
    
    # Run the circuit on the simulator
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Get the outcome (should be either '0' or '1')
    outcome = list(counts.keys())[0]
    
    return int(outcome)

def batched_quantum_coin_toss(num_tosses=10, use_hardware=False):
    """
    Perform multiple quantum coin tosses efficiently
    
    Args:
        num_tosses: Number of coin tosses to perform
        use_hardware: Whether to use hardware acceleration
        
    Returns:
        list: List of 0s and 1s representing coin toss outcomes
    """
    # Choose the backend
    if use_hardware:
        backend = initialize_quantum_backend()
    else:
        from qiskit_aer import AerSimulator
        backend = AerSimulator()
    
    # Create a quantum circuit with 1 qubit and num_tosses classical bits
    qc = QuantumCircuit(1, num_tosses)
    
    # Perform the tosses
    for i in range(num_tosses):
        # Reset qubit to |0⟩ (except for first iteration where it's already |0⟩)
        if i > 0:
            qc.reset(0)
            
        # Apply Hadamard gate to create superposition
        qc.h(0)
        
        # Measure the qubit
        qc.measure(0, i)
    
    # Run the circuit
    job = backend.run(qc, shots=1)
    result = job.result()
    counts = result.get_counts()
    
    # Parse the bitstring (comes in reverse order in Qiskit)
    bit_string = list(counts.keys())[0]
    
    # Convert to list of integers (and reverse to get correct order)
    toss_results = [int(bit) for bit in reversed(bit_string)]
    
    return toss_results

def biased_quantum_coin(bias_angle, shots=1):
    """
    Create a biased quantum coin by applying Ry rotation
    
    Args:
        bias_angle: Angle in radians to control bias
                   0 = all 0s, π = all 1s, π/2 = fair coin
        shots: Number of coin tosses to perform
        
    Returns:
        dict: Count of outcomes
        float: Probability of 0
        float: Probability of 1
    """
    # Use standard simulator for this demonstration
    from qiskit_aer import AerSimulator
    backend = AerSimulator()
    
    # Create a quantum circuit
    qc = QuantumCircuit(1, 1)
    
    # Apply Ry rotation for bias
    # Ry(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
    qc.ry(bias_angle, 0)
    
    # Measure the qubit
    qc.measure(0, 0)
    
    # Run the circuit
    job = backend.run(qc, shots=shots)
    result = job.result()
    counts = result.get_counts()
    
    # Calculate probabilities
    prob_0 = counts.get('0', 0) / shots
    prob_1 = counts.get('1', 0) / shots
    
    return counts, prob_0, prob_1

def plot_bias_experiment():
    """
    Run experiments with different rotation angles and plot the results
    against theoretical predictions
    """
    angles = np.linspace(0, np.pi, 20)
    prob_ones = []
    
    for angle in angles:
        _, _, p1 = biased_quantum_coin(angle, shots=100)
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

if __name__ == "__main__":
    # Test single coin toss
    print("\n=== Single Quantum Coin Toss ===")
    result = single_quantum_coin_toss()
    print(f"Result: {result} ({'Heads' if result == 0 else 'Tails'})")
    
    # Test batched coin tosses
    print("\n=== Batched Quantum Coin Tosses (10) ===")
    results = batched_quantum_coin_toss(10)
    heads = results.count(0)
    tails = results.count(1)
    print(f"Results: {results}")
    print(f"Heads: {heads}, Tails: {tails}")
    
    # Try with Quantum Rings hardware
    try:
        print("\n=== Quantum Rings Hardware Coin Toss ===")
        hardware_result = single_quantum_coin_toss(use_hardware=True)
        print(f"Hardware result: {hardware_result} ({'Heads' if hardware_result == 0 else 'Tails'})")
    except Exception as e:
        print(f"Hardware simulation error: {e}")
    
    # Test biased coin
    print("\n=== Biased Quantum Coin ===")
    for angle in [0, np.pi/4, np.pi/2, 3*np.pi/4, np.pi]:
        counts, p0, p1 = biased_quantum_coin(angle, shots=100)
        print(f"Angle: {angle:.2f} radians")
        print(f"Counts: {counts}")
        print(f"Probability of 0: {p0:.4f}, Probability of 1: {p1:.4f}")
        print("-" * 30)
    
    # Run the visualization experiment
    print("\n=== Running Bias Visualization Experiment ===")
    plot_bias_experiment()