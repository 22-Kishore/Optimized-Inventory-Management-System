import heapq

class Graph:
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex):
        if vertex not in self.vertices:
            self.vertices[vertex] = {}

    def add_edge(self, from_vertex, to_vertex, weight):
        self.vertices[from_vertex][to_vertex] = weight

    def dijkstra_shortest_path(self, start_vertex):
        distances = {vertex: float('inf') for vertex in self.vertices}
        distances[start_vertex] = 0

        priority_queue = [(0, start_vertex)]

        while priority_queue:
            current_distance, current_vertex = heapq.heappop(priority_queue)

            if current_distance > distances[current_vertex]:
                continue

            for neighbor, weight in self.vertices[current_vertex].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(priority_queue, (distance, neighbor))
        print(distances)
        return distances

# Real-time route planning function
def find_shortest_route(graph, pickup_location, destination):
    shortest_distances = graph.dijkstra_shortest_path(pickup_location)
    shortest_distance_to_destination = shortest_distances[destination]

    if shortest_distance_to_destination == float('inf'):
        return "No route available"

    return shortest_distance_to_destination

if __name__ == "__main__":
    # Creating the road network graph
    road_network = Graph()

    # User input: Add vertices (intersections/locations)
    num_vertices = int(input("Enter the number of vertices: "))
    for _ in range(num_vertices):
        vertex = input("Enter vertex: ")
        road_network.add_vertex(vertex)

    # User input: Add edges (road segments) with weights (travel time or distance)
    num_edges = int(input("Enter the number of edges: "))
    for _ in range(num_edges):
        from_vertex, to_vertex, weight = input("Enter from_vertex to_vertex weight separated by space: ").split()
        road_network.add_edge(from_vertex, to_vertex, int(weight))

    # User input: Pickup location and destination
    pickup_location = input("Enter pickup location: ")
    destination = input("Enter destination: ")

    # Finding the shortest route from pickup location to destination
    shortest_distance = find_shortest_route(road_network, pickup_location, destination)

    print(f"Shortest distance from {pickup_location} to {destination}: {shortest_distance}")
