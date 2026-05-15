import numpy as np
from networks import generate_network, get_hubs

class SIRSimulation:
    
    def __init__(self, graph, beta=0.3, gamma=0.1):
        self.G = graph
        self.beta = beta
        self.gamma = gamma
        self.N = len(graph.nodes())
        self.reset()
    
    def reset(self, initial_infected=5):
        self.states = {node: 'S' for node in self.G.nodes()}
        initial_nodes = np.random.choice(list(self.G.nodes()), 
                                         size=min(initial_infected, self.N), 
                                         replace=False)
        for node in initial_nodes:
            self.states[node] = 'I'
        
        self.time = 0
        self.history = {'S': [], 'I': [], 'R': [], 't': []}
        self.record()
    
    def record(self):
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
        self.record()
    
    def run_until_end(self, max_steps=500):
        while self.history['I'][-1] > 0 and self.time < max_steps:
            self.step()
        
        return {
            'final_size': self.history['R'][-1],
            'peak_infected': max(self.history['I']),
            'duration': self.time,
            'attack_rate': self.history['R'][-1] / self.N
        }


class InterventionSimulation(SIRSimulation):
    
    def vaccinate_random(self, coverage):
        n_vaccinate = int(self.N * coverage)
        susceptible = [n for n in self.G.nodes() if self.states[n] == 'S']
        
        if n_vaccinate > len(susceptible):
            n_vaccinate = len(susceptible)
        
        vaccinated = np.random.choice(susceptible, size=n_vaccinate, replace=False)
        
        for node in vaccinated:
            self.states[node] = 'R'
        
        self.record()
        return len(vaccinated)
    
    def vaccinate_targeted(self, coverage):
        n_vaccinate = int(self.N * coverage)
        hubs = get_hubs(self.G, top_n=n_vaccinate)
        vaccinated = [n for n in hubs if self.states[n] == 'S']
        
        for node in vaccinated:
            self.states[node] = 'R'
        
        self.record()
        return len(vaccinated)


def run_baseline(network_type='BA', n_runs=100):
    results = []
    
    for _ in range(n_runs):
        G = generate_network(network_type, n=500, m=2, p=0.008)
        sim = SIRSimulation(G, beta=0.3, gamma=0.1)
        sim.reset(initial_infected=5)
        outcome = sim.run_until_end()
        results.append(outcome['attack_rate'])
    
    return {
        'mean': np.mean(results),
        'std': np.std(results),
        'data': results
    }


def compare_strategies(network_type='BA', coverage=0.1, n_runs=100):
    random_results = []
    targeted_results = []
    
    for _ in range(n_runs):
        G = generate_network(network_type, n=500, m=2, p=0.008)
        
        sim_random = InterventionSimulation(G, beta=0.3, gamma=0.1)
        sim_random.reset(initial_infected=5)
        sim_random.vaccinate_random(coverage)
        outcome_random = sim_random.run_until_end()
        random_results.append(outcome_random['attack_rate'])
        
        sim_targeted = InterventionSimulation(G, beta=0.3, gamma=0.1)
        sim_targeted.reset(initial_infected=5)
        sim_targeted.vaccinate_targeted(coverage)
        outcome_targeted = sim_targeted.run_until_end()
        targeted_results.append(outcome_targeted['attack_rate'])
    
    return {
        'random': {'mean': np.mean(random_results), 'std': np.std(random_results)},
        'targeted': {'mean': np.mean(targeted_results), 'std': np.std(targeted_results)}
    }
