import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading, time, random

class GraphAnimator:
    def __init__(self, root):
        self.G = nx.Graph()
        self.pos = {}
        self.root = root
        self.queue_callback = None
        self.total_weight_callback = None
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

    def reset_graph(self):
        self.generate_random_graph()
        self._draw_graph()

    def generate_random_graph(self):
        self.G.clear()
        self.pos.clear()
        self.G.add_nodes_from(range(6))
        edges = []
        for i in range(6):
            for j in range(i + 1, 6):
                if random.random() < 0.5:
                    weight = random.randint(1, 20)
                    edges.append((i, j, weight))
        self.G.add_weighted_edges_from(edges)
        self.pos = nx.spring_layout(self.G, seed=42)

    def _reset_colors(self):
        self._draw_graph()

    def _draw_graph(self, highlight_edges=[], highlight_nodes=[], queue=[], temp_red_edges=[], total_weight=0):
        self.ax.clear()
        node_colors = []
        for n in self.G.nodes:
            if n in highlight_nodes:
                if highlight_nodes[-1] == n:
                    node_colors.append("#FF69B4")  # current: hot pink
                else:
                    node_colors.append("dimgray")  # previously visited
            else:
                node_colors.append("lightgrey")  # default

        edge_colors = []
        for u, v in self.G.edges:
            if (u, v) in highlight_edges or (v, u) in highlight_edges:
                edge_colors.append("lightgreen")
            elif (u, v) in temp_red_edges or (v, u) in temp_red_edges:
                edge_colors.append("red")
            else:
                edge_colors.append("darkgrey")

        nx.draw(self.G, self.pos, with_labels=True, node_color=node_colors,
                edge_color=edge_colors, ax=self.ax)
        labels = nx.get_edge_attributes(self.G, 'weight')
        nx.draw_networkx_edge_labels(self.G, self.pos, edge_labels=labels, ax=self.ax)

        if self.total_weight_callback:
            self.total_weight_callback(total_weight)
        self.canvas.draw()

        if self.queue_callback:
            self.queue_callback(queue.copy())

    def animate_prim(self):
        self._reset_colors()

        def run():
            visited = set()
            queue = []
            mst_edges = []
            total_weight = 0

            start = 0
            visited.add(start)
            for v in self.G.neighbors(start):
                queue.append((self.G[start][v]['weight'], start, v))
            queue.sort()
            self._draw_graph(mst_edges, list(visited), queue, [], total_weight)


            while queue:
                w, u, v = queue.pop(0)
                temp = [(u, v)]
                self._draw_graph(mst_edges, list(visited) + [v], queue, temp, total_weight)
                time.sleep(0.5)

                if v in visited:
                    continue

                visited.add(v)
                mst_edges.append((u, v))
                total_weight += w
                self._draw_graph(mst_edges, list(visited), queue, [], total_weight)
                time.sleep(1)

                for n in self.G.neighbors(v):
                    if n not in visited:
                        queue.append((self.G[v][n]['weight'], v, n))
                queue.sort()

            time.sleep(3)
            self._draw_graph(total_weight=total_weight)

        threading.Thread(target=run).start()

    def animate_kruskal(self):
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

            for w, u, v in queue:
                self._draw_graph(mst_edges, list(sum(([u, v] for u, v in mst_edges), [])), queue, [(u, v)], total_weight)
                time.sleep(0.5)
                if union(u, v):
                    mst_edges.append((u, v))
                    total_weight += w
                    self._draw_graph(mst_edges, list(sum(([u, v] for u, v in mst_edges), [])), queue, [], total_weight)
                    time.sleep(1)

            time.sleep(3)
            self._draw_graph(total_weight=total_weight)

        threading.Thread(target=run).start()
