# Quantum Coin Toss Simulator

A Python implementation of a quantum randomness generator using quantum superposition principles, built with Qiskit.

## Project Overview

This project demonstrates how quantum computing principles can be applied to generate true randomness. Unlike classical random number generators that rely on deterministic algorithms, quantum randomness leverages the inherent unpredictability of quantum measurement to produce provably random outcomes.

Key features:
- Basic quantum coin toss implementation using Hadamard gates
- Biased quantum coin implementation using Ry rotation gates
- Visualization of quantum probability distributions
- Mathematical verification of statistical properties

## Theoretical Background

A quantum coin toss works by:
1. Initializing a qubit in the |0⟩ state
2. Applying a Hadamard transformation to create an equal superposition: 
   H|0⟩ = (|0⟩ + |1⟩)/√2
3. Measuring the qubit, which collapses the superposition with a 50% chance of each outcome

For biased coins, we use the Ry rotation gate:
- Ry(θ)|0⟩ = cos(θ/2)|0⟩ + sin(θ/2)|1⟩
- This gives probability of measuring |1⟩ as sin²(θ/2)

## Installation

### Prerequisites
- Python 3.13 or later
- Virtual environment (recommended)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/quantum-coin-toss.git
cd quantum-coin-toss
```

2. Create and activate a virtual environment:
```bash
python3.13 -m venv .venv
source .venv/bin/activate
```

3. Install required packages:
```bash
pip install qiskit qiskit-aer matplotlib numpy
```

## Usage

### Basic Quantum Coin Toss

```python
from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator

# Create a quantum circuit
qc = QuantumCircuit(1, 1)
qc.h(0)  # Apply Hadamard gate
qc.measure(0, 0)  # Measure

# Run simulation
simulator = AerSimulator()
job = simulator.run(qc, shots=1000)
result = job.result()
counts = result.get_counts()

print(f"Results: {counts}")
```

### Run the Full Demo

```bash
python quantum_coin.py
```

This will:
1. Perform single and multiple fair coin tosses
2. Demonstrate biased quantum coins with various angles
3. Generate a visualization comparing experimental and theoretical results

## Code Structure

- `quantum_coin.py` - Main implementation file containing:
  - `quantum_coin_toss()` - Fair coin toss using Hadamard gate
  - `biased_quantum_coin()` - Parameterized coin toss with Ry rotation
  - `plot_bias_experiment()` - Visualization function comparing experimental and theoretical results

## Mathematical Verification

The code verifies the quantum measurement postulate by demonstrating that:
- For a fair coin (Hadamard gate): P(0) = P(1) = 0.5
- For a biased coin (Ry gate): P(1) = sin²(θ/2)

The visualization proves this relationship by plotting experimental results against the theoretical curve.

## Applications

- Cryptographic key generation
- Monte Carlo simulations
- Fair online gambling
- Quantum-secure random number generation
- Scientific simulations requiring unbiased random numbers

## License

MIT License - See LICENSE file for details.

## References

1. Nielsen, M. A., & Chuang, I. L. (2010). Quantum Computation and Quantum Information.
2. Qiskit Documentation: https://qiskit.org/documentation/
3. "Quantum Random Number Generators" - Ma et al. (2016)
