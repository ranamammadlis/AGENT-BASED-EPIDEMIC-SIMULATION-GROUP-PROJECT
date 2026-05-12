import numpy as np
from matplotlib.colors import Normalize
import matplotlib.pyplot as plt
import matplotlib.cm as cm

def monte_carlo_sim(Graph, sims, t, vacination = None, coverage=None):

    beta_values = np.linspace(0.01, 0.5, 25)
    gamma_values = np.linspace(0.01, 0.5, 25)
    avg_outbreak_size = np.zeros((len(beta_values), len(gamma_values)))
    r0 = np.zeros((len(beta_values), len(gamma_values)))

    for i, beta in enumerate(beta_values):
        for j, gamma in enumerate(gamma_values):
            ratios = []

            for sim in range(sims):
                model = InterventionEngine(Graph, beta=beta, gamma=gamma)
                model.reset(initial_infected=1)

                if vacination is not None:
                    if vacination == "random":
                        model.vaccinate_random(coverage=coverage)
                        result = model.run_epidemic(max_steps=t)

                    elif vacination == "targeted":
                        model.vaccinate_targeted(coverage=coverage, strategy='degree')
                        result = model.run_epidemic(max_steps=t)
                          
                else:
                    result= model.run_epidemic(max_steps=t)
            
                infected_per_population = (model.N - result["history"]["S"][-1])/model.N
                ratios.append(infected_per_population)

            avg_outbreak_size[i][j] = np.mean(ratios)
            r0[i][j] = beta/gamma
            
    return avg_outbreak_size, r0



N = 100
t = 50
sims = 100

figure, axes = plt.subplots(2,3, figsize=(20,10))
G_BA = generate_network("BA", n=N, m=2, p=0.02)
G_ER = generate_network("ER", n=N, m=2, p=0.03)

networks = {0 : ("Barabási–Albert model", G_BA), 1 : ("Erdős-Rényi model", G_ER )}

for i, network in networks.items():
    for j, vaccin in enumerate([None, "random", "targeted"]):
        test = monte_carlo_sim(network[1], sims=sims, t=t, vacination=vaccin, coverage=0.2)
        outbreak_sizes= test[0]

        R0 = test[1]
        theoretical_epidemic = R0 > 1

        axes[i, j].imshow(outbreak_sizes, origin="lower", extent=[0.01, 0.5, 0.01, 0.5], aspect='equal' )
        axes[i, j].set_title(f"{vaccin} vaccination on {network[0]}" if vaccin is not None else network[0])
        axes[i, j].set_xlabel("gamma")
        axes[i, j].contour(theoretical_epidemic, colors='red', extent=[0.01,0.5,0.01,0.5])

        if j == 0:
            axes[i, j].set_ylabel("beta")

figure.subplots_adjust(wspace=0.8, hspace=0.3)
normalizer = Normalize(0, 1)
im = cm.ScalarMappable(norm=normalizer)
figure.colorbar(im, label="Final outbreak size", ax=axes.ravel().tolist(), orientation='horizontal', fraction = 0.05)
plt.show()