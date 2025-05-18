import tkinter as tk
from tkinter import ttk
from graph_animator import GraphAnimator

PASTEL_PINK = "#FFC9DE"

class PrimKruskalApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Prim vs Kruskal Animation")
        self.root.geometry("900x700")
        self.root.configure(bg=PASTEL_PINK)

        self.graph_animator = GraphAnimator(root)
        self.graph_animator.canvas.get_tk_widget().pack(fill="both", expand=True)

        control_frame = tk.Frame(root, bg=PASTEL_PINK)
        control_frame.pack(pady=10)

        ttk.Button(control_frame, text="Start Prim Animation", command=self.start_prim).pack(side="left", padx=20)
        ttk.Button(control_frame, text="Start Kruskal Animation", command=self.start_kruskal).pack(side="left", padx=20)
        ttk.Button(control_frame, text="Generate New Tree", command=self.graph_animator.reset_graph).pack(side="left", padx=20)

        self.weight_label = tk.Label(root, text="Total Weight: 0", bg=PASTEL_PINK, font=("Courier", 11, "bold"))
        self.weight_label.pack()

        self.queue_label = tk.Label(root, text="Priority Queue: []", bg=PASTEL_PINK, font=("Courier", 10))
        self.queue_label.pack(pady=5)

        self.graph_animator.set_queue_callback(self.update_queue_display)
        self.graph_animator.set_total_weight_callback(self.update_total_weight)

    def update_queue_display(self, queue):
        self.queue_label.config(text=f"Priority Queue: {queue}")

    def update_total_weight(self, weight):
        self.weight_label.config(text=f"Total Weight: {weight}")

    def start_prim(self):
        self.graph_animator.animate_prim()

    def start_kruskal(self):
        self.graph_animator.animate_kruskal()

def launch_gui():
    root = tk.Tk()
    app = PrimKruskalApp(root)
    root.mainloop()
