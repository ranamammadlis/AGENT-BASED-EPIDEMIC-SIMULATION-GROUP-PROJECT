# SIR Epidemic Simulator - Complete User Guide

## Table of Contents
1. [Getting Started](#getting-started)
2. [Understanding the SIR Model](#understanding-the-sir-model)
3. [Interface Overview](#interface-overview)
4. [Detailed Tutorials](#detailed-tutorials)
5. [Interpretation Guide](#interpretation-guide)
6. [Advanced Features](#advanced-features)
7. [Troubleshooting](#troubleshooting)

---

## Getting Started

### Installation & First Run

**Method 1: Using Python (For Developers/Researchers)**
```bash
# 1. Install Python from python.org (3.8 or higher)
# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the simulator
python sir_epidemic_simulator.py
```

**Method 2: Using Executable (For Everyone)**
```bash
# 1. Build the executable
python build_executable.py

# 2. Find and run the .exe file
# Located in: dist/SIR_Epidemic_Simulator.exe

# 3. Double-click to run!
```

### First Simulation in 60 Seconds

1. **Launch** the application
2. **Go to "Single Simulation" tab**
3. **Keep default settings**:
   - Network Type: Small World
   - Network Size: 100
   - β (Beta): 0.30
   - γ (Gamma): 0.10
   - R₀: 3.00 (shown in blue/red)
4. **Click "Run Simulation"**
5. **Watch the results!**
   - SIR curves show disease progression
   - Statistics show outbreak size
   - R₀ > 1 means epidemic occurred

---

## Understanding the SIR Model

### The Three States

**S - Susceptible** 🔵
- Individuals who can catch the disease
- Healthy but not immune
- Decrease as people get infected

**I - Infected** 🔴
- Individuals who have the disease
- Can spread to susceptible neighbors
- Recover over time

**R - Recovered** 🟢
- Individuals who had the disease and recovered
- Now immune (cannot be infected again)
- Removed from transmission chain

### Key Parameters Explained

#### β (Beta) - Infection Rate
- **What it is**: Probability of transmission per contact
- **Range**: 0.0 to 1.0
- **Examples**:
  - β = 0.1: Low transmission (common cold)
  - β = 0.3: Moderate transmission (flu)
  - β = 0.6: High transmission (measles)
- **Real world factors**:
  - Contact patterns (handshakes, proximity)
  - Disease characteristics (airborne vs contact)
  - Interventions (masks, distancing)

#### γ (Gamma) - Recovery Rate
- **What it is**: Probability of recovery per time step
- **Range**: 0.0 to 1.0
- **Examples**:
  - γ = 0.05: Slow recovery (20 days average)
  - γ = 0.1: Moderate recovery (10 days average)
  - γ = 0.2: Fast recovery (5 days average)
- **Interpretation**: 1/γ ≈ average infectious period

#### R₀ - Basic Reproduction Number
- **Formula**: R₀ = β / γ
- **Meaning**: Average number of people one infected person infects
- **Critical threshold**: R₀ = 1
  - R₀ < 1: Disease dies out 🟢
  - R₀ = 1: Endemic equilibrium
  - R₀ > 1: Epidemic spreads 🔴

**Examples**:
- Seasonal flu: R₀ ≈ 1.3
- COVID-19 (original): R₀ ≈ 2.5-3.5
- Measles: R₀ ≈ 12-18

### Network Types and Real-World Analogies

#### Erdős-Rényi Random
- **Description**: Every pair of nodes has equal probability of connection
- **Real world**: Not realistic for disease spread
- **Use case**: Theoretical baseline

#### Small World Network (Default)
- **Description**: High clustering, short paths between any two nodes
- **Real world**: Social networks, realistic contact patterns
- **Characteristics**: 
  - Most people have similar number of contacts
  - "Six degrees of separation" phenomenon
- **Use case**: General disease modeling

#### Scale-Free Network
- **Description**: Few highly connected "hubs", many low-connectivity nodes
- **Real world**: 
  - Airports (few major hubs)
  - Social media (influencers)
  - Sexual contact networks
- **Characteristics**:
  - Very vulnerable to targeted hub removal
  - Can have large outbreaks even with low R₀
- **Use case**: Modeling superspreader events

#### Regular Grid
- **Description**: Each node connected to immediate neighbors
- **Real world**: Geographic spread, household transmission
- **Characteristics**: 
  - Slow, spatial spread
  - No long-distance jumps
- **Use case**: Localized outbreaks

---

## Interface Overview

### Tab 1: Single Simulation

**Purpose**: Run one simulation with specific parameters

**Controls**:
```
Network Type     [Dropdown]     Choose network structure
Network Size     [Spinner]      Number of individuals (10-500)
β (Infection)    [Slider]       Transmission probability (0-1)
γ (Recovery)     [Slider]       Recovery probability (0-1)
R₀              [Display]      Auto-calculated, color-coded
Initial Infected [Spinner]      Starting infections (1-50)
```

**Outputs**:
- SIR curves plot (S, I, R over time)
- Statistics panel:
  - Final recovered
  - Peak infected
  - Outbreak duration
  - Attack rate (% infected)
  - Network properties

### Tab 2: Monte Carlo Analysis

**Purpose**: Explore parameter space systematically

**Controls**:
```
Simulations/point  [Spinner]   Replications per (β,γ) pair
β range           [Min-Max]   Beta values to test
γ range           [Min-Max]   Gamma values to test
Grid Resolution   [Spinner]   Number of points per axis
Network Type      [Dropdown]  Network structure
Network Size      [Spinner]   Population size
```

**Outputs**:
- Phase Diagram 1: Attack Rate heatmap
- Phase Diagram 2: Peak Infected heatmap
- Black contour line: R₀ = 1 (epidemic threshold)
- Progress bar and status updates

### Tab 3: Network Animation

**Purpose**: Visualize disease spreading through network

**Controls**:
```
Network Size        [Spinner]    Nodes (10-100, smaller is faster)
Network Type        [Dropdown]   Network structure
β                  [Entry]      Infection rate
γ                  [Entry]      Recovery rate
Animation Speed     [Spinner]    Milliseconds per frame
```

**Outputs**:
- Opens new window with:
  - Left panel: Network with colored nodes
  - Right panel: Real-time SIR curves
- Animation stops when no infected remain

### Tab 4: Results & Export

**Purpose**: Save and export your work

**Features**:
- Scrollable results log (all simulations)
- Save Current Plot (PNG/PDF)
- Export Results as JSON (for further analysis)
- Generate Report (comprehensive text file)

---

## Detailed Tutorials

### Tutorial 1: Basic Epidemic Simulation

**Goal**: See how a disease spreads with moderate transmission

**Steps**:
1. Open "Single Simulation" tab
2. Settings:
   - Network: Small World
   - Size: 100
   - β = 0.3
   - γ = 0.1
   - Initial infected = 3
3. Note R₀ = 3.0 (red, epidemic will occur)
4. Click "Run Simulation"

**What to observe**:
- Susceptibles (blue) decrease rapidly at first
- Infected (red) peaks around time step 10-15
- Recovered (green) levels off as outbreak ends
- Attack rate ~80-95% (most people get infected)

**Try varying**:
- Increase β → faster, larger outbreak
- Increase γ → slower, smaller outbreak
- Change network type → different spread patterns

---

### Tutorial 2: Finding the Epidemic Threshold

**Goal**: Visualize where R₀ = 1 separates epidemics from die-outs

**Steps**:
1. Open "Monte Carlo Analysis" tab
2. Settings:
   - Simulations per point: 50
   - β range: 0.05 to 0.5
   - γ range: 0.05 to 0.5
   - Grid resolution: 15
   - Network: Small World, Size 100
3. Click "Run Monte Carlo Analysis"
4. Wait 2-3 minutes (progress bar shows status)

**What to observe**:
- **Attack Rate Phase Diagram**:
  - Red region (top-left): High β, low γ → large outbreaks
  - Green region (bottom-right): Low β, high γ → small outbreaks
  - **Black line**: Critical boundary (R₀ = 1)
  - Above line: R₀ > 1, epidemics occur
  - Below line: R₀ < 1, disease dies out

- **Peak Infected Phase Diagram**:
  - Shows maximum simultaneous infections
  - Useful for healthcare capacity planning

**Interpretation**:
- Points near the black line are most sensitive to interventions
- Small changes in β or γ can flip from epidemic to die-out
- Real-world interventions move you down (reduce β) or right (increase γ)

**Try experimenting**:
- Different network types (Scale-Free shows different threshold)
- Higher resolution (20x20) for smoother diagrams
- More simulations (100) for less noise

---

### Tutorial 3: Modeling Intervention Strategies

**Goal**: Simulate real-world interventions like social distancing

**Scenario**: COVID-19-like disease
- Baseline: β = 0.35, γ = 0.1 (R₀ = 3.5)
- Network: Small World, Size 200

**Part A: No Intervention**
1. Single Simulation tab
2. β = 0.35, γ = 0.1
3. Run simulation
4. Note: Attack rate ~90%, peak ~60 infected

**Part B: Social Distancing (50% contact reduction)**
1. New simulation
2. β = 0.175 (half of 0.35)
3. γ = 0.1 (same)
4. Note: R₀ = 1.75 (still epidemic, but weaker)
5. Run simulation
6. Compare: Attack rate ~60%, peak ~30 infected

**Part C: Strong Intervention (70% reduction)**
1. New simulation
2. β = 0.105 (30% of baseline)
3. γ = 0.1
4. Note: R₀ = 1.05 (barely epidemic)
5. Run simulation
6. Compare: Attack rate ~20%, peak ~10 infected

**Part D: Intervention + Treatment (faster recovery)**
1. New simulation
2. β = 0.175 (50% contact reduction)
3. γ = 0.15 (50% faster recovery via treatment)
4. Note: R₀ = 1.17
5. Run simulation
6. Compare: Attack rate ~40%, peak ~20 infected

**Key lessons**:
- Modest interventions reduce but don't eliminate epidemics
- Combining interventions (reduce β AND increase γ) is powerful
- Getting R₀ < 1 stops the epidemic entirely
- Small changes near R₀ = 1 have huge effects

---

### Tutorial 4: Network Structure Matters

**Goal**: Compare disease spread on different network types

**Setup**: β = 0.3, γ = 0.1, Size = 100, Initial infected = 3

**Experiment 1: Small World**
1. Run simulation
2. Record: Attack rate, peak infected

**Experiment 2: Scale-Free**
1. Change network type to Scale-Free
2. Run simulation
3. Compare with Small World

**Experiment 3: Regular Grid**
1. Change to Regular Grid
2. Run simulation
3. Compare with previous

**Expected results**:
- **Small World**: Fast spread, high attack rate
- **Scale-Free**: Very fast initial spread (hits hubs), high attack rate
- **Regular Grid**: Slow spatial spread, moderate attack rate

**Explanation**:
- Scale-Free: Hubs get infected early, rapidly spread to many
- Small World: Short paths mean disease reaches everyone quickly
- Regular Grid: Only spreads to immediate neighbors, no jumps

**Real-world implications**:
- Airports act as hubs (scale-free pattern)
- Social distancing targets hub connections
- Travel restrictions convert networks to more grid-like

---

### Tutorial 5: Creating Publication-Quality Phase Diagrams

**Goal**: Generate professional plots for papers/presentations

**Steps**:
1. Monte Carlo Analysis tab
2. Settings for high quality:
   - Simulations per point: 100 (reduces noise)
   - β range: 0.0 to 0.6
   - γ range: 0.0 to 0.6
   - Grid resolution: 25 (smooth heatmap)
   - Network: Small World, Size 150
3. Run analysis (will take 5-10 minutes)
4. View both phase diagrams
5. Go to "Results & Export" tab
6. Click "Save Current Plot"
7. Choose PDF format for vector graphics
8. Save with descriptive name

**Tips for presentations**:
- Use Attack Rate diagram for policy audiences
- Use Peak Infected for healthcare capacity discussions
- Annotate the R₀ = 1 line as "epidemic threshold"
- Add arrows showing intervention effects

---

### Tutorial 6: Animation for Teaching

**Goal**: Create compelling visualization for classroom/video

**Settings for best animation**:
- Network Size: 25-30 (visible but not cluttered)
- Network Type: Small World (realistic)
- β = 0.4 (fast enough to see spread)
- γ = 0.08 (long enough to watch)
- Animation Speed: 300 ms (readable)

**Steps**:
1. Animation tab
2. Enter settings above
3. Click "Start Animation"
4. Watch disease spread from initial infected
5. Note synchronized SIR curves

**Teaching points to highlight**:
- Initial exponential growth of infected (red)
- Peak infection occurs when new infections = recoveries
- Depletion of susceptibles eventually ends outbreak
- Network clusters can delay spread

**For video/screen recording**:
- Use OBS Studio or similar to record
- Smaller network (20) records better
- Slower speed (500ms) easier to follow
- Pause and annotate key moments

---

## Interpretation Guide

### Reading SIR Curves

**Typical Epidemic Curve**:
```
|                    S (blue) starts high, drops
| S                 I (red) rises then falls
| \                R (green) rises to plateau
|  \      I
|   \    / \
|    \ /     \   R
|     X       ---/
|    / \     /
|   /   \   /
|  /     \ /
| /       X
+-------------------> Time
```

**Key points**:
1. **S and I crossover**: Peak of infected
2. **I returns to zero**: Outbreak ends
3. **Final R plateau**: Total infected over outbreak
4. **Steepness of I**: Speed of spread

**Variations**:
- **Flat I curve**: Low β or high γ, slow spread
- **Tall sharp I peak**: High β, low γ, explosive outbreak
- **R never rises much**: R₀ < 1, disease dies out quickly

### Reading Phase Diagrams

**Axes**:
- **X-axis (β)**: Left = low transmission, Right = high transmission
- **Y-axis (γ)**: Bottom = slow recovery, Top = fast recovery

**Colors**:
- **Dark red**: Large outbreaks (70-100% infected)
- **Orange**: Moderate outbreaks (30-70% infected)
- **Yellow**: Small outbreaks (10-30% infected)
- **Light green**: Minimal spread (<10% infected)

**The R₀ = 1 line**:
- **Above and right**: Safe zone (R₀ < 1)
- **Below and left**: Danger zone (R₀ > 1)
- **On the line**: Exactly R₀ = 1, critical

**Strategic interpretation**:
- To stop epidemic, must cross the black line
- Can do this by:
  - Moving right (increase γ): Treatment, faster isolation
  - Moving up (decrease β): Social distancing, masks, vaccines
  - Usually need both

### Understanding Attack Rates

**Attack Rate** = Final Recovered / Total Population

- **0-10%**: Minor outbreak, most avoided infection
- **10-30%**: Moderate outbreak, significant but limited
- **30-60%**: Major outbreak, healthcare system stressed
- **60-90%**: Severe epidemic, most population affected
- **90-100%**: Complete epidemic, nearly everyone infected

**Factors affecting attack rate**:
- Higher R₀ → higher attack rate
- Network structure (scale-free often has higher attack rates)
- Initial number infected (minimal effect)
- Population size (minimal effect for large populations)

### Peak Infected

**Why it matters**:
- Determines healthcare capacity needs
- ICU beds, ventilators, staff
- "Flatten the curve" means reducing peak

**Typical values** (for population of 100):
- **Peak < 10**: Manageable, low strain
- **Peak 10-30**: Moderate strain
- **Peak 30-60**: High strain, capacity concerns
- **Peak > 60**: Crisis, overwhelmed system

**Relationship to interventions**:
- "Flattening curve": Reduce peak, extend duration
- Total infected may be similar, but peak is lower
- Achieved by reducing β during epidemic

---

## Advanced Features

### Exporting Data for R/Python Analysis

**Export JSON**:
1. Complete simulations
2. Results & Export tab
3. "Export Results as JSON"
4. Save file

**JSON structure**:
```json
{
  "timestamp": "2024-01-15T10:30:00",
  "results": "text log of results",
  "monte_carlo_results": {
    "beta": [0.1, 0.2, ...],
    "gamma": [0.1, 0.15, ...],
    "attack_rate": [0.05, 0.12, ...],
    "peak_infected": [5, 12, ...],
    "R0": [1.0, 1.33, ...]
  }
}
```

**Loading in Python**:
```python
import json
import numpy as np
import pandas as pd

with open('results.json') as f:
    data = json.load(f)

mc = data['monte_carlo_results']
df = pd.DataFrame(mc)

# Further analysis
import matplotlib.pyplot as plt
plt.scatter(df['R0'], df['attack_rate'])
plt.xlabel('R₀')
plt.ylabel('Attack Rate')
plt.show()
```

### Batch Simulations

**Goal**: Run many simulations automatically

**Python script**:
```python
import networkx as nx
from sir_epidemic_simulator import SIRModel

# Parameter sweep
results = []
for beta in [0.1, 0.2, 0.3, 0.4]:
    for gamma in [0.05, 0.1, 0.15]:
        for _ in range(50):  # 50 replications
            graph = nx.watts_strogatz_graph(100, 6, 0.3)
            model = SIRModel(graph, beta, gamma)
            stats = model.run_until_stable()
            results.append({
                'beta': beta,
                'gamma': gamma,
                **stats
            })

import pandas as pd
df = pd.DataFrame(results)
df.to_csv('batch_results.csv', index=False)
```

### Custom Network Structures

**Import your own network**:
```python
import networkx as nx
from sir_epidemic_simulator import SIRModel

# Load network from file
graph = nx.read_edgelist('my_network.txt')

# Or create custom
graph = nx.Graph()
graph.add_edges_from([(0,1), (1,2), (2,3), ...])

# Run simulation
model = SIRModel(graph, beta=0.3, gamma=0.1)
stats = model.run_until_stable()
```

### Stochastic vs Mean-Field

**Current implementation**: Stochastic (individual-based)
- Each infection/recovery is random event
- Different outcomes each run
- More realistic, captures fluctuations

**Alternative (if needed)**: Mean-field differential equations
```python
import numpy as np
from scipy.integrate import odeint

def sir_ode(y, t, beta, gamma, N):
    S, I, R = y
    dS = -beta * S * I / N
    dI = beta * S * I / N - gamma * I
    dR = gamma * I
    return dS, dI, dR

# Solve
N = 1000
I0, R0 = 1, 0
S0 = N - I0 - R0
y0 = (S0, I0, R0)
t = np.linspace(0, 160, 160)
solution = odeint(sir_ode, y0, t, args=(0.3, 0.1, N))
```

---

## Troubleshooting

### Installation Issues

**Problem**: `pip install` fails

**Solutions**:
```bash
# Update pip first
python -m pip install --upgrade pip

# Install one at a time to identify problem
pip install networkx
pip install numpy
pip install matplotlib
pip install pyinstaller

# Use specific versions if needed
pip install networkx==3.0
```

**Problem**: tkinter not found

**Solutions**:
- **Windows**: Reinstall Python with tkinter option checked
- **Linux**: `sudo apt-get install python3-tk`
- **macOS**: Should be included with Python

### Runtime Issues

**Problem**: "ModuleNotFoundError" when running

**Solution**:
```bash
# Make sure you're in the right directory
cd path/to/sir_simulator
python sir_epidemic_simulator.py
```

**Problem**: GUI doesn't appear

**Solution**:
- Check if running in virtual environment
- Try: `python -m tkinter` to test tkinter
- Some remote desktop environments don't support GUIs

**Problem**: Simulation takes too long

**Solutions**:
- Reduce network size (< 100)
- Reduce Monte Carlo simulations (< 50)
- Reduce grid resolution (< 15)
- Use faster computer

### Build Issues

**Problem**: PyInstaller not found

**Solution**:
```bash
pip install pyinstaller
# Or use full path
python -m pip install pyinstaller
```

**Problem**: Build fails with import errors

**Solution**:
```bash
# Clear previous builds
rm -rf build dist *.spec

# Rebuild
pyinstaller --clean sir_epidemic_simulator.py
```

**Problem**: Executable won't run on other computers

**Solutions**:
- Make sure target computer has same OS
- Include Visual C++ redistributable (Windows)
- Check antivirus isn't blocking
- Try `--onefile` flag for single exe

### Simulation Issues

**Problem**: All results are the same

**Check**: Are you using the same random seed?
**Solution**: Each run uses random numbers, so results vary

**Problem**: Disease never spreads

**Check**: 
- Is β too low?
- Is γ too high?
- Is R₀ < 1?
**Solution**: Increase β or decrease γ

**Problem**: Everyone gets infected

**Check**: Is R₀ very high (> 3)?
**Solution**: This is expected for high R₀ in connected networks

### Performance Issues

**Problem**: Monte Carlo analysis crashes

**Solutions**:
- Reduce simulations per point (try 20)
- Reduce network size (try 50)
- Reduce grid resolution (try 10)
- Close other programs
- Check RAM usage

**Problem**: Animation is choppy

**Solutions**:
- Reduce network size (< 30)
- Increase animation interval (> 400ms)
- Close other programs
- Use simpler network (Regular Grid)

---

## Tips for Different Audiences

### For Students
- Start with animations to build intuition
- Use small networks (< 50) for faster results
- Try extreme parameters to see effects clearly
- Focus on R₀ concept first

### For Researchers
- Use Monte Carlo for systematic exploration
- Export JSON for statistical analysis
- Run multiple replicates (100+)
- Document all parameter choices
- Consider network robustness

### For Policy Makers
- Focus on intervention scenarios
- Use Attack Rate diagrams
- Show "with/without intervention" comparisons
- Emphasize Peak Infected for capacity
- Include confidence intervals (MC results)

### For Educators
- Use animations for engagement
- Interactive demos with students choosing parameters
- Compare to historical epidemics
- Discuss limitations of models
- Connect to real interventions

---

**Document Version**: 1.0
**Last Updated**: 2024
**For**: SIR Epidemic Simulator v1.0
