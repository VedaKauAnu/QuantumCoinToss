import os
import sys
import subprocess
import argparse

def check_python_version():
    """Check if the Python version is compatible"""
    required_version = (3, 7)
    current_version = sys.version_info
    
    if current_version < required_version:
        print(f"❌ Python {required_version[0]}.{required_version[1]} or higher is required")
        print(f"   Current version: {current_version[0]}.{current_version[1]}")
        return False
    
    print(f"✅ Python version {current_version[0]}.{current_version[1]} is compatible")
    return True

def install_requirements():
    """Install required packages"""
    requirements = [
        "qiskit>=1.0.0",
        "qiskit-aer>=0.12.0",
        "matplotlib>=3.7.0",
        "numpy>=1.24.0",
        "scipy>=1.10.0"
    ]
    
    print("Installing base requirements...")
    for req in requirements:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", req])
            print(f"✅ Installed {req}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to install {req}")
            return False
    
    return True

def install_quantum_rings():
    """Install Quantum Rings SDK"""
    print("\nInstalling Quantum Rings SDK...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "quantumrings>=1.0.0"])
        print("✅ Quantum Rings SDK installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install Quantum Rings SDK")
        return False

def configure_environment(token=None):
    """Configure environment variables for Quantum Rings"""
    if token:
        # Set the token for the current session
        os.environ['QUANTUM_RINGS_TOKEN'] = token
        print(f"✅ Set QUANTUM_RINGS_TOKEN for current session")
        
        # Write instructions for permanent setup
        print("\nTo permanently set the token, add the following to your shell profile:")
        print(f"export QUANTUM_RINGS_TOKEN='{token}'")
        
        # Detect shell type and suggest the right file
        shell = os.environ.get('SHELL', '')
        if 'bash' in shell:
            print("\nFor bash, add to ~/.bashrc or ~/.bash_profile:")
            print(f"echo 'export QUANTUM_RINGS_TOKEN=\"{token}\"' >> ~/.bashrc")
        elif 'zsh' in shell:
            print("\nFor zsh, add to ~/.zshrc:")
            print(f"echo 'export QUANTUM_RINGS_TOKEN=\"{token}\"' >> ~/.zshrc")
        elif 'fish' in shell:
            print("\nFor fish, use:")
            print(f"set -Ux QUANTUM_RINGS_TOKEN \"{token}\"")
    else:
        print("⚠️ No token provided, skipping environment configuration")
        print("You can set the token later with:")
        print("export QUANTUM_RINGS_TOKEN='your_token_here'")

def test_setup():
    """Test if the setup was successful"""
    print("\nTesting setup...")
    
    try:
        # Try to import the necessary modules
        import qiskit
        import qiskit_aer
        import quantumrings
        
        print("✅ All required modules imported successfully")
        
        # Check if the token is set
        token = os.environ.get('QUANTUM_RINGS_TOKEN')
        if token:
            masked_token = token[:4] + "..." + token[-4:] if len(token) > 8 else "..."
            print(f"✅ QUANTUM_RINGS_TOKEN is set: {masked_token}")
        else:
            print("⚠️ QUANTUM_RINGS_TOKEN is not set")
        
        return True
    
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def main():
    """Main function to run the setup process"""
    parser = argparse.ArgumentParser(description='Setup environment for Quantum Rings SDK')
    parser.add_argument('--token', type=str, help='Your Quantum Rings API token')
    parser.add_argument('--install', action='store_true', help='Install required packages')
    parser.add_argument('--test', action='store_true', help='Test the setup')
    
    args = parser.parse_args()
    
    print("=== Quantum Rings SDK Setup ===\n")
    
    if not check_python_version():
        sys.exit(1)
    
    if args.install:
        if not install_requirements():
            print("⚠️ Some requirements could not be installed")
        
        if not install_quantum_rings():
            print("⚠️ Quantum Rings SDK could not be installed")
    
    if args.token:
        configure_environment(args.token)
    
    if args.test or not (args.install or args.token):
        test_setup()
    
    print("\nSetup completed!")

if __name__ == "__main__":
    main()