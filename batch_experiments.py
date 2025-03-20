import sys
import time
import os
import numpy as np
from quantum_coin_experiment import run_experiment
from quantum_rings_provider import initialize_quantum_backend

# Check for Quantum Rings token
has_qr_token = os.environ.get('QUANTUM_RINGS_TOKEN') is not None

def main():
    print("===== QUANTUM COIN TOSS EXPERIMENTS =====")
    print("This script will run a series of quantum coin experiments")
    print("Press Ctrl+C at any time to skip to the next experiment")
    
    # Check if we can connect to Quantum Rings
    print("Testing Quantum Rings connection...")
    try:
        backend = initialize_quantum_backend()
        has_qr_backend = not isinstance(backend, __import__('qiskit_aer').AerSimulator)
        if has_qr_backend:
            print("✅ Connected to Quantum Rings backend")
        else:
            print("⚠️ Using Aer simulator as fallback (Quantum Rings not available)")
    except Exception as e:
        print(f"⚠️ Error testing Quantum Rings connection: {e}")
        has_qr_backend = False
    
    # List of experiments to run
    experiments = [
        {
            "name": "Basic Fair Quantum Coin",
            "params": {
                "num_tosses": 50,
                "use_hardware": False,
                "batch_size": 5,
                "bias_angle": None
            }
        },
        {
            "name": "Hardware-Accelerated Fair Quantum Coin",
            "params": {
                "num_tosses": 50,
                "use_hardware": has_qr_backend,  # Only use if available
                "batch_size": 5,
                "bias_angle": None
            }
        },
        {
            "name": "Slightly Biased Quantum Coin (60/40)",
            "params": {
                "num_tosses": 50,
                "use_hardware": False,
                "batch_size": 5,
                "bias_angle": np.arcsin(np.sqrt(0.4)) * 2  # P(1) = sin²(θ/2) = 0.4
            }
        },
        {
            "name": "Heavily Biased Quantum Coin (90/10)",
            "params": {
                "num_tosses": 50,
                "use_hardware": False,
                "batch_size": 5,
                "bias_angle": np.arcsin(np.sqrt(0.1)) * 2  # P(1) = sin²(θ/2) = 0.1
            }
        }
    ]
    
    # Run each experiment
    for i, experiment in enumerate(experiments, 1):
        print("\n" + "=" * 50)
        print(f"Experiment {i}/{len(experiments)}: {experiment['name']}")
        print("=" * 50 + "\n")
        
        try:
            # Run the experiment with specified parameters
            run_experiment(**experiment["params"])
            
            # Pause between experiments to let user see results
            if i < len(experiments):
                for countdown in range(5, 0, -1):
                    sys.stdout.write(f"\rStarting next experiment in {countdown} seconds... ")
                    sys.stdout.flush()
                    time.sleep(1)
                print("\n")
                
        except KeyboardInterrupt:
            print("\nExperiment skipped by user")
            continue
    
    print("\n===== ALL EXPERIMENTS COMPLETED =====")
    print("Results and visualizations have been saved")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExperiment suite interrupted by user")
        sys.exit(0)