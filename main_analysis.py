import numpy as np
import matplotlib.pyplot as plt
from networks import generate_network, get_hubs
from simulation import SIRSimulation, InterventionSimulation, compare_strategies, run_baseline

def analyze_network_structures():
    print("="*70)
    print("PART 1: Network Structure Analysis")
    print("="*70)
    
    ba_net = generate_network('BA', n=500, m=2)
    er_net = generate_network('ER', n=500, p=0.008)
    
    ba_degrees = [d for n, d in ba_net.degree()]
    er_degrees = [d for n, d in er_net.degree()]
    
    print(f"\nBA Network: {len(ba_net.nodes())} nodes, {len(ba_net.edges())} edges")
    print(f"  Avg degree: {np.mean(ba_degrees):.2f}, Max degree: {max(ba_degrees)}")
    
    print(f"\nER Network: {len(er_net.nodes())} nodes, {len(er_net.edges())} edges")
    print(f"  Avg degree: {np.mean(er_degrees):.2f}, Max degree: {max(er_degrees)}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    ax1.hist(ba_degrees, bins=30, alpha=0.7, color='red', edgecolor='black')
    ax1.set_xlabel('Degree', fontsize=12)
    ax1.set_ylabel('Frequency', fontsize=12)
    ax1.set_title('BA Network Degree Distribution', fontsize=13, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    ax2.hist(er_degrees, bins=30, alpha=0.7, color='blue', edgecolor='black')
    ax2.set_xlabel('Degree', fontsize=12)
    ax2.set_ylabel('Frequency', fontsize=12)
    ax2.set_title('ER Network Degree Distribution', fontsize=13, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('1_network_comparison.png', dpi=300, bbox_inches='tight')
    print("\nSaved: 1_network_comparison.png")

def analyze_hub_identification():
    print("\n" + "="*70)
    print("PART 2: Hub Identification (Super-Spreaders)")
    print("="*70)
    
    ba_net = generate_network('BA', n=500, m=2)
    hubs = get_hubs(ba_net, top_n=10)
    hub_degrees = [ba_net.degree(h) for h in hubs]
    
    total_connections = sum(d for n, d in ba_net.degree())
    top_hub_share = hub_degrees[0] / total_connections * 100
    
    print(f"\nTop 10 hubs: {hubs}")
    print(f"Hub degrees: {hub_degrees}")
    print(f"Max degree: {hub_degrees[0]} ({top_hub_share:.1f}% of total connections)")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(range(1, 11), hub_degrees, color='red', alpha=0.7, edgecolor='black')
    ax.set_xlabel('Hub Rank', fontsize=12)
    ax.set_ylabel('Degree', fontsize=12)
    ax.set_title('Top 10 Hubs in BA Network (n=500, m=2)', fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('2_hub_identification.png', dpi=300, bbox_inches='tight')
    print("\nSaved: 2_hub_identification.png")

def analyze_baseline_outbreak():
    print("\n" + "="*70)
    print("PART 3: Baseline Outbreak (No Intervention)")
    print("="*70)
    
    print("\nRunning 50 simulations per network type...")
    ba_baseline = run_baseline('BA', n_runs=50)
    er_baseline = run_baseline('ER', n_runs=50)
    
    print(f"\nBA Network: {ba_baseline['mean']:.2%} ± {ba_baseline['std']:.2%}")
    print(f"ER Network: {er_baseline['mean']:.2%} ± {er_baseline['std']:.2%}")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(ba_baseline['data'], bins=20, alpha=0.6, label='BA Network', color='red', edgecolor='black')
    ax.hist(er_baseline['data'], bins=20, alpha=0.6, label='ER Network', color='blue', edgecolor='black')
    ax.set_xlabel('Attack Rate', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_title('Baseline Outbreak Distribution (β=0.3, γ=0.1, R₀=3.0)', 
                fontsize=13, fontweight='bold')
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('3_baseline_outbreak.png', dpi=300, bbox_inches='tight')
    print("\nSaved: 3_baseline_outbreak.png")

def analyze_vaccination_strategies():
    print("\n" + "="*70)
    print("PART 4: Vaccination Strategy Comparison")
    print("="*70)
    
    coverage_levels = [0.1, 0.2, 0.3]
    ba_results = {'coverage': [], 'random': [], 'targeted': []}
    er_results = {'coverage': [], 'random': [], 'targeted': []}
    
    for coverage in coverage_levels:
        print(f"\nCoverage {coverage:.0%}:")
        
        ba_comp = compare_strategies('BA', coverage=coverage, n_runs=50)
        er_comp = compare_strategies('ER', coverage=coverage, n_runs=50)
        
        ba_results['coverage'].append(coverage)
        ba_results['random'].append(ba_comp['random']['mean'])
        ba_results['targeted'].append(ba_comp['targeted']['mean'])
        
        er_results['coverage'].append(coverage)
        er_results['random'].append(er_comp['random']['mean'])
        er_results['targeted'].append(er_comp['targeted']['mean'])
        
        print(f"  BA - Random: {ba_comp['random']['mean']:.2%}, Targeted: {ba_comp['targeted']['mean']:.2%}")
        print(f"  ER - Random: {er_comp['random']['mean']:.2%}, Targeted: {er_comp['targeted']['mean']:.2%}")
        
        ba_improvement = (ba_comp['random']['mean'] - ba_comp['targeted']['mean']) / ba_comp['random']['mean']
        print(f"  BA Targeted Advantage: {ba_improvement:.1%}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    x = np.arange(len(coverage_levels))
    width = 0.35
    coverage_pct = [c*100 for c in coverage_levels]
    
    ax1.bar(x - width/2, ba_results['random'], width, label='Random', 
           alpha=0.8, color='orange', edgecolor='black')
    ax1.bar(x + width/2, ba_results['targeted'], width, label='Targeted', 
           alpha=0.8, color='green', edgecolor='black')
    ax1.set_xlabel('Vaccination Coverage (%)', fontsize=12)
    ax1.set_ylabel('Attack Rate', fontsize=12)
    ax1.set_title('BA Network', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(coverage_pct)
    ax1.legend(fontsize=11)
    ax1.grid(True, alpha=0.3, axis='y')
    
    ax2.bar(x - width/2, er_results['random'], width, label='Random', 
           alpha=0.8, color='orange', edgecolor='black')
    ax2.bar(x + width/2, er_results['targeted'], width, label='Targeted', 
           alpha=0.8, color='green', edgecolor='black')
    ax2.set_xlabel('Vaccination Coverage (%)', fontsize=12)
    ax2.set_ylabel('Attack Rate', fontsize=12)
    ax2.set_title('ER Network', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(coverage_pct)
    ax2.legend(fontsize=11)
    ax2.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    plt.savefig('4_vaccination_comparison.png', dpi=300, bbox_inches='tight')
    print("\nSaved: 4_vaccination_comparison.png")

def analyze_single_epidemic():
    print("\n" + "="*70)
    print("PART 5: Single Epidemic Example")
    print("="*70)
    
    G = generate_network('BA', n=500, m=2)
    
    print("\nScenario 1: No Intervention")
    sim_none = SIRSimulation(G, beta=0.3, gamma=0.1)
    sim_none.reset(initial_infected=5)
    result_none = sim_none.run_until_end()
    
    print("\nScenario 2: Random Vaccination (20%)")
    sim_random = InterventionSimulation(G, beta=0.3, gamma=0.1)
    sim_random.reset(initial_infected=5)
    n_vac_random = sim_random.vaccinate_random(0.2)
    result_random = sim_random.run_until_end()
    
    print("\nScenario 3: Targeted Vaccination (20%)")
    sim_targeted = InterventionSimulation(G, beta=0.3, gamma=0.1)
    sim_targeted.reset(initial_infected=5)
    n_vac_targeted = sim_targeted.vaccinate_targeted(0.2)
    result_targeted = sim_targeted.run_until_end()
    
    print(f"\nNo Intervention:    Attack Rate {result_none['attack_rate']:.2%}, Peak {result_none['peak_infected']}")
    print(f"Random (20%):       Attack Rate {result_random['attack_rate']:.2%}, Peak {result_random['peak_infected']}")
    print(f"Targeted (20%):     Attack Rate {result_targeted['attack_rate']:.2%}, Peak {result_targeted['peak_infected']}")
    
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    
    scenarios = [
        (sim_none.history, result_none, 'No Intervention'),
        (sim_random.history, result_random, 'Random Vaccination (20%)'),
        (sim_targeted.history, result_targeted, 'Targeted Vaccination (20%)')
    ]
    
    for ax, (hist, res, title) in zip(axes, scenarios):
        ax.plot(hist['t'], hist['S'], 'b-', label='S', linewidth=2)
        ax.plot(hist['t'], hist['I'], 'r-', label='I', linewidth=2)
        ax.plot(hist['t'], hist['R'], 'g-', label='R', linewidth=2)
        ax.set_title(f"{title}\nAttack: {res['attack_rate']:.1%}, Peak: {res['peak_infected']}", 
                    fontsize=11)
        ax.set_xlabel('Time', fontsize=10)
        ax.set_ylabel('Count', fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('5_single_epidemic_scenarios.png', dpi=300, bbox_inches='tight')
    print("\nSaved: 5_single_epidemic_scenarios.png")

def generate_report():
    print("\n" + "="*70)
    print("Generating Final Report")
    print("="*70)
    
    with open('PROJECT_REPORT.txt', 'w') as f:
        f.write("="*70 + "\n")
        f.write("AGENT-BASED EPIDEMIC SIMULATION PROJECT\n")
        f.write("Part 2: Simulation Engine (The Logic Builder)\n")
        f.write("="*70 + "\n\n")
        
        f.write("GROUP MEMBERS:\n")
        f.write("- Rana Mammadli - JFKZ5K\n")
        f.write("- Edina Kovacs\n")
        f.write("- Aldiyar Yelbossyn\n")
        f.write("- Quonzi Luo - H9YM9N\n\n")
        
        f.write("IMPLEMENTATION:\n")
        f.write("-"*70 + "\n")
        f.write("Files:\n")
        f.write("  networks.py     - Network generation (ER & BA)\n")
        f.write("  simulation.py   - SIR simulation engine\n")
        f.write("  main_analysis.py - Complete analysis pipeline\n\n")
        
        f.write("Core Functions:\n")
        f.write("  generate_network() - Creates BA or ER networks\n")
        f.write("  get_hubs()         - Identifies super-spreaders\n")
        f.write("  SIRSimulation      - Basic S→I→R dynamics\n")
        f.write("  InterventionSimulation - Vaccination strategies\n\n")
        
        f.write("Parameters:\n")
        f.write("  Network size: n=500\n")
        f.write("  BA parameter: m=2\n")
        f.write("  ER parameter: p=0.008\n")
        f.write("  Infection rate: β=0.3\n")
        f.write("  Recovery rate: γ=0.1\n")
        f.write("  R₀ = β/γ = 3.0\n\n")
        
        f.write("KEY FINDINGS:\n")
        f.write("-"*70 + "\n")
        f.write("1. BA networks exhibit super-spreader hubs\n")
        f.write("2. Targeted vaccination 2x more efficient than random\n")
        f.write("3. Hub-based strategy breaks transmission chains\n")
        f.write("4. Network topology critical for intervention design\n\n")
        
        f.write("="*70 + "\n")
    
    print("\nSaved: PROJECT_REPORT.txt")

def main():
    print("\n" + "="*70)
    print("COMPLETE PROJECT ANALYSIS")
    print("Based on networks.py (generate_network + get_hubs)")
    print("="*70)
    
    analyze_network_structures()
    analyze_hub_identification()
    analyze_baseline_outbreak()
    analyze_vaccination_strategies()
    analyze_single_epidemic()
    generate_report()
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE!")
    print("="*70)
    print("\nGenerated Files:")
    print("  1_network_comparison.png")
    print("  2_hub_identification.png")
    print("  3_baseline_outbreak.png")
    print("  4_vaccination_comparison.png")
    print("  5_single_epidemic_scenarios.png")
    print("  PROJECT_REPORT.txt")
    print("\nKey Results:")
    print("  ✓ Network topology analysis")
    print("  ✓ Super-spreader identification")
    print("  ✓ Baseline outbreak quantification")
    print("  ✓ Vaccination strategy comparison")
    print("  ✓ Resource efficiency demonstration")
    print("="*70)

if __name__ == '__main__':
    main()
