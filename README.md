# 🐜 Ant Colony Optimization for Travelling Salesman Problem (TSP)

This project implements the **Travelling Salesman Problem (TSP)** using **Ant Colony Optimization (ACO)** on real-world city graph data. It includes functionality to construct and visualize graphs of cities from any country and apply ACO to find the optimal tour.

## 📂 Project Structure

- `ant_colony_optimizer.py`: Contains the ACO algorithm for solving TSP and a hypertuning function to find the best hyperparameters.
- `graph_utils.py`: Contains utilities for:
  - Extracting city data from OpenStreetMap.
  - Building and saving graphs of cities.
  - Converting graphs to adjacency matrices.
  - Visualizing optimal ACO routes.
- `requirements.txt`: Lists all necessary Python libraries.

## 🚀 Features

- TSP solved using Ant Colony Optimization.
- City graph generated using geolocation data (OpenStreetMap & Overpass API).
- Graph visualization with city-to-city distances.
- Support for hyperparameter tuning of the ACO algorithm.
- Modular design: use your own graph or real-world city data.

## 🧪 Installation

Install all dependencies using pip:

```bash
pip install -r requirements.txt
```

## 📷 Example
![image](https://github.com/user-attachments/assets/2df7aeab-c3e8-45ad-9d06-e3dff40fe86e)
