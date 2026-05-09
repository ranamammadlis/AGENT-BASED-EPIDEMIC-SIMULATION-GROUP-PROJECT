import networkx as nx
import numpy as np
from typing import Dict, List, Tuple, Optional, Callable

class SIREngine:
    
    def __init__(self, graph: nx.Graph, beta: float, gamma: float):
        self.G = graph
        self.beta = beta
        self.gamma = gamma
        self.N = len(graph.nodes())
        self.reset()
    
    def reset(self, initial_infected: int = 1):
        self.states = {node: 'S' for node in self.G.nodes()}
        infected_nodes = np.random.choice(list(self.G.nodes()), 
                                         size=min(initial_infected, self.N), 
                                         replace=False)
        for node in infected_nodes:
            self.states[node] = 'I'
        
        self.time = 0
        self.history = {'S': [], 'I': [], 'R': [], 't': []}
        self._record_state()
    
    def _record_state(self):
        self.history['S'].append(sum(1 for s in self.states.values() if s == 'S'))
        self.history['I'].append(sum(1 for s in self.states.values() if s == 'I'))
        self.history['R'].append(sum(1 for s in self.states.values() if s == 'R'))
        self.history['t'].append(self.time)
    
    def step(self):
        new_states = self.states.copy()
        
        for node in self.G.nodes():
            if self.states[node] == 'S':
                infected_neighbors = [n for n in self.G.neighbors(node) 
                                     if self.states[n] == 'I']
                for _ in infected_neighbors:
                    if np.random.random() < self.beta:
                        new_states[node] = 'I'
                        break
            
            elif self.states[node] == 'I':
                if np.random.random() < self.gamma:
                    new_states[node] = 'R'
        
        self.states = new_states
        self.time += 1
        self._record_state()
    
    def run_epidemic(self, max_steps: int = 1000) -> Dict:
        while self.history['I'][-1] > 0 and self.time < max_steps:
            self.step()
        
        return {
            'final_size': self.history['R'][-1],
            'peak_infected': max(self.history['I']),
            'duration': self.time,
            'attack_rate': self.history['R'][-1] / self.N,
            'history': self.history
        }


class InterventionEngine(SIREngine):
    
    def __init__(self, graph: nx.Graph, beta: float, gamma: float):
        super().__init__(graph, beta, gamma)
        self.vaccinated = set()
    
    def reset(self, initial_infected: int = 1):
        super().reset(initial_infected)
        self.vaccinated = set()
    
    def vaccinate_random(self, coverage: float) -> int:
        n_vaccinate = int(self.N * coverage)
        susceptible = [n for n in self.G.nodes() if self.states[n] == 'S']
        
        if n_vaccinate > len(susceptible):
            n_vaccinate = len(susceptible)
        
        vaccinated_nodes = np.random.choice(susceptible, size=n_vaccinate, replace=False)
        
        for node in vaccinated_nodes:
            self.states[node] = 'R'
            self.vaccinated.add(node)
        
        self._record_state()
        return len(vaccinated_nodes)
    
    def vaccinate_targeted(self, coverage: float, strategy: str = 'degree') -> int:
        susceptible = [n for n in self.G.nodes() if self.states[n] == 'S']
        
        if strategy == 'degree':
            node_importance = {n: self.G.degree(n) for n in susceptible}
        elif strategy == 'betweenness':
            bc = nx.betweenness_centrality(self.G)
            node_importance = {n: bc[n] for n in susceptible}
        elif strategy == 'closeness':
            cc = nx.closeness_centrality(self.G)
            node_importance = {n: cc[n] for n in susceptible}
        elif strategy == 'pagerank':
            pr = nx.pagerank(self.G)
            node_importance = {n: pr[n] for n in susceptible}
        else:
            node_importance = {n: self.G.degree(n) for n in susceptible}
        
        sorted_nodes = sorted(node_importance.items(), key=lambda x: x[1], reverse=True)
        n_vaccinate = int(self.N * coverage)
        
        if n_vaccinate > len(sorted_nodes):
            n_vaccinate = len(sorted_nodes)
        
        vaccinated_nodes = [node for node, _ in sorted_nodes[:n_vaccinate]]
        
        for node in vaccinated_nodes:
            self.states[node] = 'R'
            self.vaccinated.add(node)
        
        self._record_state()
        return len(vaccinated_nodes)
    
    def apply_social_distancing(self, reduction: float) -> float:
        original_beta = self.beta
        self.beta = original_beta * (1 - reduction)
        return self.beta
    
    def apply_treatment(self, improvement: float) -> float:
        original_gamma = self.gamma
        self.gamma = original_gamma * (1 + improvement)
        return self.gamma


def compare_vaccination_strategies(graph: nx.Graph, beta: float, gamma: float,
                                   coverage: float, n_runs: int = 50) -> Dict:
    
    results = {
        'no_vaccine': {'attack_rates': [], 'peak_infected': []},
        'random': {'attack_rates': [], 'peak_infected': []},
        'targeted': {'attack_rates': [], 'peak_infected': []}
    }
    
    for _ in range(n_runs):
        engine = InterventionEngine(graph, beta, gamma)
        engine.reset(initial_infected=3)
        outcome = engine.run_epidemic()
        results['no_vaccine']['attack_rates'].append(outcome['attack_rate'])
        results['no_vaccine']['peak_infected'].append(outcome['peak_infected'])
    
    for _ in range(n_runs):
        engine = InterventionEngine(graph, beta, gamma)
        engine.reset(initial_infected=3)
        engine.vaccinate_random(coverage)
        outcome = engine.run_epidemic()
        results['random']['attack_rates'].append(outcome['attack_rate'])
        results['random']['peak_infected'].append(outcome['peak_infected'])
    
    for _ in range(n_runs):
        engine = InterventionEngine(graph, beta, gamma)
        engine.reset(initial_infected=3)
        engine.vaccinate_targeted(coverage, strategy='degree')
        outcome = engine.run_epidemic()
        results['targeted']['attack_rates'].append(outcome['attack_rate'])
        results['targeted']['peak_infected'].append(outcome['peak_infected'])
    
    summary = {}
    for strategy in results:
        summary[strategy] = {
            'mean_attack_rate': np.mean(results[strategy]['attack_rates']),
            'std_attack_rate': np.std(results[strategy]['attack_rates']),
            'mean_peak': np.mean(results[strategy]['peak_infected']),
            'std_peak': np.std(results[strategy]['peak_infected'])
        }
    
    return {'raw': results, 'summary': summary}


def intervention_sweep(graph_generator: Callable, beta: float, gamma: float,
                      coverage_range: np.ndarray, n_runs: int = 30) -> Dict:
    
    results = {
        'coverage': [],
        'random_attack': [],
        'targeted_attack': [],
        'random_peak': [],
        'targeted_peak': []
    }
    
    for coverage in coverage_range:
        random_attacks = []
        targeted_attacks = []
        random_peaks = []
        targeted_peaks = []
        
        for _ in range(n_runs):
            graph = graph_generator()
            
            engine_random = InterventionEngine(graph, beta, gamma)
            engine_random.reset(initial_infected=3)
            engine_random.vaccinate_random(coverage)
            outcome_random = engine_random.run_epidemic()
            random_attacks.append(outcome_random['attack_rate'])
            random_peaks.append(outcome_random['peak_infected'])
            
            engine_targeted = InterventionEngine(graph, beta, gamma)
            engine_targeted.reset(initial_infected=3)
            engine_targeted.vaccinate_targeted(coverage, strategy='degree')
            outcome_targeted = engine_targeted.run_epidemic()
            targeted_attacks.append(outcome_targeted['attack_rate'])
            targeted_peaks.append(outcome_targeted['peak_infected'])
        
        results['coverage'].append(coverage)
        results['random_attack'].append(np.mean(random_attacks))
        results['targeted_attack'].append(np.mean(targeted_attacks))
        results['random_peak'].append(np.mean(random_peaks))
        results['targeted_peak'].append(np.mean(targeted_peaks))
    
    return results


def run_intervention_scenarios(graph: nx.Graph, beta: float, gamma: float) -> Dict:
    
    scenarios = {}
    
    baseline = SIREngine(graph, beta, gamma)
    baseline.reset(initial_infected=3)
    scenarios['baseline'] = baseline.run_epidemic()
    
    engine = InterventionEngine(graph, beta, gamma)
    engine.reset(initial_infected=3)
    engine.vaccinate_random(0.2)
    scenarios['vaccine_20pct_random'] = engine.run_epidemic()
    
    engine = InterventionEngine(graph, beta, gamma)
    engine.reset(initial_infected=3)
    engine.vaccinate_targeted(0.2, strategy='degree')
    scenarios['vaccine_20pct_targeted'] = engine.run_epidemic()
    
    engine = InterventionEngine(graph, beta, gamma)
    engine.reset(initial_infected=3)
    engine.apply_social_distancing(0.5)
    scenarios['social_distancing_50pct'] = engine.run_epidemic()
    
    engine = InterventionEngine(graph, beta, gamma)
    engine.reset(initial_infected=3)
    engine.apply_treatment(0.5)
    scenarios['treatment_50pct_faster'] = engine.run_epidemic()
    
    engine = InterventionEngine(graph, beta, gamma)
    engine.reset(initial_infected=3)
    engine.vaccinate_targeted(0.2, strategy='degree')
    engine.apply_social_distancing(0.3)
    scenarios['combined_vaccine_distancing'] = engine.run_epidemic()
    
    return scenarios


if __name__ == '__main__':
    
    G = nx.watts_strogatz_graph(100, 6, 0.3)
    beta, gamma = 0.3, 0.1
    
    print("=== Basic SIR Simulation ===")
    engine = SIREngine(G, beta, gamma)
    engine.reset(initial_infected=3)
    result = engine.run_epidemic()
    print(f"Attack Rate: {result['attack_rate']:.2%}")
    print(f"Peak Infected: {result['peak_infected']}")
    print(f"Duration: {result['duration']} steps")
    
    print("\n=== Vaccination Comparison ===")
    comparison = compare_vaccination_strategies(G, beta, gamma, coverage=0.2, n_runs=50)
    for strategy, stats in comparison['summary'].items():
        print(f"\n{strategy.upper()}:")
        print(f"  Mean Attack Rate: {stats['mean_attack_rate']:.2%} ± {stats['std_attack_rate']:.2%}")
        print(f"  Mean Peak: {stats['mean_peak']:.1f} ± {stats['std_peak']:.1f}")
    
    print("\n=== Intervention Scenarios ===")
    scenarios = run_intervention_scenarios(G, beta, gamma)
    for name, result in scenarios.items():
        print(f"\n{name}:")
        print(f"  Attack Rate: {result['attack_rate']:.2%}")
        print(f"  Peak Infected: {result['peak_infected']}")
