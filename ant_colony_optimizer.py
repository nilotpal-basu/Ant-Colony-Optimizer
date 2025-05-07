import numpy as np
import random
from itertools import product

def aco_tsp(adj_matrix, n_ants=100, n_iterations=100, alpha=1.5, beta=2.0, evaporation=0.7, Q=100):
    n_nodes = len(adj_matrix)
    pheromone = np.ones((n_nodes, n_nodes))
    best_length = float('inf')
    best_path = []

    distances = np.where(adj_matrix == 0, 100000, adj_matrix)

    def route_length(path):
        return sum(distances[path[i], path[i + 1]] for i in range(len(path) - 1)) + distances[path[-1], path[0]]

    for it in range(n_iterations):
        paths = []
        for _ in range(n_ants):
            unvisited = list(range(n_nodes))
            current = random.choice(unvisited)
            path = [current]
            unvisited.remove(current)

            while unvisited:
                probs = []
                for j in unvisited:
                    if distances[current][j] != np.inf:
                        tau = pheromone[current][j] ** alpha
                        eta = (1 / distances[current][j]) ** beta
                        probs.append(tau * eta)
                    else:
                        probs.append(0)
                probs = np.array(probs, dtype=np.float64)
                probs /= probs.sum()
                next_node = np.random.choice(unvisited, p=probs)


                path.append(next_node)
                unvisited.remove(next_node)
                current = next_node

            paths.append((path, route_length(path)))

        for path, length in paths:
            if length < best_length:
                best_length = length
                best_path = path

        pheromone *= (1 - evaporation)
        for path, length in paths:
            for i in range(len(path) - 1):
                pheromone[path[i]][path[i+1]] += Q / length
                pheromone[path[i+1]][path[i]] += Q / length
            pheromone[path[-1]][path[0]] += Q / length
            pheromone[path[0]][path[-1]] += Q / length

        print(f"Iteration {it+1}: Distance = {best_length:.2f}")

    best_path.append(best_path[0])
    return best_path, best_length

def hypertune_aco_tsp(adj_matrix, alphas, betas, evaporations, n_ants, Q=100, n_iterations=100):
    best_config = None
    best_distance = float('inf')
    best_path = None

    for alpha, beta, evap, n_ant in product(alphas, betas, evaporations, n_ants):
        print(f"\nTesting config: alpha={alpha}, beta={beta}, evaporation={evap}, ant_num={n_ant}")
        try:
            path, dist = aco_tsp(
                adj_matrix,
                n_ants=n_ant,
                n_iterations=n_iterations,
                alpha=alpha,
                beta=beta,
                evaporation=evap,
                Q=Q
            )
            print(f"  ➤ Final distance: {dist:.2f}")
            if dist < best_distance:
                best_distance = dist
                best_config = (alpha, beta, evap, Q)
                best_path = path
        except Exception as e:
            print(f"  ✗ Failed: {e}")

    print("\nBest Configuration:")
    print(f"  alpha={best_config[0]}, beta={best_config[1]}, evaporation={best_config[2]}, n_ants={best_config[3]}")
    print(f"  Best Distance: {best_distance:.2f}")
    return best_path, best_distance, best_config
