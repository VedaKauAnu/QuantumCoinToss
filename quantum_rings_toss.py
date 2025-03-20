import argparse
import time
import numpy as np
import matplotlib.pyplot as plt

# Import our modules
from quantum_rings_coin import single_quantum_coin_toss, batched_quantum_coin_toss, biased_quantum_coin
from quantum_rings_provider import create_rings_backend
from quantum_stats import analyze_coin_tosses, print_analysis, plot_results
from quantum_visualizer import QuantumVisualizer

def run_experiment(num_tosses=100, use_hardware=False, batch_size=50, 
                  visualize=True, delay=0.05, bias_angle=None):
    """
    Run a complete quantum coin toss experiment with visualization and analysis
    
    Args:
        num_tosses: Total number of coin tosses to perform
        use_hardware: Whether to use hardware acceleration
        batch_size: Number of tosses per batch for efficiency
        visualize: Whether to show real-time visualization
        delay: Delay between visualization updates (seconds)
        bias_angle: If set, creates a biased coin with the given angle (radians)
    """
    # Setup experiment description
    experiment_type = "Biased" if bias_angle is not None else "Fair"
    hardware_type = "Hardware-Accelerated" if use_hardware else "Simulated"
    experiment_name = f"{experiment_type} {hardware_type} Quantum Coin Toss"
    
    print(f"\n=== Starting {experiment_name} Experiment ===")
    print(f"Number of tosses: {num_tosses}")
    if bias_angle is not None:
        print(f"Bias angle: {bias_angle:.4f} radians")
        p0_theory = np.cos(bias_angle/2)**2
        p1_theory = np.sin(bias_angle/2)**2
        print(f"Theoretical probabilities: P(0)={p0_theory:.4f}, P(1)={p1_theory:.4f}")
    
    # Initialize visualizer if requested with optimized settings
    visualizer = None
    if visualize:
        visualizer = QuantumVisualizer(update_interval=500)  # Less frequent updates
        visualizer.start_visualization(title=experiment_name)
    
    # Storage for results
    results = []
    
    try:
        # Process in batches for efficiency
        tosses_completed = 0
        start_time = time.time()
        
        # Calculate optimal batch sizes
        remaining_tosses = num_tosses
        
        while tosses_completed < num_tosses:
            current_batch_size = min(batch_size, num_tosses - tosses_completed)
            
            if bias_angle is not None:
                # Generate biased coin tosses
                _, _, _ = biased_quantum_coin(bias_angle, shots=current_batch_size)
                
                # Generate individual tosses for visualization
                batch_results = []
                for _ in range(current_batch_size):
                    r = np.random.random()
                    if r < np.cos(bias_angle/2)**2:
                        batch_results.append(0)
                    else:
                        batch_results.append(1)
            else:
                # Generate fair quantum coin tosses with optimized batching
                batch_results = batched_quantum_coin_toss(current_batch_size, use_hardware)
            
            # Add all results at once
            results.extend(batch_results)
            
            # Update visualization (only once per batch)
            if visualizer:
                visualizer.add_result(batch_results)
                
                # Only pause once per batch
                if delay > 0:
                    plt.pause(delay)
            
            # Update progress
            tosses_completed += len(batch_results)
            elapsed = time.time() - start_time
            rate = tosses_completed / elapsed if elapsed > 0 else 0
            
            if tosses_completed % batch_size == 0 or tosses_completed == num_tosses:
                print(f"Progress: {tosses_completed}/{num_tosses} tosses completed ({rate:.1f} tosses/sec)")
                
    except KeyboardInterrupt:
        print("\nExperiment interrupted by user")
    
    finally:
        # Display total time
        total_time = time.time() - start_time
        toss_rate = num_tosses / total_time if total_time > 0 else 0
        print(f"\nExperiment completed in {total_time:.2f} seconds")
        print(f"Average rate: {toss_rate:.1f} tosses per second")
        
        # Run statistical analysis if we have results
        if results:
            analysis = analyze_coin_tosses(results)
            print_analysis(analysis)
            
            # Compare to theoretical if biased
            if bias_angle is not None:
                print("\nComparison to Theoretical Expectation:")
                p0_observed = analysis['p0']
                p1_observed = analysis['p1']
                p0_error = abs(p0_observed - p0_theory)
                p1_error = abs(p1_observed - p1_theory)
                print(f"P(0) - Theory: {p0_theory:.4f}, Observed: {p0_observed:.4f}, Error: {p0_error:.4f}")
                print(f"P(1) - Theory: {p1_theory:.4f}, Observed: {p1_observed:.4f}, Error: {p1_error:.4f}")
        
        # Save visualization if active
        if visualize and visualizer:
            filename = f"quantum_coin_{experiment_type.lower()}_{hardware_type.lower()}.png"
            visualizer.save_visualization(filename)
            print(f"Visualization saved as {filename}")
            
            # Create additional analysis plot
            plot_results(results, title=f"{experiment_name} Analysis (n={len(results)})")
            
            # Close visualization
            time.sleep(1)  # Give time for save to complete
            visualizer.stop_visualization()

def main():
    """Parse command line arguments and run experiment"""
    parser = argparse.ArgumentParser(description='Quantum Coin Toss Experiment')
    
    parser.add_argument('--tosses', type=int, default=100,
                        help='Number of coin tosses to perform')
    parser.add_argument('--hardware', action='store_true',
                        help='Use hardware acceleration')
    parser.add_argument('--batch-size', type=int, default=50,  # Increased from 10
                        help='Number of tosses per batch for efficiency')
    parser.add_argument('--no-viz', action='store_true',
                        help='Disable visualization')
    parser.add_argument('--delay', type=float, default=0.05,  # Reduced from 0.1
                        help='Delay between visualization updates (seconds)')
    parser.add_argument('--bias', type=float, default=None,
                        help='Set bias angle in radians (0 to π)')
    
    args = parser.parse_args()
    
    # Run the experiment
    run_experiment(
        num_tosses=args.tosses,
        use_hardware=args.hardware,
        batch_size=args.batch_size,
        visualize=not args.no_viz,
        delay=args.delay,
        bias_angle=args.bias
    )

if __name__ == "__main__":
    main()