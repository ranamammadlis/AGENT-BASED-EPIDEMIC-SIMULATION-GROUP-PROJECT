# To run this visualization, ensure that 'networks.py' and 'simulation.py' 
# are in the same directory.


import matplotlib.pyplot as plt
import matplotlib.animation as animation
import networkx as nx

from networks import generate_network 
from simulation import SIRSimulation

class EpidemicVisualizer:
    def __init__(self, G, simulation):
        self.G = G
        self.sim = simulation
        self.pos = nx.spring_layout(G, seed=42)
        self.fig, self.ax = plt.subplots(figsize=(10, 7))
        self.color_map = {'S': '#3498db', 'I': '#e74c3c', 'R': '#95a5a6'}

    def update(self, frame):
        self.ax.clear()
        
        if frame > 0:
            self.sim.step()
            
        colors = [self.color_map[self.sim.states[node]] for node in self.G.nodes()]
        
        nx.draw(self.G, self.pos, node_color=colors, with_labels=False, 
                node_size=70, ax=self.ax, edge_color='#bdc3c7', alpha=0.7)
        
        self.ax.set_title(f"Epidemic Simulation: Day {frame}", fontsize=14)
        self.ax.text(0.5, -0.05, "Blue: Healthy | Red: Infected | Gray: Recovered", 
                     transform=self.ax.transAxes, ha='center')

    def run(self):
        self.ani = animation.FuncAnimation(
            self.fig, self.update, frames=50, interval=500, repeat=False
        )
        plt.show()

if __name__ == "__main__":
    network = generate_network('BA', n=100, m=2) 
    
    from simulation import InterventionSimulation
    
    simulation = InterventionSimulation(network, beta=0.3, gamma=0.1)
    simulation.reset(initial_infected=3)
    
    simulation.vaccinate_targeted(coverage=0.2) #comment this if you want to test it without coverage
    
    visualizer = EpidemicVisualizer(network, simulation)
    visualizer.run()
