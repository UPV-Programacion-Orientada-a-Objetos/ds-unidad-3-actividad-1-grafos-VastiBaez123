import random

def generate_dummy_snap(filename="web-Google.txt", num_nodes=1000, num_edges=5000):
    with open(filename, "w") as f:
        f.write(f"# Directed graph (each unordered pair of nodes is saved once): {filename}\n")
        f.write(f"# Nodes: {num_nodes} Edges: {num_edges}\n")
        f.write("# FromNodeId\tToNodeId\n")
        for _ in range(num_edges):
            u = random.randint(0, num_nodes - 1)
            v = random.randint(0, num_nodes - 1)
            if u != v:
                f.write(f"{u}\t{v}\n")

if __name__ == "__main__":
    generate_dummy_snap("web-Google.txt", 5000, 20000)
    print("Generated dummy dataset 'web-Google.txt'")
