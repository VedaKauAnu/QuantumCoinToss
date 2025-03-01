"""
Advanced Quantum Coin Toss Experiments
--------------------------------------
This script demonstrates more sophisticated quantum coin toss applications
including multi-qubit implementations, entanglement-based protocols,
and practical applications like quantum random number generators.
"""

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Import additional visualization tools
from qiskit.visualization import plot_histogram, plot_bloch_multivector

# Set plot style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = [10, 6]

def fair_quantum_coin(shots=1):
    """
    Basic quantum coin toss using the Hadamard gate
    """
    qc = QuantumCircuit(1, 1)
    qc.h(0)  # Apply Hadamard gate to create superposition
    qc.measure(0, 0)
    
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    
    return counts

def biased_quantum_coin(bias_angle, shots=1000):
    """
    Biased quantum coin using the Ry rotation gate
    bias_angle: angle in radians controlling the bias
    """
    qc = QuantumCircuit(1, 1)
    qc.ry(bias_angle, 0)  # Apply Ry rotation for bias
    qc.measure(0, 0)
    
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    
    # Calculate probabilities
    prob_0 = counts.get('0', 0) / shots
    prob_1 = counts.get('1', 0) / shots
    
    return counts, prob_0, prob_1

def entanglement_based_coin_toss(shots=1000):
    """
    Two-party quantum coin toss using entanglement
    This ensures fairness between two parties
    """
    # Create circuit with 2 qubits and 2 classical bits
    qc = QuantumCircuit(2, 2)
    
    # Prepare Bell state (entangled qubits)
    qc.h(0)  # Put first qubit in superposition
    qc.cx(0, 1)  # CNOT to entangle qubits
    
    # Measure both qubits
    qc.measure([0, 1], [0, 1])
    
    # Run the simulation
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    
    return counts

def quantum_rng(num_bits=8, shots=1):
    """
    Quantum Random Number Generator
    Generates random numbers using quantum measurements
    
    num_bits: number of bits in the random number
    shots: number of random numbers to generate
    """
    # Create circuit with num_bits qubits and classical bits
    qc = QuantumCircuit(num_bits, num_bits)
    
    # Put all qubits in superposition
    for i in range(num_bits):
        qc.h(i)
    
    # Measure all qubits
    qc.measure(range(num_bits), range(num_bits))
    
    # Run the simulation
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    
    # Convert binary strings to integers
    random_numbers = []
    for bitstring in counts:
        random_numbers.extend([int(bitstring, 2)] * counts[bitstring])
    
    return random_numbers

def visualize_bloch_sphere(angles):
    """
    Visualizes quantum states on the Bloch sphere
    for different rotation angles
    """
    bloch_vectors = []
    
    for angle in angles:
        # Create state vector
        qc = QuantumCircuit(1)
        qc.ry(angle, 0)
        
        # Get statevector simulator
        simulator = AerSimulator(method='statevector')
        qc_transpiled = transpile(qc, simulator)
        
        # Execute and get statevector
        job = simulator.run(qc_transpiled)
        result = job.result()
        statevector = result.get_statevector()
        
        # Store the statevector
        bloch_vectors.append((angle, statevector))
    
    return bloch_vectors

def security_analysis(num_trials=1000, sequence_length=10):
    """
    Tests the unpredictability of the quantum coin toss
    by analyzing sequences of tosses
    """
    # Generate many quantum coin tosses
    all_tosses = []
    for _ in range(num_trials):
        result = fair_quantum_coin(shots=sequence_length)
        # Extract individual tosses from the results
        if '0' in result:
            zeros = ['0'] * result.get('0', 0)
            all_tosses.extend(zeros)
        if '1' in result:
            ones = ['1'] * result.get('1', 0)
            all_tosses.extend(ones)
    
    # Convert to numpy array for analysis
    toss_array = np.array(all_tosses, dtype=int)
    
    # Analyze sequence properties
    sequence_counts = {}
    for i in range(len(toss_array) - 1):
        pattern = ''.join(map(str, toss_array[i:i+2]))
        if pattern in sequence_counts:
            sequence_counts[pattern] += 1
        else:
            sequence_counts[pattern] = 1
    
    # Calculate autocorrelation
    autocorr = np.correlate(toss_array, toss_array, mode='full')
    
    return sequence_counts, autocorr

def multi_party_coin_toss(num_parties=3, shots=1000):
    """
    Implements a multi-party quantum coin toss protocol
    where all parties must agree on the outcome.
    
    Uses GHZ state: (|000...0⟩ + |111...1⟩)/√2
    """
    # Create circuit with qubits for each party
    qc = QuantumCircuit(num_parties, num_parties)
    
    # Create GHZ state
    qc.h(0)  # Put first qubit in superposition
    for i in range(1, num_parties):
        qc.cx(0, i)  # CNOT to entangle all qubits
    
    # Measure all qubits
    qc.measure(range(num_parties), range(num_parties))
    
    # Run the simulation
    simulator = AerSimulator()
    result = simulator.run(qc, shots=shots).result()
    counts = result.get_counts()
    
    return counts

if __name__ == "__main__":
    print("\n=== ADVANCED QUANTUM COIN EXPERIMENTS ===\n")
    
    # 1. Fair coin toss example
    print("1. Running 1000 fair quantum coin tosses...")
    fair_results = fair_quantum_coin(shots=1000)
    print(f"Results: {fair_results}")
    
    # 2. Biased coin example with visualization
    print("\n2. Testing biased quantum coins with different angles...")
    angles = np.linspace(0, np.pi, 7)
    bias_results = []
    
    for angle in angles:
        _, p0, p1 = biased_quantum_coin(angle, shots=1000)
        bias_results.append((angle, p0, p1))
        print(f"Angle: {angle:.2f}, P(0): {p0:.4f}, P(1): {p1:.4f}")
    
    # 3. Entanglement-based fair coin toss
    print("\n3. Running entanglement-based fair coin toss...")
    entangled_results = entanglement_based_coin_toss(shots=1000)
    print(f"Entangled results: {entangled_results}")
    
    # 4. Quantum random number generator
    print("\n4. Generating 10 random 8-bit numbers...")
    random_numbers = quantum_rng(num_bits=8, shots=10)
    print(f"Random numbers: {random_numbers}")
    
    # 5. Security analysis of quantum coin tosses
    print("\n5. Analyzing security properties of quantum coin tosses...")
    sequence_counts, autocorr = security_analysis(num_trials=100, sequence_length=20)
    print(f"Sequence pattern counts: {sequence_counts}")
    
    # 6. Multi-party coin toss
    print("\n6. Running 3-party quantum coin toss protocol...")
    multi_party_results = multi_party_coin_toss(num_parties=3, shots=1000)
    print(f"Multi-party toss results: {multi_party_results}")
    
    # Create visualizations
    print("\n7. Creating visualizations (saving to files)...")
    
    # Plot bias results
    angles_plot = [r[0] for r in bias_results]
    p1_plot = [r[2] for r in bias_results]
    
    plt.figure(figsize=(10, 6))
    plt.plot(angles_plot, p1_plot, 'bo-', label='Experimental')
    x_range = np.linspace(0, np.pi, 100)
    plt.plot(x_range, np.sin(x_range/2)**2, 'r-', label='Theoretical: sin²(θ/2)')
    plt.xlabel('Rotation Angle (radians)')
    plt.ylabel('Probability of Measuring |1⟩')
    plt.title('Quantum Coin Bias vs. Rotation Angle')
    plt.grid(True)
    plt.legend()
    plt.savefig('quantum_bias_curve.png')
    
    # Plot multi-party results
    plt.figure(figsize=(10, 6))
    outcomes = list(multi_party_results.keys())
    counts = list(multi_party_results.values())
    plt.bar(outcomes, counts)
    plt.xlabel('Measurement Outcomes')
    plt.ylabel('Counts')
    plt.title('Multi-Party Quantum Coin Toss Results')
    plt.savefig('multi_party_results.png')
    
    # Plot autocorrelation
    plt.figure(figsize=(10, 6))
    plt.plot(autocorr[len(autocorr)//2:len(autocorr)//2+20])
    plt.xlabel('Lag')
    plt.ylabel('Autocorrelation')
    plt.title('Autocorrelation of Quantum Coin Toss Sequence')
    plt.grid(True)
    plt.savefig('quantum_autocorrelation.png')
    
    print("\nExperiments complete! Visualizations saved to files.")