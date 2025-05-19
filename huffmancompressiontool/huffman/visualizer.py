import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

class HuffmanVisualizer:
    def __init__(self, root_node, canvas_frame, huffman_codes, fig_size=(3.5, 1.8), node_size=600, font_size=7, speed_ms=750):
        self.root_node = root_node
        self.canvas_frame = canvas_frame
        self.huffman_codes = huffman_codes
        self.visited = set()
        self.current_node = None
        self.node_map = {}
        self.arrow_labels = {}
        self.fig, self.ax = plt.subplots(figsize=fig_size)
        self.node_size = node_size
        self.font_size = font_size
        self.speed_ms = speed_ms
        self.G = nx.DiGraph()
        self.pos = {}
        self.labels = {}
        self.hidden_nodes = set()
        self.visible_edges = set()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

        self._build_graph(self.root_node)

    def _build_graph(self, node, x=0, y=0, layer=2.0):
        if node is None:
            return
        node_id = id(node)
        char_label = node.character if node.character else self._get_combined_label(node)
        self.labels[node_id] = f"{char_label}\n{node.freq}"
        self.pos[node_id] = (x, -y)
        self.hidden_nodes.add(node_id)

        if node.character:
            self.node_map[node.character] = node_id

        if node.left:
            edge = (node_id, id(node.left))
            self.G.add_edge(*edge)
            self.arrow_labels[edge] = '0'
            self._build_graph(node.left, x - 1 / layer, y + 1, layer * 2.0)

        if node.right:
            edge = (node_id, id(node.right))
            self.G.add_edge(*edge)
            self.arrow_labels[edge] = '1'
            self._build_graph(node.right, x + 1 / layer, y + 1, layer * 2.0)

    def _get_combined_label(self, node):
        def gather_chars(n):
            if not n:
                return ""
            if n.character:
                return n.character
            return gather_chars(n.left) + gather_chars(n.right)
        return f"({gather_chars(node.left)}+{gather_chars(node.right)})"

    def _draw(self):
        self.ax.clear()

        visible_nodes = [n for n in self.G.nodes() if n not in self.hidden_nodes]

        # Draw nodes
        node_colors = []
        for node in self.G.nodes():
            if node not in visible_nodes:
                node_colors.append((0, 0, 0, 0))  # transparent
            elif node == self.current_node:
                node_colors.append("#FF69B4")  # pink
            elif node in self.visited:
                node_colors.append("lightgrey")
            else:
                node_colors.append("#FFE4B5")

        nx.draw_networkx_nodes(
            self.G, self.pos, nodelist=self.G.nodes(), node_color=node_colors,
            node_size=self.node_size, ax=self.ax
        )

        # Draw labels for visible nodes
        visible_labels = {n: self.labels[n] for n in visible_nodes}
        nx.draw_networkx_labels(
            self.G, self.pos, visible_labels, ax=self.ax, font_size=self.font_size
        )

        # Draw only visible edges and their labels
        visible_edges = list(self.visible_edges)

        nx.draw_networkx_edges(
            self.G,
            self.pos,
            edgelist=visible_edges,
            ax=self.ax,
            edge_color="black",
            arrows=False
        )

        visible_edge_labels = {
            e: self.arrow_labels[e] for e in visible_edges if e in self.arrow_labels
        }

        nx.draw_networkx_edge_labels(
            self.G,
            self.pos,
            edge_labels=visible_edge_labels,
            font_color="black",
            ax=self.ax,
            font_size=self.font_size - 2  # smaller edge label font
        )

        self.ax.set_axis_off()
        self.canvas.draw()

    def animate_build(self):
        def gather_merge_steps(node):
            if node is None or node.character is not None:
                return []
            steps = []
            left_id = id(node.left)
            right_id = id(node.right)
            parent_id = id(node)
            steps += gather_merge_steps(node.left)
            steps += gather_merge_steps(node.right)
            return steps + [[left_id, right_id, parent_id]]

        merge_steps = gather_merge_steps(self.root_node)
        self.visited.clear()
        self.current_node = None

        for step in merge_steps:
            for node_id in step:
                self.hidden_nodes.discard(node_id)
                self.current_node = node_id

                # Reveal incoming edge to this node
                for parent, child in self.G.edges():
                    if child == node_id:
                        self.visible_edges.add((parent, child))

            self._draw()
            self.canvas_frame.update()
            time.sleep(self.speed_ms / 1000)

            for node_id in step:
                self.visited.add(node_id)
            self.current_node = None
            self._draw()

    def highlight_encoding_path(self, char):
        code = self.huffman_codes.get(char)
        if not code:
            return

        node = self.root_node
        path = []
        for bit in code:
            path.append(id(node))
            node = node.left if bit == '0' else node.right
        path.append(id(node))

        self.visited.clear()
        for node_id in path:
            self.current_node = node_id
            self.visited.add(node_id)
            self._draw()
            self.canvas_frame.update()
            time.sleep(self.speed_ms / 1000)

        self.current_node = None
        self._draw()
