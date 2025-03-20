import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

def analyze_coin_tosses(results):
    """
    Analyze the statistics of a sequence of coin tosses
    
    Args:
        results: List of 0s and 1s representing coin toss outcomes
        
    Returns:
        dict: Dictionary containing statistical analysis results
    """
    if not results:
        return {"error": "No results provided"}
    
    # Basic counts
    total = len(results)
    zeros = results.count(0)
    ones = results.count(1)
    
    # Probabilities
    p0 = zeros / total
    p1 = ones / total
    
    # Bias from fair coin (0.5)
    bias = abs(p1 - 0.5)
    
    # Calculate run statistics
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
    
    # Calculate entropy (measure of randomness)
    # Shannon entropy is -sum(p_i * log2(p_i))
    if p0 > 0 and p1 > 0:
        entropy = -p0 * np.log2(p0) - p1 * np.log2(p1)
    else:
        entropy = 0  # One of the probabilities is 0
    
    # Maximum entropy for binary distribution is 1 bit
    entropy_ratio = entropy / 1.0
    
    # Chi-squared test for goodness of fit to uniform distribution
    expected = [total/2, total/2]  # Expected counts for fair coin
    observed = [zeros, ones]
    chi2, p_value = stats.chisquare(observed, expected)
    
    # Autocorrelation at lag 1 (measure of independence)
    if len(results) > 1:
        autocorr = np.corrcoef(results[:-1], results[1:])[0, 1]
    else:
        autocorr = 0
    
    # Compile the results
    analysis = {
        "total_tosses": total,
        "zeros": zeros,
        "ones": ones,
        "p0": p0,
        "p1": p1,
        "bias": bias,
        "runs": {
            "total_runs": len(runs),
            "max_run": max(runs) if runs else 0,
            "avg_run": np.mean(runs) if runs else 0
        },
        "entropy": {
            "value": entropy,
            "ratio_to_max": entropy_ratio
        },
        "chi_squared": {
            "statistic": chi2,
            "p_value": p_value,
            "is_random": p_value > 0.05  # Null hypothesis not rejected at 5% significance
        },
        "autocorrelation": autocorr
    }
    
    return analysis

def print_analysis(analysis):
    """Print analysis results in a readable format"""
    print("\n==== Quantum Coin Toss Analysis ====")
    print(f"Total tosses: {analysis['total_tosses']}")
    print(f"Heads (0): {analysis['zeros']} ({analysis['p0']:.4f})")
    print(f"Tails (1): {analysis['ones']} ({analysis['p1']:.4f})")
    print(f"Bias from fair: {analysis['bias']:.4f}")
    
    print("\nRun Statistics:")
    print(f"Number of runs: {analysis['runs']['total_runs']}")
    print(f"Longest run: {analysis['runs']['max_run']}")
    print(f"Average run length: {analysis['runs']['avg_run']:.2f}")
    
    print("\nRandomness Metrics:")
    print(f"Entropy: {analysis['entropy']['value']:.4f} bits (Ratio to max: {analysis['entropy']['ratio_to_max']:.4f})")
    print(f"Chi-squared: {analysis['chi_squared']['statistic']:.4f} (p-value: {analysis['chi_squared']['p_value']:.4f})")
    print(f"Statistical randomness: {'Yes' if analysis['chi_squared']['is_random'] else 'No'}")
    print(f"Autocorrelation (lag 1): {analysis['autocorrelation']:.4f}")
    
    # Interpretation
    if analysis['chi_squared']['is_random'] and abs(analysis['autocorrelation']) < 0.1:
        print("\nInterpretation: Results appear statistically random")
    elif not analysis['chi_squared']['is_random']:
        print("\nInterpretation: Results show some deviation from randomness")
    elif abs(analysis['autocorrelation']) >= 0.1:
        print("\nInterpretation: Results show some serial correlation")

def plot_results(results, title="Quantum Coin Tosses"):
    """Create visualizations for coin toss results"""
    if not results:
        print("No results to plot")
        return
    
    plt.figure(figsize=(15, 10))
    
    # Plot 1: Distribution
    plt.subplot(2, 2, 1)
    values, counts = np.unique(results, return_counts=True)
    plt.bar([0, 1], [results.count(0), results.count(1)])
    plt.xticks([0, 1], ['Heads (0)', 'Tails (1)'])
    plt.ylabel('Frequency')
    plt.title('Outcome Distribution')
    
    # Add reference line for expected counts
    expected = len(results) / 2
    plt.axhline(y=expected, color='r', linestyle='--', alpha=0.7, label='Expected (50%)')
    plt.legend()
    
    # Plot 2: Running probability
    plt.subplot(2, 2, 2)
    x = list(range(1, len(results) + 1))
    # Calculate running probability of 1
    running_prob = [results[:i+1].count(1) / (i+1) for i in range(len(results))]
    
    plt.plot(x, running_prob, 'b-')
    plt.axhline(y=0.5, color='r', linestyle='--', alpha=0.7, label='Expected (0.5)')
    plt.xlabel('Toss Number')
    plt.ylabel('Running Probability of Tails (1)')
    plt.title('Convergence to Theoretical Probability')
    plt.legend()
    
    # Plot 3: Last 50 tosses
    plt.subplot(2, 2, 3)
    recent_data = results[-50:] if len(results) > 50 else results
    indices = list(range(len(recent_data)))
    
    plt.scatter(indices, recent_data, c=['blue' if x == 0 else 'orange' for x in recent_data])
    plt.yticks([0, 1], ['Heads (0)', 'Tails (1)'])
    plt.xlabel('Toss Number')
    plt.title('Last 50 Tosses')
    
    # Plot 4: Run length histogram
    plt.subplot(2, 2, 4)
    
    # Calculate run lengths
    runs = []
    current_run = 1
    for i in range(1, len(results)):
        if results[i] == results[i-1]:
            current_run += 1
        else:
            runs.append(current_run)
            current_run = 1
    runs.append(current_run)
    
    plt.hist(runs, bins=range(1, max(runs) + 2), alpha=0.7, align='left')
    plt.xlabel('Run Length')
    plt.ylabel('Frequency')
    plt.title('Run Length Distribution')
    
    # Optional: Add theoretical exponential decay for fair coin
    max_run = max(runs)
    x = np.arange(1, max_run + 1)
    y = [len(runs) * 0.5**i for i in x]
    plt.plot(x, y, 'r--', label='Theory: P(run=k) ∝ 2^-k')
    plt.legend()
    
    plt.tight_layout()
    plt.suptitle(title, fontsize=16)
    plt.subplots_adjust(top=0.9)
    
    plt.savefig('quantum_toss_analysis.png')
    print("Analysis plot saved as 'quantum_toss_analysis.png'")

if __name__ == "__main__":
    # Test with simulated fair coin data
    from basic_quantum_coin import batched_quantum_coin_toss
    
    print("Generating quantum coin tosses for analysis...")
    results = batched_quantum_coin_toss(num_tosses=100)
    
    # Run analysis
    analysis = analyze_coin_tosses(results)
    print_analysis(analysis)
    
    # Plot results
    plot_results(results, "Quantum Coin Toss Analysis (n=100)")