from graph_utils import *
from ant_colony_optimizer import *

if __name__=="__main__":
    path = "data/India_sm.pkl"
    country = "India"
    if path == None :
        country = str(input("Enter the name of the Country : "))
        city_names = get_cities(country)
        city_graph = create_graph(city_names,country)
        path = f"data/{country}_sm.pkl"
    
    city_df , adj_matrix = graph_to_adjacency_matrix(path)

    # Code snipppet for tuning aco params
    # alphas = [1.0, 2.0, 3.0]
    # betas = [1.0, 2.0 , 3.0]
    # evaporations = [0.5, 0.7]
    # n_ants = [50, 100, 150, 200]
    # best_path , best_distance , best_config = hypertune_aco_tsp(adj_matrix,alphas,betas,evaporations,n_ants)

    # After tuning I got the best params as alpha=2.0, beta=3.0, evaporation=0.7, n_ants=100
    best_config = [2.0, 3.0, 0.7, 100]
    best_path , best_length = aco_tsp(adj_matrix,alpha=best_config[0], beta=best_config[1],
                                      evaporation=best_config[2], n_ants=best_config[3], n_iterations=200)
    
    best_route_vizualizer(adj_matrix,city_df,best_path,path,country)