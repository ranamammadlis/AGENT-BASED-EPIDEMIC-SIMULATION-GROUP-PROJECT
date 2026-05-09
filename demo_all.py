import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
from sir_core_engine import *

def demo_basic_sir():
    print("\n" + "="*70)
    print("DEMO 1: Basic SIR Simulation")
    print("="*70)
    
    G = nx.watts_strogatz_graph(100, 6, 0.3)
    engine = SIREngine(G, beta=0.3, gamma=0.1)
    engine.reset(initial_infected=5)
    
    result = engine.run_epidemic()
    
    print(f"Parameters: β={engine.beta}, γ={engine.gamma}, R₀={engine.beta/engine.gamma:.2f}")
    print(f"Network: {len(G.nodes())} nodes, {len(G.edges())} edges")
    print(f"\nResults:")
    print(f"  Final size: {result['final_size']}/{engine.N}")
    print(f"  Attack rate: {result['attack_rate']:.2%}")
    print(f"  Peak infected: {result['peak_infected']}")
    print(f"  Duration: {result['duration']} steps")
    
    plt.figure(figsize=(10, 6))
    plt.plot(result['history']['t'], result['history']['S'], 'b-', label='Susceptible', linewidth=2)
    plt.plot(result['history']['t'], result['history']['I'], 'r-', label='Infected', linewidth=2)
    plt.plot(result['history']['t'], result['history']['R'], 'g-', label='Recovered', linewidth=2)
    plt.xlabel('Time Steps')
    plt.ylabel('Number of Individuals')
    plt.title(f'Basic SIR Dynamics (β={engine.beta}, γ={engine.gamma}, R₀={engine.beta/engine.gamma:.2f})')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('demo_basic_sir.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved: demo_basic_sir.png")

def demo_random_vaccination():
    print("\n" + "="*70)
    print("DEMO 2: Random Vaccination")
    print("="*70)
    
    G = nx.barabasi_albert_graph(100, 3)
    
    results = {}
    for coverage in [0, 0.2, 0.4, 0.6]:
        engine = InterventionEngine(G, beta=0.4, gamma=0.1)
        engine.reset(initial_infected=3)
        
        if coverage > 0:
            n_vac = engine.vaccinate_random(coverage)
            print(f"\nCoverage {coverage:.0%}: Vaccinated {n_vac} individuals")
        else:
            print(f"\nNo vaccination (baseline)")
        
        result = engine.run_epidemic()
        results[f"{coverage:.0%}"] = result
        
        print(f"  Attack rate: {result['attack_rate']:.2%}")
        print(f"  Peak infected: {result['peak_infected']}")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for idx, (label, result) in enumerate(results.items()):
        ax = axes[idx]
        h = result['history']
        ax.plot(h['t'], h['S'], 'b-', label='S', linewidth=2)
        ax.plot(h['t'], h['I'], 'r-', label='I', linewidth=2)
        ax.plot(h['t'], h['R'], 'g-', label='R', linewidth=2)
        ax.set_title(f"Coverage: {label} | Attack: {result['attack_rate']:.1%}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_random_vaccination.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved: demo_random_vaccination.png")

def demo_targeted_vaccination():
    print("\n" + "="*70)
    print("DEMO 3: Targeted vs Random Vaccination")
    print("="*70)
    
    G = nx.barabasi_albert_graph(150, 4)
    beta, gamma = 0.35, 0.1
    coverage = 0.3
    
    print(f"\nNetwork: Scale-free (Barabási-Albert)")
    print(f"Parameters: β={beta}, γ={gamma}, R₀={beta/gamma:.2f}")
    print(f"Coverage: {coverage:.0%}")
    
    engine_random = InterventionEngine(G, beta, gamma)
    engine_random.reset(initial_infected=5)
    n_vac_random = engine_random.vaccinate_random(coverage)
    result_random = engine_random.run_epidemic()
    
    engine_targeted = InterventionEngine(G, beta, gamma)
    engine_targeted.reset(initial_infected=5)
    n_vac_targeted = engine_targeted.vaccinate_targeted(coverage, strategy='degree')
    result_targeted = engine_targeted.run_epidemic()
    
    print(f"\nRandom vaccination:")
    print(f"  Vaccinated: {n_vac_random}")
    print(f"  Attack rate: {result_random['attack_rate']:.2%}")
    print(f"  Peak infected: {result_random['peak_infected']}")
    
    print(f"\nTargeted vaccination (high-degree nodes):")
    print(f"  Vaccinated: {n_vac_targeted}")
    print(f"  Attack rate: {result_targeted['attack_rate']:.2%}")
    print(f"  Peak infected: {result_targeted['peak_infected']}")
    
    reduction_attack = (result_random['attack_rate'] - result_targeted['attack_rate']) / result_random['attack_rate']
    reduction_peak = (result_random['peak_infected'] - result_targeted['peak_infected']) / result_random['peak_infected']
    
    print(f"\nTargeted strategy improvement:")
    print(f"  Attack rate reduction: {reduction_attack:.1%}")
    print(f"  Peak reduction: {reduction_peak:.1%}")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    h1 = result_random['history']
    ax1.plot(h1['t'], h1['S'], 'b-', label='S', linewidth=2)
    ax1.plot(h1['t'], h1['I'], 'r-', label='I', linewidth=2)
    ax1.plot(h1['t'], h1['R'], 'g-', label='R', linewidth=2)
    ax1.set_title(f"Random Vaccination\nAttack: {result_random['attack_rate']:.1%}, Peak: {result_random['peak_infected']}")
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Count')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    h2 = result_targeted['history']
    ax2.plot(h2['t'], h2['S'], 'b-', label='S', linewidth=2)
    ax2.plot(h2['t'], h2['I'], 'r-', label='I', linewidth=2)
    ax2.plot(h2['t'], h2['R'], 'g-', label='R', linewidth=2)
    ax2.set_title(f"Targeted Vaccination\nAttack: {result_targeted['attack_rate']:.1%}, Peak: {result_targeted['peak_infected']}")
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Count')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_targeted_vaccination.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved: demo_targeted_vaccination.png")

def demo_multiple_interventions():
    print("\n" + "="*70)
    print("DEMO 4: Combined Interventions")
    print("="*70)
    
    G = nx.watts_strogatz_graph(120, 6, 0.3)
    beta, gamma = 0.4, 0.1
    
    print(f"Baseline: β={beta}, γ={gamma}, R₀={beta/gamma:.2f}")
    
    scenarios = {
        'No intervention': {},
        'Social distancing (50%)': {'distancing': 0.5},
        'Vaccination (20%)': {'vaccine': 0.2},
        'Treatment improvement (40%)': {'treatment': 0.4},
        'Combined (vac+dist)': {'vaccine': 0.2, 'distancing': 0.3}
    }
    
    results = {}
    
    for name, config in scenarios.items():
        engine = InterventionEngine(G, beta, gamma)
        engine.reset(initial_infected=3)
        
        if 'vaccine' in config:
            engine.vaccinate_targeted(config['vaccine'], strategy='degree')
        if 'distancing' in config:
            engine.apply_social_distancing(config['distancing'])
        if 'treatment' in config:
            engine.apply_treatment(config['treatment'])
        
        result = engine.run_epidemic()
        results[name] = result
        
        print(f"\n{name}:")
        if 'distancing' in config:
            print(f"  Effective β: {engine.beta:.3f}")
        if 'treatment' in config:
            print(f"  Effective γ: {engine.gamma:.3f}")
        print(f"  Attack rate: {result['attack_rate']:.2%}")
        print(f"  Peak infected: {result['peak_infected']}")
    
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    axes = axes.flatten()
    
    for idx, (name, result) in enumerate(results.items()):
        ax = axes[idx]
        h = result['history']
        ax.plot(h['t'], h['S'], 'b-', label='S', linewidth=2)
        ax.plot(h['t'], h['I'], 'r-', label='I', linewidth=2)
        ax.plot(h['t'], h['R'], 'g-', label='R', linewidth=2)
        ax.set_title(f"{name}\nAttack: {result['attack_rate']:.1%}, Peak: {result['peak_infected']}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    axes[5].axis('off')
    
    plt.tight_layout()
    plt.savefig('demo_combined_interventions.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved: demo_combined_interventions.png")

def demo_network_comparison():
    print("\n" + "="*70)
    print("DEMO 5: Network Structure Impact")
    print("="*70)
    
    beta, gamma = 0.3, 0.1
    n = 100
    
    networks = {
        'Small World': nx.watts_strogatz_graph(n, 6, 0.3),
        'Scale-Free': nx.barabasi_albert_graph(n, 3),
        'Random': nx.erdos_renyi_graph(n, 0.06),
        'Grid': nx.grid_2d_graph(10, 10)
    }
    
    results = {}
    
    for name, G in networks.items():
        engine = SIREngine(G, beta, gamma)
        engine.reset(initial_infected=3)
        result = engine.run_epidemic()
        results[name] = result
        
        avg_degree = np.mean([d for n, d in G.degree()])
        print(f"\n{name}:")
        print(f"  Nodes: {len(G.nodes())}, Edges: {len(G.edges())}")
        print(f"  Avg degree: {avg_degree:.2f}")
        print(f"  Attack rate: {result['attack_rate']:.2%}")
        print(f"  Peak infected: {result['peak_infected']}")
    
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    axes = axes.flatten()
    
    for idx, (name, result) in enumerate(results.items()):
        ax = axes[idx]
        h = result['history']
        ax.plot(h['t'], h['S'], 'b-', label='S', linewidth=2)
        ax.plot(h['t'], h['I'], 'r-', label='I', linewidth=2)
        ax.plot(h['t'], h['R'], 'g-', label='R', linewidth=2)
        ax.set_title(f"{name}\nAttack: {result['attack_rate']:.1%}, Peak: {result['peak_infected']}")
        ax.set_xlabel('Time')
        ax.set_ylabel('Count')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('demo_network_comparison.png', dpi=300, bbox_inches='tight')
    print("\nPlot saved: demo_network_comparison.png")

if __name__ == '__main__':
    print("\n" + "="*70)
    print("SIR EPIDEMIC SIMULATION ENGINE - DEMONSTRATION")
    print("="*70)
    
    demo_basic_sir()
    demo_random_vaccination()
    demo_targeted_vaccination()
    demo_multiple_interventions()
    demo_network_comparison()
    
    print("\n" + "="*70)
    print("All demonstrations completed!")
    print("Check the generated PNG files for visualizations")
    print("="*70)
