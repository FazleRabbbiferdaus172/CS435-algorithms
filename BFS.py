from collections import deque

# --- Constants for labeling states ---
UNEXPLORED = "UNEXPLORED"
VISITED = "VISITED"
DISCOVERY = "DISCOVERY"
CROSS = "CROSS"

class BFSTemplate:
    """
    A Python implementation of the template method pattern for Breadth-First Search.

    This class provides a generic BFS traversal algorithm with "hooks" (methods)
    that can be overridden in a subclass to perform specific actions during the
    traversal, such as finding connected components, calculating shortest paths, etc.
    """

    def __init__(self, graph):
        """
        Initializes the BFS template with a given graph.

        Args:
            graph (dict): A dictionary representing the graph as an adjacency list.
                          Example: {'A': ['B', 'C'], 'B': ['A', 'D'], ...}
        """
        self.graph = graph
        self.vertex_labels = {}
        self.edge_labels = {}

    # --- Hooks for customization (to be overridden by subclasses) ---

    def start_bfs_component(self, s):
        """Hook called at the beginning of a new BFS component traversal."""
        print(f"  Starting BFS component from: {s}")

    def finish_bfs_component(self, s):
        """Hook called at the end of a BFS component traversal."""
        print(f"  Finished BFS component from: {s}")

    def pre_component_visit(self, v):
        """Hook called before starting a new component search at vertex v."""
        pass

    def post_component_visit(self, v):
        """Hook called after finishing a component search that started at v."""
        pass

    def pre_vertex_visit(self, v):
        """Hook called right after a vertex is dequeued."""
        print(f"    Visiting vertex: {v}")

    def post_vertex_visit(self, v):
        """Hook called after visiting all incident edges of a vertex."""
        pass

    def pre_edge_visit(self, v, w):
        """Hook called before processing an edge (v, w)."""
        pass

    def pre_disc_edge_visit(self, v, w):
        """Hook called before processing a discovery edge."""
        pass

    def post_disc_edge_visit(self, v, w):
        """Hook called after processing a discovery edge."""
        pass

    def cross_edge_visit(self, v, w):
        """Hook called when a cross edge is found."""
        print(f"      Cross edge found: ({v}, {w})")

    def result(self):
        """Hook to return the final result of the BFS traversal."""
        return {"vertices": self.vertex_labels, "edges": self.edge_labels}

    # --- Core BFS Algorithm ---

    def _init_result(self):
        """Initializes all vertex and edge labels to UNEXPLORED."""
        for v in self.graph:
            self.vertex_labels[v] = UNEXPLORED
        # Note: Edges are labeled as they are discovered.

    def bfs(self):
        """
        The main BFS algorithm driver. It iterates through all vertices to find
        all connected components in the graph.
        """
        self._init_result()
        for v in self.graph:
            if self.vertex_labels[v] == UNEXPLORED:
                self.pre_component_visit(v)
                self._bfs_component(v)
                self.post_component_visit(v)
        return self.result()

    def _bfs_component(self, s):
        """
        Performs a BFS traversal on a single connected component starting from s.
        """
        self.start_bfs_component(s)
        self.vertex_labels[s] = VISITED
        
        q = deque([s])

        while q:
            v = q.popleft()
            self.pre_vertex_visit(v)

            for w in self.graph.get(v, []): # Iterate over incident edges (v, w)
                self.pre_edge_visit(v, w)
                
                # Ensure edge label key is consistent for undirected graphs
                edge = tuple(sorted((v, w)))

                if self.vertex_labels[w] == UNEXPLORED:
                    self.pre_disc_edge_visit(v, w)
                    self.edge_labels[edge] = DISCOVERY
                    self.vertex_labels[w] = VISITED
                    q.append(w)
                    self.post_disc_edge_visit(v, w)
                elif self.edge_labels.get(edge) == None: # It's a cross edge
                    self.edge_labels[edge] = CROSS
                    self.cross_edge_visit(v, w)
            
            self.post_vertex_visit(v)
        
        self.finish_bfs_component(s)


# --- Example Usage ---
if __name__ == "__main__":
    # A simple graph with two connected components
    sample_graph = {
        'A': ['B', 'C'],
        'B': ['A', 'D', 'E'],
        'C': ['A', 'F'],
        'D': ['B'],
        'E': ['B', 'F'],
        'F': ['C', 'E'],
        'G': ['H'],
        'H': ['G']
    }

    print("--- Running Template BFS ---")
    bfs_runner = BFSTemplate(sample_graph)
    final_result = bfs_runner.bfs()
    print("\n--- Final Result ---")
    print("Vertex Labels:", final_result["vertices"])
    print("Edge Labels:", final_result["edges"])

    # --- How to extend the template ---
    class ComponentCounter(BFSTemplate):
        """A subclass to demonstrate how to use the template hooks."""
        def __init__(self, graph):
            super().__init__(graph)
            self.count = 0

        def pre_component_visit(self, v):
            """Override hook to increment count for each new component."""
            self.count += 1
            print(f"\nFound component {self.count}, starting at {v}")

        # Override result to return the count
        def result(self):
            return self.count

    print("\n\n--- Running Subclassed BFS to Count Components ---")
    component_finder = ComponentCounter(sample_graph)
    num_components = component_finder.bfs()
    print(f"\nTotal number of connected components: {num_components}")