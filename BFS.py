from collections import deque
from collections import defaultdict

# --- Constants for labeling states ---
UNEXPLORED = "UNEXPLORED"
VISITED = "VISITED"
DISCOVERY = "DISCOVERY"
CROSS = "CROSS"

# --- Graph Data Structure Classes ---

class Vertex:
    """A vertex in a graph."""
    def __init__(self, element):
        self.element = element

    def __hash__(self):
        """Allow vertices to be used as dictionary keys."""
        return hash(self.element)

    def __eq__(self, other):
        return self.element == other.element

    def __repr__(self):
        return f"Vertex({self.element})"

class Edge:
    """An edge between two vertices in a graph."""
    def __init__(self, v, w):
        self.endpoints = (v, w)

    def __hash__(self):
        """Allow edges to be used as dictionary keys, order-independent."""
        return hash(frozenset(self.endpoints))

    def __eq__(self, other):
        return frozenset(self.endpoints) == frozenset(other.endpoints)
        
    def __repr__(self):
        return f"Edge({self.endpoints[0].element}, {self.endpoints[1].element})"

class Graph:
    """A graph representation using adjacency maps for vertices and edges."""
    def __init__(self):
        self.vertices_map = {}  # Map from vertex element to Vertex object
        self.adjacency_map = {} # Map from Vertex object to a list of its incident Edges

    def vertices(self):
        """Return an iterator over all Vertex objects in the graph."""
        return self.vertices_map.values()

    def edges(self):
        """Return a set of all Edge objects in the graph."""
        unique_edges = set()
        for edge_list in self.adjacency_map.values():
            for edge in edge_list:
                unique_edges.add(edge)
        return unique_edges

    def get_vertex(self, element):
        """Return the Vertex object associated with an element."""
        return self.vertices_map.get(element)

    def incident_edges(self, v):
        """Return an iterator over all Edge objects incident to Vertex v."""
        return self.adjacency_map.get(v, [])

    def insert_vertex(self, element):
        """Insert and return a new Vertex with a given element."""
        if element not in self.vertices_map:
            v = Vertex(element)
            self.vertices_map[element] = v
            self.adjacency_map[v] = []
            return v
        return self.get_vertex(element)

    def insert_edge(self, v_element, w_element):
        """Insert and return a new Edge between two vertex elements."""
        v = self.insert_vertex(v_element)
        w = self.insert_vertex(w_element)
        edge = Edge(v, w)
        self.adjacency_map[v].append(edge)
        self.adjacency_map[w].append(edge)
        return edge

    def opposite(self, v, e):
        """Given a vertex v and an incident edge e, return the other vertex."""
        v1, v2 = e.endpoints
        return v2 if v1 == v else v1


class BFSTemplate:
    """
    A Python implementation of the template method pattern for Breadth-First Search.
    This version works with explicit Vertex, Edge, and Graph objects.
    """
    def __init__(self, graph):
        self.graph = graph
        self.vertex_labels = defaultdict()
        self.edge_labels = defaultdict()

    # --- Hooks for customization (to be overridden by subclasses) ---
    # (Hooks are identical to the previous version, so they are omitted for brevity)
    def init_result(self): pass
    def start_bfs_component(self, s): pass
    def finish_bfs_component(self, s): pass
    def pre_component_visit(self, v): pass
    def post_component_visit(self, v): pass
    def pre_vertex_visit(self, v): pass
    def post_vertex_visit(self, v): pass
    def pre_edge_visit(self, v, w, e): pass
    def pre_disc_edge_visit(self, v, w, e): pass
    def post_disc_edge_visit(self, v, w, e): pass
    def cross_edge_visit(self, v, w, e): pass
    def post_init_vertex(self, v): pass
    def post_init_edge(self, e): pass
    def is_next_componenet(self, v):
        if self.vertex_labels[v] == UNEXPLORED:
            return True

    def result(self):
        """Hook to return the final result of the BFS traversal."""
        # Convert object keys to string representation for readability
        readable_v_labels = {v.element: label for v, label in self.vertex_labels.items()}
        readable_e_labels = {repr(e): label for e, label in self.edge_labels.items()}
        return {"vertices": readable_v_labels, "edges": readable_e_labels}

    # --- Core BFS Algorithm --

    def bfs(self):
        """Main BFS algorithm driver (Handles all components)."""
        self.init_result()
        for v in self.graph.vertices():
            self.vertex_labels[v] = UNEXPLORED
        for e in self.graph.edges():
            self.edge_labels[e] = UNEXPLORED
        for v in self.graph.vertices():
            if self.is_next_componenet(v):
                self.pre_component_visit(v)
                self._bfs_component(v)
                self.post_component_visit(v)
        return self.result()

    def _bfs_component(self, s):
        """Performs a BFS traversal on a single connected component."""
        self.start_bfs_component(s)
        self.vertex_labels[s] = VISITED
        q = deque([s])

        while q:
            v = q.popleft()
            self.pre_vertex_visit(v)

            for e in self.graph.incident_edges(v):
                w = self.graph.opposite(v, e)
                self.pre_edge_visit(v, w, e)

                if self.vertex_labels[w] == UNEXPLORED:
                    self.pre_disc_edge_visit(v, w, e)
                    self.edge_labels[e] = DISCOVERY
                    self.vertex_labels[w] = VISITED
                    q.append(w)
                    self.post_disc_edge_visit(v, w, e)
                elif self.edge_labels[e] == UNEXPLORED: # It's a cross edge
                    self.edge_labels[e] = CROSS
                    self.cross_edge_visit(v, w, e)
            
            self.post_vertex_visit(v)
        
        self.finish_bfs_component(s)

    
# --- Example Usage ---
if __name__ == "__main__":
    # 1. Build the graph using the new classes
    g = Graph()
    g.insert_edge('A', 'B')
    g.insert_edge('A', 'C')
    g.insert_edge('B', 'D')
    g.insert_edge('B', 'E')
    g.insert_edge('C', 'F')
    g.insert_edge('E', 'F')
    g.insert_vertex('G') # A disconnected vertex
    g.insert_edge('H', 'I') # Another component
    
    # Demonstrate the new edges() method
    print(f"Total number of edges in the graph: {len(g.edges())}")
    print(f"The edges are: {g.edges()}")


    # 3. Run the BFS
    print("\n--- Running Template BFS ---")
    bfs_runner = BFSTemplate(g)
    final_result = bfs_runner.bfs()
    print("\n--- Final Result ---")
    print("Vertex Labels:", final_result["vertices"])
    print("Edge Labels:", final_result["edges"])
