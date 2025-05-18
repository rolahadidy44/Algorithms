import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class HuffmanVisualizer:
    def __init__(self, root, canvas_frame, fig_size=(3.5, 1.8), node_size=600, font_size=7, speed_ms=750):
        self.root_node = root
        self.canvas_frame = canvas_frame
        self.visited = set()
        self.current_node = None
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        self.node_size = node_size
        self.font_size = font_size
        self.speed_ms = speed_ms
        self.G = nx.DiGraph()
        self.pos = {}
        self.labels = {}
        self._build_graph(self.root_node)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    def _build_graph(self, node, x=0, y=0, layer=2.0):
        if node is None:
            return
        node_id = id(node)
        self.pos[node_id] = (x, -y)
        self.labels[node_id] = f"{node.character if node.character else ''}\n{node.freq}"
        if node.left:
            self.G.add_edge(node_id, id(node.left))
            self._build_graph(node.left, x - 1 / layer, y + 1, layer * 2.0)
        if node.right:
            self.G.add_edge(node_id, id(node.right))
            self._build_graph(node.right, x + 1 / layer, y + 1, layer * 2.0)

    def _draw(self):
        self.ax.clear()
        node_colors = []
        for node in self.G.nodes():
            if node == self.current_node:
                node_colors.append("#FF69B4")
            elif node in self.visited:
                node_colors.append("grey")
            else:
                node_colors.append("#FFE4B5")
        nx.draw(self.G, self.pos, with_labels=False, arrows=False, node_size=self.node_size,
                node_color=node_colors, ax=self.ax)
        nx.draw_networkx_labels(self.G, self.pos, self.labels, ax=self.ax, font_size=self.font_size)
        self.ax.set_axis_off()
        self.canvas.draw()

    def animate(self):
        def traverse(node):
            if node is None:
                return
            node_id = id(node)
            self.current_node = node_id
            self._draw()
            self.canvas_frame.update()
            time.sleep(self.speed_ms / 1000)
            self.visited.add(node_id)
            traverse(node.left)
            traverse(node.right)
        traverse(self.root_node)
