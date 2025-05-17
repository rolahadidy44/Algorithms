import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt

def draw_huffman_tree(root):
    G = nx.DiGraph()
    pos = {}
    labels = {}

    def traverse(node, x=0, y=0, layer=1):
        if node is None:
            return

        node_id = id(node)
        pos[node_id] = (x, -y)
        labels[node_id] = f"{node.character if node.character else ''}\n{node.freq}"

        if node.left:
            left_id = id(node.left)
            G.add_edge(node_id, left_id)
            traverse(node.left, x - 1 / layer, y + 1, layer * 1.5)

        if node.right:
            right_id = id(node.right)
            G.add_edge(node_id, right_id)
            traverse(node.right, x + 1 / layer, y + 1, layer * 1.5)

    traverse(root)
    plt.figure(figsize=(12, 8))
    nx.draw(G, pos, with_labels=False, arrows=False, node_size=2000, node_color="#FFE4B5")
    nx.draw_networkx_labels(G, pos, labels)
    plt.title("Huffman Tree")
    plt.show()
