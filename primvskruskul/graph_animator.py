import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading, time, random

class GraphAnimator:
    def __init__(self, root):
        self.G = nx.Graph()  # The main graph
        self.pos = {}  # Dictionary of node positions
        self.root = root
        self.queue_callback = None  # Callback to update the queue label
        self.total_weight_callback = None  # Callback to update the total weight label
        self.path_callback = None  # Callback to update the path trace
        self.text_labels = []  # Temporary text labels (e.g., reasons)
        self.current_algorithm = ""  # Track current algorithm to prefix total weight

        # Set up the drawing canvas
        self.fig, self.ax = plt.subplots(figsize=(6, 4))
        self.canvas = FigureCanvasTkAgg(self.fig, master=root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)
        self._reset_colors()

    def get_tk_widget(self):
        return self.canvas

    def set_queue_callback(self, callback):
        self.queue_callback = callback

    def set_total_weight_callback(self, callback):
        self.total_weight_callback = callback

    def set_path_callback(self, callback):
        self.path_callback = callback

    def reset_graph(self):
        self.generate_random_graph()
        self._draw_graph()
        if self.path_callback:
            self.path_callback("")
        if self.total_weight_callback:
            self.total_weight_callback(0, self.current_algorithm)

    def generate_random_graph(self):
        self.G.clear()
        self.pos.clear()
        self.G.add_nodes_from(range(6))  # Add 6 nodes
        edges = []
        for i in range(6):
            for j in range(i + 1, 6):
                if random.random() < 0.5:
                    weight = random.randint(1, 20)
                    edges.append((i, j, weight))
        self.G.add_weighted_edges_from(edges)
        self.pos = nx.spring_layout(self.G, seed=42)  # Generate layout

    def _reset_colors(self):
        self._draw_graph()

    def _draw_graph(self, highlight_edges=[], highlight_nodes=[], queue=[], temp_red_edges=[], total_weight=0, reasons={}):
        self.ax.clear()
        self.text_labels.clear()
        node_colors = []

        # Color nodes
        for n in self.G.nodes:
            if n in highlight_nodes:
                if highlight_nodes[-1] == n:
                    node_colors.append("#FF69B4")  # current node: pink
                else:
                    node_colors.append("dimgray")  # visited
            else:
                node_colors.append("lightgrey")  # default

        # Color edges
        edge_colors = []
        for u, v in self.G.edges:
            if (u, v) in highlight_edges or (v, u) in highlight_edges:
                edge_colors.append("lightgreen")  # part of MST
            elif (u, v) in temp_red_edges or (v, u) in temp_red_edges:
                edge_colors.append("red")  # rejected
            else:
                edge_colors.append("darkgrey")  # default

        # Draw graph
        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors,
                edge_color=edge_colors, ax=self.ax)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=self.ax)

        # Draw red labels for rejected reasons
        for (u, v), reason in reasons.items():
            x, y = (self.pos[u][0] + self.pos[v][0]) / 2, (self.pos[u][1] + self.pos[v][1]) / 2
            self.ax.text(x, y + 0.05, reason, color='red', fontsize=8, ha='center')

        # Callback for weight
        if self.total_weight_callback:
            self.total_weight_callback(total_weight, self.current_algorithm)

        # Callback for readable queue
        if self.queue_callback:
            readable_queue = {}
            for w, u, v in queue:
                if u not in readable_queue:
                    readable_queue[u] = []
                readable_queue[u].append(f"({u}-{v}: {w})")
            formatted = [f"From {k}: {', '.join(v)}" for k, v in readable_queue.items()]
            self.queue_callback(formatted)

        self.canvas.draw()

    def animate_prim(self):
        self.current_algorithm = "Prim"
        if self.total_weight_callback:
            self.total_weight_callback(0, self.current_algorithm)
        self._reset_colors()

        def run():
            visited = set()
            queue = []  # Priority queue: (weight, from, to)
            mst_edges = []  # Final MST
            total_weight = 0
            path_order = []

            start = 0
            visited.add(start)
            path_order.append(start)

            for v in self.G.neighbors(start):
                queue.append((self.G[start][v]['weight'], start, v))
            queue.sort()
            self._draw_graph(mst_edges, list(visited), queue, [], total_weight)

            while queue:
                w, u, v = queue.pop(0)
                reasons = {}
                if v in visited:
                    reasons[(u, v)] = "previously visited"
                    self._draw_graph(mst_edges, list(visited), queue, [(u, v)], total_weight, reasons)
                    time.sleep(0.6)
                    continue

                visited.add(v)
                path_order.append(v)
                mst_edges.append((u, v))
                total_weight += w
                self._draw_graph(mst_edges, list(visited), queue, [], total_weight)
                time.sleep(1)

                for n in self.G.neighbors(v):
                    if n not in visited:
                        queue.append((self.G[v][n]['weight'], v, n))
                queue.sort()

            time.sleep(1)
            if self.path_callback:
                self.path_callback("Prim total path: " + "-".join(map(str, path_order)))
            self._draw_graph(total_weight=total_weight)

        threading.Thread(target=run).start()

    def animate_kruskal(self):
        self.current_algorithm = "Kruskal"
        if self.total_weight_callback:
            self.total_weight_callback(0, self.current_algorithm)
        self._reset_colors()

        def run():
            parent = {n: n for n in self.G.nodes}

            def find(u):
                while parent[u] != u:
                    u = parent[u]
                return u

            def union(u, v):
                pu, pv = find(u), find(v)
                if pu != pv:
                    parent[pu] = pv
                    return True
                return False

            edges = sorted(self.G.edges(data=True), key=lambda x: x[2]['weight'])
            mst_edges = []
            queue = [(d['weight'], u, v) for u, v, d in edges]
            total_weight = 0
            path_order = []

            for w, u, v in queue:
                reasons = {}
                if find(u) == find(v):
                    reasons[(u, v)] = "would form cycle"
                    self._draw_graph(mst_edges, list(sum(([u, v] for u, v in mst_edges), [])), queue, [(u, v)], total_weight, reasons)
                    time.sleep(0.6)
                    continue

                union(u, v)
                mst_edges.append((u, v))
                total_weight += w
                path_order.extend([u, v])
                self._draw_graph(mst_edges, list(sum(([u, v] for u, v in mst_edges), [])), queue, [], total_weight)
                time.sleep(1)

            if self.path_callback:
                seen = set()
                result = []
                for x in path_order:
                    if x not in seen:
                        seen.add(x)
                        result.append(str(x))
                self.path_callback("Kruskal total path: " + "-".join(result))

            time.sleep(1)
            self._draw_graph(total_weight=total_weight)

        threading.Thread(target=run).start()