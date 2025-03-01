# Quantum Coin Toss Simulator

A Python implementation of a quantum randomness generator using quantum superposition principles, built with Qiskit.

## Project Overview

This project demonstrates how quantum computing principles can be applied to generate true randomness. Unlike classical random number generators that rely on deterministic algorithms, quantum randomness leverages the inherent unpredictability of quantum measurement to produce provably random outcomes.

Key features:
- Basic quantum coin toss implementation using Hadamard gates
- Biased quantum coin implementation using Ry rotation gates
- Advanced quantum randomness with simulated qutrit (3-level) systems
- Error mitigation techniques to improve randomness quality
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
pip install qiskit qiskit-aer matplotlib numpy pandas seaborn
```

## Usage

    ## Quick Start

        1. **Setup environment:**
        ```bash
        python -m venv .venv
        source .venv/bin/activate
        ```

        2. **Install dependencies:**
        ```bash
        pip install qiskit qiskit-aer matplotlib numpy pandas seaborn
        ```

        3. **Run basic coin toss:**
        ```bash
        python quantum_rings_toss.py --tosses 50 --no-viz
        ```

        ## Core Components

        - **quantum_rings_toss.py**: Basic quantum coin toss using Hadamard gates
        - **error_mitigated_coin.py**: Implementation with error mitigation techniques
        - **advanced_qutrit_generator.py**: Three-level quantum system simulation
        - **quantum_visualizer.py**: Real-time visualization engine (note: visualization may have issues on macOS)

        ## Command Options

        Each component accepts these command-line arguments:

        **Basic Coin Toss:**
        ```bash
        python quantum_rings_toss.py [--tosses N] [--hardware] [--no-viz] [--delay X]
        ```

        **Error Mitigation:**
        ```bash
        python error_mitigated_coin.py [--tosses N] [--hardware] [--error X] [--no-viz] [--delay X]
        ```

        **Qutrit Generator:**
        ```bash
        python advanced_qutrit_generator.py [--samples N] [--hardware] [--no-viz] [--delay X]
        ```

        Where:
        - `--tosses`/`--samples`: Number of measurements (default: 100)
        - `--hardware`: Use simulated hardware mode
        - `--error`: Set error rate for mitigation (default: 0.05)
        - `--no-viz`: Run without visualization 
        - `--delay`: Set time between measurements (default: 0.1s)

        ## Troubleshooting

        - **Visualization errors on macOS**: Use `--no-viz` flag to run without visualization
        - **Missing modules**: Ensure all dependencies are installed
        - **Import errors**: Check file names match the imports

        ## Examples

        Generate statistics for 100 coin tosses:
        ```bash
        python quantum_rings_toss.py --tosses 100 --no-viz
        ```

        Compare error mitigation with 10% error rate:
        ```bash
        python error_mitigated_coin.py --tosses 50 --hardware --error 0.1 --no-viz
        ```

        Generate qutrit random values:
        ```bash
        python advanced_qutrit_generator.py --samples 50 --no-viz
        ```

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

### Run the Coin Toss Demo with Real-time Visualization

```bash
python quantum_rings_toss_with_viz.py --tosses 200 --delay 0.05
```

This provides a real-time visualization of:
1. The distribution of coin toss outcomes
2. The running probability over time
3. The most recent 50 measurements
4. Run length analysis (sequences of consecutive identical outcomes)

Command line options:
- `--tosses N`: Number of coin tosses to perform (default: 100)
- `--hardware`: Use simulated hardware acceleration
- `--no-viz`: Disable visualization (for faster processing)
- `--delay X`: Set delay between tosses in seconds (default: 0.1)

### Advanced Features

#### Error Mitigation with Dual Visualization

```bash
python error_mitigated_coin_with_viz.py --tosses 200 --hardware --error 0.1
```

This demonstrates how error mitigation techniques improve quantum randomness quality with real-time visualization:
1. Shows two side-by-side visualizations (raw and error-mitigated)
2. Introduces configurable error rates to simulate real quantum hardware noise
3. Applies error mitigation techniques (repetition and majority voting)
4. Displays comprehensive statistics comparing both approaches

Command line options:
- `--tosses N`: Number of coin tosses to perform (default: 100)
- `--hardware`: Enable hardware simulation with noise
- `--error X`: Set the error rate between 0.0-1.0 (default: 0.05)
- `--no-viz`: Disable visualization
- `--delay X`: Set delay between tosses in seconds (default: 0.1)

#### Qutrit Random Number Generation with Visualization

```bash
python advanced_qutrit_generator_with_viz.py --samples 150
```

This implements a 3-level quantum system (qutrit) with real-time visualization:
1. Uses 2 qubits to simulate a 3-level system
2. Generates values in the set {0, 1, 2} with equal probability
3. Provides a specialized qutrit visualization interface
4. Shows the convergence to theoretical distribution (1/3 for each outcome)

Command line options:
- `--samples N`: Number of qutrit values to generate (default: 100)
- `--hardware`: Use simulated hardware acceleration
- `--no-viz`: Disable visualization
- `--delay X`: Set delay between measurements in seconds (default: 0.1)

## Implementation Details

The project contains the following main components:

1. **Core Components:**
   - `quantum_rings_provider.py` - Simulates a quantum hardware provider interface
   - `quantum_rings_toss.py` - Basic quantum coin toss implementation
   - `error_mitigated_coin.py` - Error mitigation techniques for improved quality
   - `advanced_qutrit_generator.py` - Higher-dimensional quantum random number generation

2. **Visualization Components:**
   - `quantum_visualizer.py` - Real-time data visualization engine for quantum experiments
   - `quantum_rings_toss_with_viz.py` - Coin toss implementation with visualization
   - `error_mitigated_coin_with_viz.py` - Error mitigation with dual visualizations
   - `advanced_qutrit_generator_with_viz.py` - Qutrit visualization with specialized interface

These components work together to demonstrate the advantages of quantum-based randomness over classical approaches, with both numerical analysis and visual representations of the quantum behaviors.

## Mathematical Verification

The code verifies the quantum measurement postulate by demonstrating that:
- For a fair coin (Hadamard gate): P(0) = P(1) = 0.5
- For a biased coin (Ry gate): P(1) = sin²(θ/2)
- For a qutrit system: P(0) = P(1) = P(2) = 1/3

The visualizations prove these relationships by plotting experimental results against the theoretical curves.

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