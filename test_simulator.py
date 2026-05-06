"""
Test Script for SIR Epidemic Simulator
Verifies all core functionality works correctly
"""

import sys
import traceback

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        import networkx as nx
        import numpy as np
        import matplotlib.pyplot as plt
        import tkinter as tk
        print("✓ All required modules imported successfully")
        return True
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        print("Run: pip install -r requirements.txt")
        return False

def test_sir_model():
    """Test basic SIR model functionality"""
    print("\nTesting SIR Model...")
    try:
        import networkx as nx
        import numpy as np
        
        # Import from main module
        sys.path.insert(0, '.')
        from sir_epidemic_simulator import SIRModel
        
        # Create small test network
        graph = nx.erdos_renyi_graph(20, 0.3)
        
        # Create model
        model = SIRModel(graph, beta=0.3, gamma=0.1, initial_infected=2)
        
        # Run a few steps
        for _ in range(10):
            model.step()
        
        # Check that history is being tracked
        assert len(model.history['time']) > 1, "History not tracking"
        assert model.time == 10, "Time step counter not working"
        
        print("✓ SIR Model working correctly")
        return True
    except Exception as e:
        print(f"✗ SIR Model test failed: {e}")
        traceback.print_exc()
        return False

def test_network_generation():
    """Test network generation"""
    print("\nTesting network generation...")
    try:
        import networkx as nx
        
        # Test different network types
        networks = {
            'Erdős-Rényi': nx.erdos_renyi_graph(30, 0.1),
            'Small World': nx.watts_strogatz_graph(30, 4, 0.3),
            'Scale-Free': nx.barabasi_albert_graph(30, 2),
        }
        
        for name, graph in networks.items():
            assert len(graph.nodes()) > 0, f"{name} network has no nodes"
            assert len(graph.edges()) > 0, f"{name} network has no edges"
        
        print("✓ Network generation working correctly")
        return True
    except Exception as e:
        print(f"✗ Network generation test failed: {e}")
        traceback.print_exc()
        return False

def test_monte_carlo():
    """Test Monte Carlo analyzer"""
    print("\nTesting Monte Carlo analyzer...")
    try:
        import networkx as nx
        import numpy as np
        
        sys.path.insert(0, '.')
        from sir_epidemic_simulator import MonteCarloAnalyzer, SIRModel
        
        # Create simple network generator
        def network_gen():
            return nx.erdos_renyi_graph(20, 0.2)
        
        # Create analyzer with minimal simulations
        analyzer = MonteCarloAnalyzer(network_gen, n_simulations=3)
        
        # Run small parameter sweep
        beta_range = np.linspace(0.1, 0.3, 3)
        gamma_range = np.linspace(0.1, 0.3, 3)
        
        results = analyzer.run_parameter_sweep(beta_range, gamma_range)
        
        # Check results structure
        assert 'beta' in results, "Missing beta in results"
        assert 'gamma' in results, "Missing gamma in results"
        assert 'attack_rate' in results, "Missing attack_rate in results"
        assert len(results['beta']) == 9, "Wrong number of results"
        
        print("✓ Monte Carlo analyzer working correctly")
        return True
    except Exception as e:
        print(f"✗ Monte Carlo test failed: {e}")
        traceback.print_exc()
        return False

def test_visualization():
    """Test visualization functions"""
    print("\nTesting visualization...")
    try:
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend
        import matplotlib.pyplot as plt
        
        sys.path.insert(0, '.')
        from sir_epidemic_simulator import EpidemicVisualizer
        
        # Create dummy history data
        history = {
            'time': list(range(20)),
            'S': [100 - i*3 for i in range(20)],
            'I': [i*2 if i < 10 else 20-i*2 for i in range(20)],
            'R': [i for i in range(20)]
        }
        
        # Test SIR curve plotting
        fig = EpidemicVisualizer.plot_sir_curves(history)
        assert fig is not None, "Failed to create plot"
        plt.close(fig)
        
        print("✓ Visualization working correctly")
        return True
    except Exception as e:
        print(f"✗ Visualization test failed: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Run all tests and report results"""
    print("="*60)
    print("SIR EPIDEMIC SIMULATOR - TEST SUITE")
    print("="*60)
    
    tests = [
        ("Import Test", test_imports),
        ("SIR Model Test", test_sir_model),
        ("Network Generation Test", test_network_generation),
        ("Monte Carlo Test", test_monte_carlo),
        ("Visualization Test", test_visualization),
    ]
    
    results = []
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"\n✗ {name} crashed: {e}")
            traceback.print_exc()
            results.append((name, False))
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "PASS" if result else "FAIL"
        symbol = "✓" if result else "✗"
        print(f"{symbol} {name}: {status}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED! The simulator is ready to use.")
        print("\nNext steps:")
        print("1. Run the simulator: python sir_epidemic_simulator.py")
        print("2. Or build executable: python build_executable.py")
    else:
        print("\n⚠ Some tests failed. Please check the errors above.")
        print("Make sure all dependencies are installed:")
        print("  pip install -r requirements.txt")
    
    print("="*60)
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
