import networkx as nx

def generate_network(network_type, n=500, m=2, p=0.01):
    if network_type == 'BA':
        return nx.barabasi_albert_graph(n, m)
    elif network_type == 'ER':
        return nx.erdos_renyi_graph(n, p)
    else:
        raise ValueError("Type error")

def get_hubs(G, top_n=10):
    degrees = dict(G.degree())
    return sorted(degrees, key=degrees.get, reverse=True)[:top_n]
