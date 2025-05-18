import tkinter as tk
from tkinter import ttk
from huffman.core import count_frequency, build_huffman_tree, generate_huffman_codes, encode_string, decode_string
from huffman.visualizer import HuffmanVisualizer

PASTEL_ORANGE = "#FFD1A4"
PASTEL_PINK = "#FFC9DE"
PASTEL_PURPLE = "#8624CB"

class HuffmanApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression Tool 💨")
        self.root.geometry("760x600")
        self.root.configure(bg=PASTEL_PINK)
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)

        self.main_menu = tk.Frame(root, bg=PASTEL_PINK)
        self.result_screen = tk.Frame(root, bg=PASTEL_PINK)
        for frame in (self.main_menu, self.result_screen):
            frame.grid(row=0, column=0, sticky="nsew")

        self.huffman_codes = {}  # Initialize Huffman code storage
        self.char_buttons = []

        self.setup_main_menu()
        self.setup_result_screen()
        self.show_frame(self.main_menu)

    def setup_main_menu(self):
        for i in range(3):
            self.main_menu.rowconfigure(i, weight=1)
        self.main_menu.columnconfigure(0, weight=1)

        label = ttk.Label(self.main_menu, text="Enter text to compress:", background=PASTEL_PINK, font=("Helvetica", 14))
        label.grid(row=0, column=0, pady=(80, 10))

        self.entry = ttk.Entry(self.main_menu, width=50, font=("Helvetica", 12))
        self.entry.grid(row=1, column=0, ipady=6)

        submit_btn = ttk.Button(self.main_menu, text="Generate Huffman Codes", command=self.submit_text)
        submit_btn.grid(row=2, column=0, pady=(10, 80), ipadx=8, ipady=4)

    def setup_result_screen(self):
        self.top_frame = tk.Frame(self.result_screen, bg=PASTEL_PINK)
        self.top_frame.pack(fill="x", padx=20, pady=(10, 0))

        self.freq_label = tk.Label(self.top_frame, justify="left", anchor="nw",
                                   font=("Courier New", 9), fg=PASTEL_PURPLE, bg=PASTEL_PINK)
        self.freq_label.grid(row=0, column=0, sticky="nw")

        self.code_label = tk.Label(self.top_frame, justify="left", anchor="nw",
                                   font=("Courier New", 9), fg=PASTEL_PURPLE, bg=PASTEL_PINK)
        self.code_label.grid(row=0, column=1, sticky="nw", padx=(40, 0))

        self.enc_label = tk.Label(self.top_frame, justify="center", anchor="center",
                                  font=("Courier New", 9), fg=PASTEL_PURPLE, bg=PASTEL_PINK)
        self.enc_label.grid(row=0, column=2, padx=(40, 0), sticky="n")

        self.canvas_frame = tk.Frame(self.result_screen, bg=PASTEL_PINK)
        self.canvas_frame.pack(fill="both", expand=True, padx=20, pady=(10, 0))

        self.char_buttons_frame = tk.Frame(self.result_screen, bg=PASTEL_PINK)
        self.char_buttons_frame.pack(pady=(0, 5))

        back_btn = ttk.Button(self.result_screen, text="⬅ Back to Main Menu", command=lambda: self.show_frame(self.main_menu))
        back_btn.pack(padx=10, pady=10, anchor="sw")

    def submit_text(self):
        input_text = self.entry.get()

        # Build from scratch each time
        freq_dict = count_frequency(input_text)
        root = build_huffman_tree(freq_dict)

        self.huffman_codes = generate_huffman_codes(root)
        encoded = encode_string(input_text, self.huffman_codes)
        decoded = decode_string(encoded, self.huffman_codes)

        freq_text = "Character Frequencies:\n"
        for char, freq in freq_dict.items():
            freq_text += f"{repr(char)}: {freq}\n"

        code_text = "Huffman Codes:\n"
        for char, code in self.huffman_codes.items():
            code_text += f"{repr(char)}: {code}\n"

        encoded_decoded = f"Encoded: {encoded}\n\nDecoded: {decoded}"

        self.freq_label.config(text=freq_text)
        self.code_label.config(text=code_text)
        self.enc_label.config(text=encoded_decoded)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        for widget in self.char_buttons_frame.winfo_children():
            widget.destroy()

        visualizer = HuffmanVisualizer(root, self.canvas_frame, self.huffman_codes, fig_size=(3.5, 1.8), node_size=600, font_size=7, speed_ms=500)
        self.root.after(100, visualizer.animate_build)

        for char in sorted(self.huffman_codes.keys()):
            btn = ttk.Button(self.char_buttons_frame, text=char, command=lambda c=char: visualizer.highlight_encoding_path(c))
            btn.pack(side="left", padx=5)
            self.char_buttons.append(btn)

        self.show_frame(self.result_screen)

    def show_frame(self, frame):
        frame.tkraise()
        if frame == self.main_menu:
            self.entry.delete(0, tk.END)
            self.huffman_codes = {}
            for widget in self.result_screen.winfo_children():
                widget.destroy()
            self.setup_result_screen()

def launch_gui():
    root = tk.Tk()
    app = HuffmanApp(root)
    root.mainloop()
