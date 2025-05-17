import tkinter as tk
from tkinter import ttk
from huffman.core import count_frequency, build_huffman_tree, generate_huffman_codes
from huffman.visualizer import draw_huffman_tree 
# Colors
PASTEL_ORANGE = "#FFD1A4"
PASTEL_PINK = "#FFC9DE"
PASTEL_BLUE = "#D0E8FF"
TEXT_COLOR = "#333333"

def submit_text():
    input_text = entry.get()
    freq_dict = count_frequency(input_text)
    root = build_huffman_tree(freq_dict)
    huffman_codes = generate_huffman_codes(root)

    output_text.config(state="normal")
    output_text.delete("1.0", tk.END)

    for char, code in huffman_codes.items():
        output_text.insert(tk.END, f"Character: {repr(char)} | Code: {code}\n")
    draw_huffman_tree(root) 
    output_text.config(state="disabled")

window = tk.Tk()
window.title("Huffman Compression Tool 💨")
window.geometry("550x520")
window.configure(bg=PASTEL_PINK)

 
style = ttk.Style()
style.theme_use("clam")

style.configure("TLabel", font=("Helvetica", 13), background=PASTEL_PINK, foreground=TEXT_COLOR)
style.configure("TEntry", font=("Helvetica", 12))
style.configure("TButton", font=("Helvetica", 12), padding=6, background=PASTEL_ORANGE)

# Label
entry_label = ttk.Label(window, text="Enter text to compress:")
entry_label.pack(pady=(20, 5))

# Entry
entry = ttk.Entry(window, width=50)
entry.pack(pady=(0, 10))

# Button
submit_button = ttk.Button(window, text="Generate Huffman Codes", command=submit_text)
submit_button.pack(pady=(0, 20))

# Output
output_frame = tk.Frame(window, bg=PASTEL_BLUE, bd=2, relief="ridge")
output_frame.pack(pady=(0, 20), padx=10)

output_text = tk.Text(output_frame, height=15, width=60, font=("Courier New", 11), wrap="word", bg=PASTEL_BLUE, fg=TEXT_COLOR, relief="flat")
output_text.pack()
output_text.config(state="disabled")

window.mainloop()
