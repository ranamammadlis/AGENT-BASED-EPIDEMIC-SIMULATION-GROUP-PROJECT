import matplotlib.pyplot as plt
import numpy as np
from sir_core_engine import *

def plot_sir_comparison(scenarios: Dict, title: str = "Intervention Comparison"):
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, result) in enumerate(scenarios.items()):
        if idx >= 6:
            break
        
        ax = axes[idx]
        history = result['history']
        
        ax.plot(history['t'], history['S'], 'b-', label='S', linewidth=2)
        ax.plot(history['t'], history['I'], 'r-', label='I', linewidth=2)
        ax.plot(history['t'], history['R'], 'g-', label='R', linewidth=2)
        
        ax.set_title(f"{name}\nAttack: {result['attack_rate']:.1%}, Peak: {result['peak_infected']}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    for idx in range(len(scenarios), 6):
        axes[idx].axis('off')
    
    plt.suptitle(title, fontsize=16, fontweight='bold')
    plt.tight_layout()
    return fig

def plot_vaccination_comparison(comparison: Dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    strategies = list(comparison['summary'].keys())
    attack_means = [comparison['summary'][s]['mean_attack_rate'] for s in strategies]
    attack_stds = [comparison['summary'][s]['std_attack_rate'] for s in strategies]
    peak_means = [comparison['summary'][s]['mean_peak'] for s in strategies]
    peak_stds = [comparison['summary'][s]['std_peak'] for s in strategies]
    
    x_pos = np.arange(len(strategies))
    colors = ['gray', 'orange', 'green']
    
    ax1.bar(x_pos, attack_means, yerr=attack_stds, color=colors, alpha=0.7, capsize=5)
    ax1.set_xticks(x_pos)
    ax1.set_xticklabels(strategies)
    ax1.set_ylabel('Attack Rate')
    ax1.set_title('Final Attack Rate by Strategy')
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2.bar(x_pos, peak_means, yerr=peak_stds, color=colors, alpha=0.7, capsize=5)
    ax2.set_xticks(x_pos)
    ax2.set_xticklabels(strategies)
    ax2.set_ylabel('Peak Infected')
    ax2.set_title('Peak Infected by Strategy')
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    return fig

def plot_intervention_sweep(results: Dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    coverage = np.array(results['coverage']) * 100
    
    ax1.plot(coverage, results['random_attack'], 'o-', label='Random', 
             color='orange', linewidth=2, markersize=6)
    ax1.plot(coverage, results['targeted_attack'], 's-', label='Targeted', 
             color='green', linewidth=2, markersize=6)
    ax1.set_xlabel('Vaccination Coverage (%)')
    ax1.set_ylabel('Attack Rate')
    ax1.set_title('Attack Rate vs Coverage')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    ax2.plot(coverage, results['random_peak'], 'o-', label='Random', 
             color='orange', linewidth=2, markersize=6)
    ax2.plot(coverage, results['targeted_peak'], 's-', label='Targeted', 
             color='green', linewidth=2, markersize=6)
    ax2.set_xlabel('Vaccination Coverage (%)')
    ax2.set_ylabel('Peak Infected')
    ax2.set_title('Peak Infected vs Coverage')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig

def plot_network_vaccination(graph: nx.Graph, vaccinated: set, states: Dict):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    pos = nx.spring_layout(graph, k=1, iterations=50, seed=42)
    
    node_colors_vac = ['red' if n in vaccinated else 'lightblue' for n in graph.nodes()]
    ax1.set_title('Vaccinated Nodes (Red)')
    nx.draw(graph, pos, node_color=node_colors_vac, node_size=300, 
            with_labels=False, ax=ax1, edge_color='gray', alpha=0.5)
    
    color_map = {'S': 'lightblue', 'I': 'red', 'R': 'lightgreen'}
    node_colors_state = [color_map[states[n]] for n in graph.nodes()]
    ax2.set_title('Final Epidemic State')
    nx.draw(graph, pos, node_color=node_colors_state, node_size=300, 
            with_labels=False, ax=ax2, edge_color='gray', alpha=0.5)
    
    plt.tight_layout()
    return fig

def generate_report(scenarios: Dict, comparison: Dict = None, filename: str = 'report.txt'):
    with open(filename, 'w') as f:
        f.write("="*70 + "\n")
        f.write("SIR INTERVENTION ANALYSIS REPORT\n")
        f.write("="*70 + "\n\n")
        
        f.write("INTERVENTION SCENARIOS\n")
        f.write("-"*70 + "\n")
        for name, result in scenarios.items():
            f.write(f"\n{name}:\n")
            f.write(f"  Attack Rate: {result['attack_rate']:.2%}\n")
            f.write(f"  Peak Infected: {result['peak_infected']}\n")
            f.write(f"  Duration: {result['duration']} steps\n")
            f.write(f"  Final Size: {result['final_size']}\n")
        
        if comparison:
            f.write("\n\nVACCINATION STRATEGY COMPARISON\n")
            f.write("-"*70 + "\n")
            for strategy, stats in comparison['summary'].items():
                f.write(f"\n{strategy.upper()}:\n")
                f.write(f"  Mean Attack Rate: {stats['mean_attack_rate']:.2%} ± {stats['std_attack_rate']:.2%}\n")
                f.write(f"  Mean Peak Infected: {stats['mean_peak']:.1f} ± {stats['std_peak']:.1f}\n")
        
        f.write("\n" + "="*70 + "\n")

if __name__ == '__main__':
    
    G = nx.barabasi_albert_graph(150, 3)
    beta, gamma = 0.35, 0.1
    
    print("Running intervention scenarios...")
    scenarios = run_intervention_scenarios(G, beta, gamma)
    
    print("Running vaccination comparison...")
    comparison = compare_vaccination_strategies(G, beta, gamma, coverage=0.25, n_runs=50)
    
    print("Creating plots...")
    
    fig1 = plot_sir_comparison(scenarios, "SIR Intervention Scenarios")
    plt.savefig('intervention_scenarios.png', dpi=300, bbox_inches='tight')
    
    fig2 = plot_vaccination_comparison(comparison)
    plt.savefig('vaccination_comparison.png', dpi=300, bbox_inches='tight')
    
    print("\nRunning coverage sweep...")
    coverage_range = np.linspace(0, 0.6, 13)
    sweep_results = intervention_sweep(
        lambda: nx.barabasi_albert_graph(150, 3), 
        beta, gamma, coverage_range, n_runs=30
    )
    
    fig3 = plot_intervention_sweep(sweep_results)
    plt.savefig('coverage_sweep.png', dpi=300, bbox_inches='tight')
    
    print("Generating report...")
    generate_report(scenarios, comparison, 'intervention_report.txt')
    
    print("\nAll plots saved!")
    print("Report saved to: intervention_report.txt")
    
    plt.show()
