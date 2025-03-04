"""
Real-time Quantum Randomness Visualizer
This module provides visualization tools for quantum randomness experiments
"""
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import threading
import time
import collections

class QuantumVisualizer:
    """Class to visualize quantum randomness in real-time"""
    
    def __init__(self, max_samples=100, update_interval=200):
        """
        Initialize the visualizer
        
        Args:
            max_samples: Maximum number of samples to display in history
            update_interval: Milliseconds between animation updates
        """
        self.results = []
        self.running = False
        self.fig = None
        self.animation = None
        self.lock = threading.Lock()
        self.max_samples = max_samples
        self.update_interval = update_interval
        
        # For qutrit visualization
        self.is_qutrit = False
        
        # For run tracking
        self.run_lengths = collections.deque(maxlen=max_samples)
    
    def add_result(self, result):
        """Add a new measurement result"""
        with self.lock:
            self.results.append(result)
            # Keep only the most recent max_samples
            if len(self.results) > self.max_samples:
                self.results.pop(0)
    
    def start_visualization(self, title="Quantum Randomness Visualization", is_qutrit=False):
        """Start the visualization thread"""
        self.is_qutrit = is_qutrit
        self.running = True
        
        # Create figure with multiple subplots
        self.fig, self.axes = plt.subplots(2, 2, figsize=(12, 8))
        self.fig.suptitle(title, fontsize=16)
        
        # Flatten axes for easier indexing
        self.axes = self.axes.flatten()
        
        # Configure plots based on qutrit mode
        if self.is_qutrit:
            self.axes[0].set_title("Measurement Distribution")
            self.axes[0].set_xlabel("Outcome")
            self.axes[0].set_ylabel("Frequency")
            self.axes[0].set_xticks([0, 1, 2])
            
            self.axes[1].set_title("Running Probability")
            self.axes[1].set_xlabel("Sample")
            self.axes[1].set_ylabel("Probability")
            self.axes[1].set_ylim(0, 0.5)
            self.axes[1].axhline(y=1/3, color='r', linestyle='--', alpha=0.7, label='Ideal (1/3)')
            self.axes[1].legend()
            
            self.axes[2].set_title("Last 50 Measurements")
            self.axes[2].set_xlabel("Sample")
            self.axes[2].set_ylabel("Outcome")
            self.axes[2].set_ylim(-0.5, 2.5)
            self.axes[2].set_yticks([0, 1, 2])
        else:
            self.axes[0].set_title("Coin Toss Distribution")
            self.axes[0].set_xlabel("Outcome")
            self.axes[0].set_ylabel("Frequency")
            self.axes[0].set_xticks([0, 1])
            self.axes[0].set_xticklabels(['0 (Heads)', '1 (Tails)'])
            
            self.axes[1].set_title("Running Probability")
            self.axes[1].set_xlabel("Sample")
            self.axes[1].set_ylabel("Probability of 1 (Tails)")
            self.axes[1].set_ylim(0, 1)
            self.axes[1].axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='Ideal (0.5)')
            self.axes[1].legend()
            
            self.axes[2].set_title("Last 50 Coin Tosses")
            self.axes[2].set_xlabel("Sample")
            self.axes[2].set_ylabel("Outcome")
            self.axes[2].set_ylim(-0.5, 1.5)
            self.axes[2].set_yticks([0, 1])
            self.axes[2].set_yticklabels(['0 (Heads)', '1 (Tails)'])
        
        # Fourth plot - run length histogram
        self.axes[3].set_title("Run Length Distribution")
        self.axes[3].set_xlabel("Run Length")
        self.axes[3].set_ylabel("Frequency")
        
        # Start the animation
        self.animation = FuncAnimation(
            self.fig, 
            self._update_plots, 
            interval=self.update_interval,
            blit=False
        )
    
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        plt.ion()  # Turn on interactive mode
        plt.draw()
        plt.pause(0.5)  # Force initial render
    
    def _update_plots(self, frame):
        """Update function for the animation"""
        with self.lock:
            data = list(self.results)  # Make a copy to avoid thread issues
        
        if not data:
            return self.axes
        
        # Clear all axes
        for ax in self.axes:
            ax.clear()
        
        # Plot 1: Distribution
        if self.is_qutrit:
            values, counts = np.unique(data, return_counts=True)
            self.axes[0].bar(values, counts, color=['blue', 'green', 'orange'])
            self.axes[0].set_title("Measurement Distribution")
            self.axes[0].set_xlabel("Outcome")
            self.axes[0].set_ylabel("Frequency")
            self.axes[0].set_xticks([0, 1, 2])
            
            # Add ideal reference
            total = len(data)
            if total > 0:
                for i in range(3):
                    if i not in values:
                        values = np.append(values, i)
                        counts = np.append(counts, 0)
                ideal = total / 3
                self.axes[0].axhline(y=ideal, color='r', linestyle='--', label='Ideal')
                self.axes[0].legend()
        else:
            values, counts = np.unique(data, return_counts=True)
            self.axes[0].bar([0, 1], [data.count(0), data.count(1)], color=['blue', 'orange'])
            self.axes[0].set_title("Coin Toss Distribution")
            self.axes[0].set_xlabel("Outcome")
            self.axes[0].set_ylabel("Frequency")
            self.axes[0].set_xticks([0, 1])
            self.axes[0].set_xticklabels(['0 (Heads)', '1 (Tails)'])
            
            # Add ideal reference
            ideal = len(data) / 2
            self.axes[0].axhline(y=ideal, color='r', linestyle='--', label='Ideal')
            self.axes[0].legend()
        
        # Plot 2: Running probability
        x = list(range(1, len(data) + 1))
        if self.is_qutrit:
            # Calculate running probabilities for each outcome
            running_p0 = [data[:i+1].count(0) / (i+1) for i in range(len(data))]
            running_p1 = [data[:i+1].count(1) / (i+1) for i in range(len(data))]
            running_p2 = [data[:i+1].count(2) / (i+1) for i in range(len(data))]
            
            self.axes[1].plot(x, running_p0, 'b-', label='P(0)', alpha=0.7)
            self.axes[1].plot(x, running_p1, 'g-', label='P(1)', alpha=0.7)
            self.axes[1].plot(x, running_p2, 'orange', label='P(2)', alpha=0.7)
            self.axes[1].set_title("Running Probability")
            self.axes[1].set_xlabel("Sample")
            self.axes[1].set_ylabel("Probability")
            self.axes[1].set_ylim(0, 0.5)
            self.axes[1].axhline(y=1/3, color='r', linestyle='--', alpha=0.7, label='Ideal (1/3)')
            self.axes[1].legend()
        else:
            # Calculate running probability of 1
            running_prob = [data[:i+1].count(1) / (i+1) for i in range(len(data))]
            
            self.axes[1].plot(x, running_prob, 'b-')
            self.axes[1].set_title("Running Probability")
            self.axes[1].set_xlabel("Sample")
            self.axes[1].set_ylabel("Probability of 1 (Tails)")
            self.axes[1].set_ylim(0, 1)
            self.axes[1].axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='Ideal (0.5)')
            self.axes[1].legend()
        
        # Plot 3: Last 50 measurements
        recent_data = data[-50:] if len(data) > 50 else data
        indices = list(range(len(recent_data)))
        
        if self.is_qutrit:
            colors = ['blue' if x == 0 else 'green' if x == 1 else 'orange' for x in recent_data]
            self.axes[2].scatter(indices, recent_data, color=colors)
            self.axes[2].set_title("Last 50 Measurements")
            self.axes[2].set_xlabel("Sample")
            self.axes[2].set_ylabel("Outcome")
            self.axes[2].set_ylim(-0.5, 2.5)
            self.axes[2].set_yticks([0, 1, 2])
        else:
            colors = ['blue' if x == 0 else 'orange' for x in recent_data]
            self.axes[2].scatter(indices, recent_data, color=colors)
            self.axes[2].set_title("Last 50 Coin Tosses")
            self.axes[2].set_xlabel("Sample")
            self.axes[2].set_ylabel("Outcome")
            self.axes[2].set_ylim(-0.5, 1.5)
            self.axes[2].set_yticks([0, 1])
            self.axes[2].set_yticklabels(['0 (Heads)', '1 (Tails)'])
        
        # Plot 4: Run length analysis
        self._update_run_lengths(data)
        if self.run_lengths:
            values, counts = np.unique(self.run_lengths, return_counts=True)
            self.axes[3].bar(values, counts)
            self.axes[3].set_title("Run Length Distribution")
            self.axes[3].set_xlabel("Run Length")
            self.axes[3].set_ylabel("Frequency")
            
            # Optional: Add theoretical exponential decay for fair coin
            if not self.is_qutrit:
                max_run = max(self.run_lengths)
                x = np.arange(1, max_run + 1)
                y = [len(self.run_lengths) * 0.5**i for i in x]
                self.axes[3].plot(x, y, 'r--', label='Theory')
                self.axes[3].legend()
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.9)
        
        return self.axes
    
    def _update_run_lengths(self, data):
        """Update the run length statistics"""
        if not data:
            return
        
        # Calculate run lengths
        run_lengths = []
        current_run = 1
        
        for i in range(1, len(data)):
            if data[i] == data[i-1]:
                current_run += 1
            else:
                run_lengths.append(current_run)
                current_run = 1
        
        # Add the last run
        run_lengths.append(current_run)
        
        # Update the deque
        self.run_lengths = collections.deque(run_lengths, maxlen=self.max_samples)
    
    def stop_visualization(self):
        """Stop the visualization"""
        self.running = False
        if self.animation:
            self.animation.event_source.stop()
        
        if self.fig:
            plt.close(self.fig)
    
    def save_visualization(self, filename="quantum_visualization.png"):
        """Save the current visualization state to a file"""
        if self.fig:
            self.fig.savefig(filename)
            print(f"Visualization saved to {filename}")


# Example usage (when run directly)
if __name__ == "__main__":
    import random
    
    # Demo random coin tosses
    visualizer = QuantumVisualizer()
    visualizer.start_visualization(title="Demo Coin Toss Visualization")
    
    try:
        for _ in range(200):
            # Simulate a coin toss
            result = random.randint(0, 1)
            visualizer.add_result(result)
            time.sleep(0.05)
    except KeyboardInterrupt:
        print("Interrupted by user")
    finally:
        visualizer.save_visualization()
        time.sleep(1)
        visualizer.stop_visualization()