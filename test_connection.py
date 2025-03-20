import os
import sys
from qiskit import QuantumCircuit
from quantum_rings_provider import create_rings_backend, initialize_quantum_backend

def check_requirements():
    """Check if all required packages are installed"""
    try:
        import qiskit
        import qiskit_aer
        import matplotlib
        import numpy
        import scipy
        print("✅ Base dependencies are installed")
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install base dependencies: pip install qiskit qiskit-aer matplotlib numpy scipy")
        return False
    
    # Check for Quantum Rings SDK
    try:
        import quantumrings
        print("✅ Quantum Rings SDK is installed")
    except ImportError:
        print("❌ Quantum Rings SDK is not installed")
        print("Please install it: pip install quantumrings")
        return False
    
    return True

def check_authentication():
    """Check if Quantum Rings authentication token is available"""
    token = os.environ.get('QUANTUM_RINGS_TOKEN')
    if token:
        print("✅ Quantum Rings token found in environment variables")
        # Show a masked version of the token for verification
        print(f"   Token: {token[:4]}...{token[-4:] if len(token) > 8 else ''}")
        return True
    else:
        print("❓ Quantum Rings token not found in environment variables")
        print("   You can set it with: export QUANTUM_RINGS_TOKEN='your_token_here'")
        print("   Or provide it directly when creating the backend")
        return False

def test_connection():
    """Test connection to Quantum Rings backend"""
    print("\nTesting connection to Quantum Rings backend...")
    try:
        # Try to initialize the backend
        backend = initialize_quantum_backend()
        
        if backend is None:
            print("❌ Failed to initialize backend")
            return False
        
        # Create a simple circuit
        qc = QuantumCircuit(1, 1)
        qc.h(0)  # Apply Hadamard gate
        qc.measure(0, 0)
        
        # Run the circuit
        print("Running a simple quantum circuit...")
        job = backend.run(qc, shots=10)
        result = job.result()
        counts = result.get_counts()
        
        print(f"✅ Circuit executed successfully!")
        print(f"Results: {counts}")
        
        return True
    
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

if __name__ == "__main__":
    print("=== Quantum Rings SDK Test ===\n")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    print("\n--- Authentication Check ---")
    check_authentication()
    
    print("\n--- Connection Test ---")
    test_connection()
    
    print("\nTest completed. If any issues were encountered, please check the documentation.")