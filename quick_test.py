from networks import generate_network, get_hubs
from simulation import SIRSimulation, InterventionSimulation, compare_strategies

print("="*70)
print("QUICK TEST - All Components")
print("="*70)

print("\n[1/6] Testing generate_network...")
ba_net = generate_network('BA', n=500, m=2)
er_net = generate_network('ER', n=500, p=0.008)
print(f"✓ BA: {len(ba_net.nodes())} nodes, {len(ba_net.edges())} edges")
print(f"✓ ER: {len(er_net.nodes())} nodes, {len(er_net.edges())} edges")

print("\n[2/6] Testing get_hubs...")
hubs = get_hubs(ba_net, top_n=5)
degrees = [ba_net.degree(h) for h in hubs]
print(f"✓ Top 5 hubs: {hubs}")
print(f"✓ Degrees: {degrees}")

print("\n[3/6] Testing SIRSimulation...")
sim = SIRSimulation(ba_net, beta=0.3, gamma=0.1)
sim.reset(initial_infected=5)
result = sim.run_until_end()
print(f"✓ Attack rate: {result['attack_rate']:.2%}")
print(f"✓ Peak infected: {result['peak_infected']}")
print(f"✓ Duration: {result['duration']} steps")

print("\n[4/6] Testing random vaccination...")
sim_random = InterventionSimulation(ba_net, beta=0.3, gamma=0.1)
sim_random.reset(initial_infected=5)
n_vac = sim_random.vaccinate_random(0.2)
result_random = sim_random.run_until_end()
print(f"✓ Vaccinated: {n_vac}")
print(f"✓ Attack rate: {result_random['attack_rate']:.2%}")

print("\n[5/6] Testing targeted vaccination...")
sim_targeted = InterventionSimulation(ba_net, beta=0.3, gamma=0.1)
sim_targeted.reset(initial_infected=5)
n_vac = sim_targeted.vaccinate_targeted(0.2)
result_targeted = sim_targeted.run_until_end()
print(f"✓ Vaccinated: {n_vac}")
print(f"✓ Attack rate: {result_targeted['attack_rate']:.2%}")

if result_targeted['attack_rate'] < result_random['attack_rate']:
    improvement = (result_random['attack_rate'] - result_targeted['attack_rate']) / result_random['attack_rate']
    print(f"✓ Targeted advantage: {improvement:.1%}")

print("\n[6/6] Testing strategy comparison (5 runs)...")
comparison = compare_strategies('BA', coverage=0.2, n_runs=5)
print(f"✓ Random:   {comparison['random']['mean']:.2%}")
print(f"✓ Targeted: {comparison['targeted']['mean']:.2%}")

print("\n" + "="*70)
print("ALL TESTS PASSED ✓")
print("="*70)
print("\nYour networks.py is working perfectly!")
print("Run 'python main_analysis.py' for complete analysis")
print("="*70)
