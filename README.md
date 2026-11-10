#  Agent-Based Epidemic Simulation on Networks

##  Project Overview

This project investigates the dynamics of infectious disease spread using the **SIR (Susceptible–Infected–Recovered)** model combined with **network science** principles.

The simulation explores how different social network structures influence epidemic behavior, specifically comparing:

- Erdős–Rényi (ER) Networks
- Barabási–Albert (BA) Scale-Free Networks

The primary objective is to evaluate the effectiveness of:

-  Targeted Hub Vaccination
vs.
-  Random Vaccination

---

#  Core Objectives

- Simulate epidemic spreading on complex networks
- Analyze how topology affects infection dynamics
- Compare vaccination strategies under limited resources
- Produce statistical and visual evidence through simulations

---

#  Main Challenges and Logic

##  Network Heterogeneity

Real-world social networks are not perfectly random.  
Many contain highly connected nodes (hubs) that act as super-spreaders.

This project focuses on the vulnerability of Scale-Free (BA) networks and demonstrates how removing or vaccinating hubs can dramatically reduce epidemic spread.

---

##  Resource Optimization

With only 20% vaccine coverage, random vaccination often fails to achieve herd immunity.

To solve this problem, the project implements a targeted vaccination strategy that identifies high-degree nodes.

---

##  Cross-Module Integration

Ensuring seamless communication between:
- network generation
- simulation engine
- analysis tools

---

# ️ Key Design Decisions

##  Modular Architecture

- networks.py → graph generation
- simulation.py → SIR model

---

##  Monte Carlo Validation

100+ simulations per experiment for statistical reliability.

---

##  Visualization

Real-time epidemic visualization included.

---

#  File Structure

├── img/
│   │   1_network_comparison.png
│   │   2_hub_identification.png
│   │   3_baseline_outbreak.png
│   │   4_vaccination_comparison.png
│   └── 5_single_epidemic_scenarios.png
│   main_analysis.py
│   monte_carlo.py
│   networks.py
│   quick_test.py
│   simulation.py
│   visualization.py
└── README.md

---

# How to Run

## Install
pip install -r requirements.txt

## Full analysis
python main_analysis.py

## Visualization
python visualization.py

---

#  Key Findings

- BA networks: vaccinating top 20% hubs → ~90% → <15% infection
- Random vaccination is much less effective
- Network structure is critical for epidemic control
