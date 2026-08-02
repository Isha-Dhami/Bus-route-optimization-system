# Bus Route Optimization System

A web-based transit navigation application designed to optimize route selection for travelers. The system helps users find the most efficient paths between source and destination bus stops by calculating the shortest distance and estimated travel time.

## 🚀 Features
- **Interactive Interface:** Clean UI allowing users to dynamically select their source and destination stops.
- **Route Optimization:** Implements **Dijkstra's Algorithm** to compute the absolute shortest path and minimal travel time.
- **Regional Data Integration:** Modeled using real-world bus route datasets from Uttarakhand.
- **Team Collaboration:** Developed in a structured 3-member team environment focusing on modular component integration.

## 🛠️ Tech Stack
- **Frontend:** HTML5, CSS3, JavaScript
- **Backend/Logic:** Python (Graph algorithms and routing logic)

## 📌 How It Works
1. The backend models the bus network as a weighted graph where vertices are stops and edge weights represent distance/time.
2. The user inputs their starting location and destination via the web interface.
3. The system executes Dijkstra's algorithm on the graph model.
4. The optimal path, total distance, and estimated travel time are rendered instantly on screen.
