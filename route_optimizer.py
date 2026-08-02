import csv
import heapq
import webbrowser
from math import radians, sin, cos, sqrt, atan2
from flask import Flask, render_template, jsonify, request

app = Flask(__name__, template_folder='../web', static_folder='../web')

class Graph:
    def __init__(self):
        self.edges = {}
        self.coordinates = self._load_coordinates()
    
    def _load_coordinates(self):
        return {
            # Kumaon Region
            'HALDWANI': (29.2186, 79.5276),
            'KATHGODAM': (29.2679, 79.5285),
            'BHIMTAL': (29.3444, 79.5633),
            'BHOWALI': (29.3869, 79.5075),
            'NAINITAL': (29.3919, 79.4545),
            'ALMORA': (29.5972, 79.6609),
            'RANIKHET': (29.6429, 79.4323),
            'KAUSANI': (29.8431, 79.6045),
            'BAGESHWAR': (29.8404, 79.7719),
            'PITHORAGARH': (29.5825, 80.2184),
            'MUKTESHWAR': (29.4729, 79.6479),
            
            # Garhwal Region
            'DEHRADUN': (30.3165, 78.0322),
            'MUSSOORIE': (30.4546, 78.0700),
            'RISHIKESH': (30.0869, 78.2676),
            'HARIDWAR': (29.9457, 78.1642),
            'UTTARKASHI': (30.7296, 78.4434),
            'SRINAGAR': (30.2224, 78.7834),
            'RUDRAPRAYAG': (30.2847, 78.9839),
            'KEDARNATH': (30.7346, 79.0669),
            'BADRINATH': (30.7446, 79.4933),
            
            # Other Important Towns
            'KOTDWAR': (29.7469, 78.5280),
            'RAMNAGAR': (29.3975, 79.1289),
            'RUDRAPUR': (28.9800, 79.4000),
            'TANAKPUR': (29.0753, 80.1119),
            'DHARCHULA': (29.8476, 80.5373),
            'BAIJNATH': (29.9194, 79.6167),
            'GARUR': (29.8694, 79.4869),
            'GWALDAM': (30.0186, 79.5728),
            'KARANPRAYAG': (30.2608, 79.2153),
            'NANDPRAYAG': (30.3300, 79.3333),
            'CHAMOLI': (30.4167, 79.3333),
            'PIPALKOTI': (30.4258, 79.4306),
            'MORADABAD': (28.8381, 78.7768),
            'KASHIPUR': (29.2136, 78.9569),
            'RAMNAGAR': (29.3975, 79.1289),  
            'ROORKEE': (29.8543, 77.8880),
            'NAJIBABAD': (29.6119, 78.3427),
            'KASHIPUR': (29.2136, 78.9569),
            'MORADABAD': (28.8381, 78.7768),
            'NAJIBABAD': (29.6119, 78.3427),
            'NAGAR': (30.1417, 78.2917),    
            'CHAMBA': (30.3566, 78.3984),   
            'DEVPRAYAG': (30.1460, 78.5987),
            'GWALDAM': (30.0186, 79.5728),   
            'BAIJNATH': (29.9194, 79.6167),  
            'ROORKEE': (29.8543, 77.8880),
            'NAJIBABAD': (29.6119, 78.3427),
            'KOTDWAR': (29.7469, 78.5280),
            'HARIDWAR': (29.9457, 78.1642),
            'PIPALKOTI': (30.4258, 79.4306),
            'MUKTESHWAR': (29.4729, 79.6479),
            'RAMGARH': (29.4500, 79.5500),  
        }

    def add_edge(self, from_node, to_node, distance, time):
        from_node = from_node.strip().upper()
        to_node = to_node.strip().upper()
        
        if from_node not in self.edges:
            self.edges[from_node] = []
        self.edges[from_node].append((to_node, distance, time))
        
        if to_node not in self.edges:
            self.edges[to_node] = []
        self.edges[to_node].append((from_node, distance, time))

    def dijkstra(self, start, end, optimize='distance'):
        start = start.strip().upper()
        end = end.strip().upper()
        
        distances = {node: float('inf') for node in self.edges}
        times = {node: float('inf') for node in self.edges}
        previous_nodes = {node: None for node in self.edges}
        distances[start] = 0
        times[start] = 0
        
        queue = [(0, start)]
        
        while queue:
            current_metric, current_node = heapq.heappop(queue)
            
            if current_node == end:
                break
                
            for neighbor, distance, time in self.edges.get(current_node, []):
                if optimize == 'distance':
                    new_metric = distances[current_node] + distance
                    if new_metric < distances[neighbor]:
                        distances[neighbor] = new_metric
                        times[neighbor] = times[current_node] + time
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(queue, (new_metric, neighbor))
                else:
                    new_metric = times[current_node] + time
                    if new_metric < times[neighbor]:
                        times[neighbor] = new_metric
                        distances[neighbor] = distances[current_node] + distance
                        previous_nodes[neighbor] = current_node
                        heapq.heappush(queue, (new_metric, neighbor))
        
        path = []
        current = end
        while current is not None:
            path.append(current)
            current = previous_nodes.get(current, None)
        path.reverse()
        
        if not path or path[0] != start:
            return [], 0, 0
        
        return path, distances[end], times[end]

def load_graph_from_csv(filename):
    graph = Graph()
    # Haldwani/Kathgodam Hub
    graph.add_edge('HALDWANI', 'KATHGODAM', 7, 0.25)  
    graph.add_edge('KATHGODAM', 'BHIMTAL', 12, 0.5)   
    graph.add_edge('BHIMTAL', 'BHOWALI', 8, 0.33)     
    graph.add_edge('BHOWALI', 'ALMORA', 28, 1.25)     
    graph.add_edge('BHOWALI', 'NAINITAL', 10, 0.5)    
   # Almora/Kausani Network
    graph.add_edge('ALMORA', 'KAUSANI', 52, 2.0)    
    graph.add_edge('KAUSANI', 'BAGESHWAR', 40, 1.5)   
    graph.add_edge('BAGESHWAR', 'PITHORAGARH', 90, 3.5) 
   # Nainital/Ranikhet Connections
    graph.add_edge('NAINITAL', 'RANIKHET', 60, 2.5)   
    graph.add_edge('ALMORA', 'RANIKHET', 50, 1.75)    
    graph.add_edge('KAUSANI', 'RANIKHET', 70, 2.75)   
   # Char Dham Routes
    graph.add_edge('RISHIKESH', 'DEVPRAYAG', 70, 2.5) 
    graph.add_edge('RUDRAPRAYAG', 'UKHIMATH', 40, 1.5) 
    graph.add_edge('BADRINATH', 'JOSHIMATH', 45, 1.75) 
   # Hill Stations
    graph.add_edge('MUSSOORIE', 'DHANAULTI', 25, 1.0) 
    graph.add_edge('UTTARKASHI', 'GANGOTRI', 100, 4.5) 
    graph.add_edge('RISHIKESH', 'NAGAR', 35, 1.5)        
    graph.add_edge('NAGAR', 'CHAMBA', 25, 1.25)         
    graph.add_edge('CHAMBA', 'DEVPRAYAG', 40, 2.5)        
    graph.add_edge('DEVPRAYAG', 'SRINAGAR', 35, 1.75)   
    graph.add_edge('SRINAGAR', 'RUDRAPRAYAG', 40, 2.0)  
    graph.add_edge('RUDRAPRAYAG', 'KARANPRAYAG', 60, 2.5) 
    graph.add_edge('KARANPRAYAG', 'GWALDAM', 60, 3.0)    
    graph.add_edge('GWALDAM', 'KAUSANI', 40, 2.5)        
    graph.add_edge('KAUSANI', 'ALMORA', 52, 2.0)       
    graph.add_edge('ALMORA', 'BHIMTAL', 65, 3.0)        
    graph.add_edge('BHIMTAL', 'KATHGODAM', 12, 0.5)     
    graph.add_edge('KATHGODAM', 'HALDWANI', 7, 0.25)    
    graph.add_edge('DEHRADUN', 'MORADABAD', 150, 4.0)  
    graph.add_edge('MORADABAD', 'KASHIPUR', 50, 1.25)   
    graph.add_edge('KASHIPUR', 'HALDWANI', 60, 2.0)    
    graph.add_edge('HALDWANI', 'KATHGODAM', 7, 0.25)
    graph.add_edge('KATHGODAM', 'BHIMTAL', 12, 0.5)
    graph.add_edge('BHIMTAL', 'BHOWALI', 8, 0.33)
    graph.add_edge('BHOWALI', 'ALMORA', 28, 1.25)
    graph.add_edge('ALMORA', 'KAUSANI', 52, 2.0)
    graph.add_edge('KAUSANI', 'GWALDAM', 40, 2.5)  
    graph.add_edge('GWALDAM', 'KARANPRAYAG', 60, 3.0)
    graph.add_edge('KARANPRAYAG', 'NANDPRAYAG', 20, 0.75)
    graph.add_edge('NANDPRAYAG', 'JOSHIMATH', 45, 2.0)
    graph.add_edge('JOSHIMATH', 'BADRINATH', 45, 1.75)
    graph.add_edge('DEHRADUN', 'RISHIKESH', 40, 1.5)
    graph.add_edge('RISHIKESH', 'DEVPRAYAG', 70, 2.5)
    graph.add_edge('DEVPRAYAG', 'SRINAGAR', 35, 1.75)
    graph.add_edge('SRINAGAR', 'RUDRAPRAYAG', 40, 2.0)
    graph.add_edge('RUDRAPRAYAG', 'KARANPRAYAG', 60, 2.5)
    graph.add_edge('KARANPRAYAG', 'JOSHIMATH', 45, 2.0)
    graph.add_edge('JOSHIMATH', 'BADRINATH', 45, 1.75)
    graph.add_edge('PITHORAGARH', 'DHARCHULA', 80, 3.5)
    graph.add_edge('DHARCHULA', 'TAWAGHAT', 15, 1.0)  
    graph.add_edge('BAGESHWAR', 'CHAUKORI', 35, 1.75)
    # Pithoragarh to Munsiyari (gateway to Milam Glacier)
    graph.add_edge('PITHORAGARH', 'MUNSIYARI', 120, 5.0)  
    graph.add_edge('ALMORA', 'JAGESHWAR', 35, 1.5)
    graph.add_edge('JOSHIMATH', 'AULI', 15, 1.0)
    graph.add_edge('TEHRI', 'GHANSALI', 45, 2.0)
    graph.add_edge('MORADABAD', 'KASHIPUR', 50, 1.25)
    graph.add_edge('KASHIPUR', 'RUDRAPUR', 30, 0.75)
    graph.add_edge('GUPTKASHI', 'SONPRAYAG', 20, 1.0)
    # Joshimath to Govindghat (Valley of Flowers access)
    graph.add_edge('JOSHIMATH', 'GOVINDGHAT', 25, 1.25)
    # Dharchula to Lipulekh (China border)
    graph.add_edge('DHARCHULA', 'LIPULEKH', 90, 6.0) 
    # Munsiyari to Namik Glacier
    graph.add_edge('MUNSIYARI', 'NAMIK', 40, 3.0) 
    # Ukhimath to Chopta (Tungnath trek)
    graph.add_edge('UKHIMATH', 'CHOPTA', 35, 2.0)
    # Gangotri to Gaumukh (glacier trek)
    graph.add_edge('GANGOTRI', 'GAUMUKH', 18, 6.0)
    # Bhimtal to Sattal (7 lakes circuit)
    graph.add_edge('BHIMTAL', 'SATTAL', 10, 0.5)
    # Nainital to Khurpatal (hidden lake)
    graph.add_edge('NAINITAL', 'KHURPATAL', 15, 0.75)
    # Ramnagar to Dhikala (Corbett NP core)
    graph.add_edge('RAMNAGAR', 'DHIKALA', 35, 2.5) 
    # Kotdwar to Lansdowne (forest drive)
    graph.add_edge('KOTDWAR', 'LANSDOWNE', 45, 2.0)
    # Badrinath Winter Route
    graph.add_edge('JOSHIMATH', 'CHAMOLI', 60, 3.0)  
    # Disaster Bypasses (e.g., Kedarnath floods)
    graph.add_edge('GUPTKASHI', 'AUGUSTMUNI', 25, 1.5)
    # Ramnagar ↔ Corbett Park (Core Area)
    graph.add_edge('RAMNAGAR', 'DHIKALA', 35, 2.5) 
    # Haldwani ↔ Tanakpur (Plains Route)
    graph.add_edge('HALDWANI', 'RUDRAPUR', 70, 2.0) 
    graph.add_edge('RUDRAPUR', 'TANAKPUR', 80, 2.5)
    # Tehri ↔ New Tehri (City Connector)
    graph.add_edge('TEHRI', 'NEW_TEHRI', 10, 0.5) 
    # Rishikesh ↔ Neelkanth Mahadev
    graph.add_edge('RISHIKESH', 'NEELKANTH', 32, 1.5)  
    graph.add_edge('BAGESHWAR', 'BAIJNATH', 25, 1.0)  
    # Direct Kausani → Baijnath link (NH309A)
    graph.add_edge('KAUSANI', 'BAIJNATH', 25, 1.0)  
    # Direct Gwaldam → Baijnath link (SH37)
    graph.add_edge('GWALDAM', 'BAIJNATH', 45, 2.0) 
    # 1. Roorkee to Kotdwar (via Najibabad)
    graph.add_edge('ROORKEE', 'NAJIBABAD', 80, 2.0)   
    graph.add_edge('NAJIBABAD', 'KOTDWAR', 40, 1.5)  
    graph.add_edge('KOTDWAR', 'RAMNAGAR', 120, 4.0)   
    graph.add_edge('RAMNAGAR', 'HALDWANI', 70, 2.5)   
    graph.add_edge('ROORKEE', 'NAJIBABAD', 80, 2.0)  
    graph.add_edge('NAJIBABAD', 'KOTDWAR', 40, 1.5)   
    graph.add_edge('KOTDWAR', 'RAMNAGAR', 120, 4.0)  
    graph.add_edge('ROORKEE', 'HARIDWAR', 35, 1.0)   
    graph.add_edge('HARIDWAR', 'RISHIKESH', 25, 0.75) 
    graph.add_edge('RISHIKESH', 'DEHRADUN', 40, 1.5)  
    graph.add_edge('ALMORA', 'PITHORAGARH', 120, 5.0) 
    graph.add_edge('GARUR', 'BAIJNATH', 15, 0.5) 
    graph.add_edge('GARUR', 'BAGESHWAR', 20, 0.75) 
    graph.add_edge('GARUR', 'KAUSANI', 35, 1.5)  
    graph.add_edge('GARUR', 'SOMESHWAR', 30, 1.25)  
    graph.add_edge('SOMESHWAR', 'ALMORA', 20, 0.75)  
    graph.add_edge('PIPALKOTI', 'JOSHIMATH', 30, 1.25)  
    graph.add_edge('PIPALKOTI', 'RUDRAPRAYAG', 55, 2.5)  
    graph.add_edge('PIPALKOTI', 'KARANPRAYAG', 30, 1.25)  
    graph.add_edge('PIPALKOTI', 'SRINAGAR', 65, 3.0)      
    graph.add_edge('MUKTESHWAR', 'BHIMTAL', 25, 1.0)  
    graph.add_edge('MUKTESHWAR', 'ALMORA', 35, 1.5)   
    graph.add_edge('MUKTESHWAR', 'BHOWALI', 20, 0.75) 
    graph.add_edge('MUKTESHWAR', 'RAMNAGAR', 90, 3.5)   
# Load from CSV

    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                graph.add_edge(
                    row['From Station'].strip(),
                    row['To Station'].strip(),
                    float(row['Distance (km)']),
                    float(row['Travel Time (hrs)'])
                )
            except (KeyError, ValueError) as e:
                print(f"Error processing row: {e}")
                continue
    return graph

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_stations')
def get_stations():
    stations = sorted(graph.coordinates.keys())
    return jsonify(stations)

@app.route('/calculate_route', methods=['POST'])
def calculate_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request"}), 400
        
    start = data.get('start')
    end = data.get('end')
    optimize = data.get('optimize', 'distance')
    algorithm = data.get('algorithm', 'dijkstra')
    
    if not start or not end:
        return jsonify({"error": "Start and end locations required"}), 400
        
    try:
        path, distance, time = graph.dijkstra(start, end, optimize)
        
        if not path:
            return jsonify({"error": "No route found"}), 404
            
        path_coordinates = []
        for node in path:
            if node in graph.coordinates:
                lat, lon = graph.coordinates[node]
                path_coordinates.append({
                    "name": node,
                    "lat": lat,
                    "lng": lon
                })
        
        return jsonify({
            "path": path,
            "path_coordinates": path_coordinates,
            "total_distance": distance,
            "total_time": time,
            "optimize": optimize,
            "algorithm": algorithm
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def create_csv_if_not_exists():
    csv_content = """Route,From Station,To Station,Distance (km),Travel Time (hrs)
HALDWANI-KATHGODAM,HALDWANI,KATHGODAM,7,0.25
KATHGODAM-BHIMTAL,KATHGODAM,BHIMTAL,12,0.5
BHIMTAL-BHOWALI,BHIMTAL,BHOWALI,8,0.33
BHOWALI-ALMORA,BHOWALI,ALMORA,28,1.25
BHOWALI-NAINITAL,BHOWALI,NAINITAL,10,0.5
ALMORA-KAUSANI,ALMORA,KAUSANI,52,2
KAUSANI-BAGESHWAR,KAUSANI,BAGESHWAR,40,1.5
ALMORA-RANIKHET,ALMORA,RANIKHET,50,1.75
RANIKHET-NAINITAL,RANIKHET,NAINITAL,60,2
NAINITAL-RAMNAGAR,NAINITAL,RAMNAGAR,70,2.5
RAMNAGAR-HALDWANI,RAMNAGAR,HALDWANI,70,2
DEHRADUN-MUSSOORIE,DEHRADUN,MUSSOORIE,35,1.5
DEHRADUN-RISHIKESH,DEHRADUN,RISHIKESH,40,1
RISHIKESH-HARIDWAR,RISHIKESH,HARIDWAR,25,0.75
HARIDWAR-RUDRAPUR,HARIDWAR,RUDRAPUR,120,3.5
RUDRAPUR-KICHAHA,RUDRAPUR,KICHAHA,30,1
KICHAHA-TANAKPUR,KICHAHA,TANAKPUR,80,2.5
TANAKPUR-PITHORAGARH,TANAKPUR,PITHORAGARH,120,4
PITHORAGARH-DHARCHULA,PITHORAGARH,DHARCHULA,80,3
DEHRADUN-KOTDWAR,DEHRADUN,KOTDWAR,120,3.5
KOTDWAR-NAZIBABAD,KOTDWAR,NAZIBABAD,40,1.25
NAZIBABAD-RISHIKESH,NAZIBABAD,RISHIKESH,80,2.5
RISHIKESH-SRINAGAR,RISHIKESH,SRINAGAR,100,3
SRINAGAR-RUDRAPRAYAG,SRINAGAR,RUDRAPRAYAG,40,1.5
RUDRAPRAYAG-KEDARNATH,RUDRAPRAYAG,KEDARNATH,75,3
RUDRAPRAYAG-BADRINATH,RUDRAPRAYAG,BADRINATH,150,5
BADRINATH-MANA,BADRINATH,MANA,5,0.25
UTTARKASHI-GANGOTRI,UTTARKASHI,GANGOTRI,100,4
BAGESHWAR-CHAUKORI,BAGESHWAR,CHAUKORI,35,1.75
PITHORAGARH-MUNSIYARI,PITHORAGARH,MUNSIYARI,120,5.0
MORADABAD-KASHIPUR,MORADABAD,KASHIPUR,50,1.25
JOSHIMATH-GOVINDGHAT,JOSHIMATH,GOVINDGHAT,25,1.25
UTTARKASHI-RISHIKESH,UTTARKASHI,RISHIKESH,150,4.5"""
    
    with open('../data/uttarakhand_routes.csv', 'w', encoding='utf-8') as f:
        f.write(csv_content)

if __name__ == "__main__":
    create_csv_if_not_exists()
    graph = load_graph_from_csv('../data/uttarakhand_routes.csv')
    webbrowser.open('http://localhost:5000')
    app.run(debug=True)