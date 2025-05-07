import networkx as nx
import osmnx as ox
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import overpy
from geopy.distance import geodesic
import pickle

def get_cities(country="India",num_cities=100):
    # Create Overpass API object
    api = overpy.Overpass()

    # Query: fetch all cities (place=city) in country
    query = f"""
    [out:json][timeout:60];
    area["name"="{country}"]->.searchArea;
    (
    node["place"="city"](area.searchArea);
    );
    out body;
    """

    # Run the query
    result = api.query(query)

    # Extract city names
    city_names = [node.tags.get("name") for node in result.nodes]
    city_names_sm = city_names[:num_cities] # Taking only num_cities number of cities
    return city_names_sm

def create_graph(city_names,country):
    # Get coordinates for each city
    city_locations = {}
    for city in city_names:
        location = ox.geocode(city + f", {country}")
        city_locations[city] = location

    # Create a graph to connect cities 
    city_graph = nx.Graph()

    # Add nodes with positions
    for city, (lat, lon) in city_locations.items():
        city_graph.add_node(city, pos=(lon, lat))

    for city1 in city_names:
        distances = []
        for city2 in city_names:
            if city1 != city2:
                dist = geodesic(city_locations[city1], city_locations[city2]).km
                distances.append((city2, dist))
        # Add edges to all cities
        distances.sort(key=lambda x: x[1])
        for city2, dist in distances[:]:
            city_graph.add_edge(city1, city2, weight=dist)

    # Save Graph
    with open(f"data/{country}_sm.pkl", "wb") as f:
        pickle.dump(city_graph, f)

    return city_graph

def plot_graph(city_graph,country): # Plotting the graph
    pos = nx.get_node_attributes(city_graph, 'pos')
    plt.figure(figsize=(20, 20))
    nx.draw(city_graph, pos, with_labels=True, node_size=1000, node_color='lightblue', font_size=10)
    nx.draw_networkx_edge_labels(city_graph, pos, edge_labels={(u, v): f"{d['weight']:.0f} km" for u, v, d in city_graph.edges(data=True)})
    plt.title(f"Major {country} Cities and Connecting Roads (approximate)")
    plt.show()

# Load saved graph
def read_graph(path):
    with open(path, "rb") as f:
        G = pickle.load(f)
    return G

# Convert city to label (Label Encoder) 
def city_to_label(df,city):
    return (df[df['city']==city].index[0])

# Convert label to city (Label Decoder)
def label_to_city(df,label):
    return df.at[label,'city']

# Creating the adjacency list
def graph_to_adjacency_matrix(path):
    city_graph = read_graph(path) # Read graph
    cities = list(city_graph.nodes) # Read nodes/cities present in the graph
    num_cities = len(cities)
    city_df = pd.DataFrame(cities,columns=['city'])
    edge_list = [[u,v,d['weight']] for u,v,d in city_graph.edges(data=True)]

    dist_matrix = np.zeros((num_cities,num_cities))
    for u,v,d in edge_list:
        # Get labels for cities
        u_label = city_to_label(city_df,u) 
        v_label = city_to_label(city_df,v)

        # Add distances to the matrix
        dist_matrix[u_label][v_label] = dist_matrix[v_label][u_label] = d
    return city_df , dist_matrix

def best_route_vizualizer(adj_matrix,city_df,best_path,path,country="India"):
    new_graph = read_graph(path) # Read data from pre-exisiting graph
    new_graph.remove_edges_from(new_graph.edges()) # Remove existing edges
    route = []
    # Convert labels to city names
    for i in best_path:
        route.append(label_to_city(city_df,i))
    # Adding best route edges
    for i in range(len(best_path)-1):
        new_graph.add_edge(route[i], route[i+1], weight=adj_matrix[best_path[i]][best_path[i+1]])
    # Vizualizing the best path
    plot_graph(new_graph,country)
