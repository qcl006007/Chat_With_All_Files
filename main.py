import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import os
from chat import create_llama_index, get_answer_from_index
import uuid
from llm import create_graph

files_indexes = []
file_index_names = []

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf"), ("Text Files", "*.txt"), ("Markdown Files", "*.md")])
    file_name = os.path.basename(file_path)
    index = create_llama_index(file_path, file_name)
    files_indexes.append(index)
    print("file uploaded!")
    file_template = "${file} has been uploaded successfully."
    file_box.insert(tk.END, file_template.format(file = file_name))


# Define a function to get the chat text
def get_chat_text():
    question = input_box.get("1.0", tk.END)
    index = files_indexes[0]
    answer = get_answer_from_index(question, index)
    output_box.delete("1.0", tk.END)
    output_box.insert(tk.END, answer)
    
def create_index_graph(file_names):
    index_set = {}
    for file_path in file_names:
        file_name = os.path.basename(file_path)
        index = create_llama_index(file_path, file_name)
        index_set[file_name] = index
    graph_name = str(uuid.uuid4())
    graph = create_graph(index_set, graph_name)
    return graph_name, graph

# Create the main window
root = tk.Tk()
root.title("My File Application")
root.geometry("700x600")
root.configure(bg='white')

# Create the input box and submit button
input_label = tk.Label(root, text="Enter your question:", anchor="w", font=("Arial", 12), bg="white", padx=10, pady=10)
input_label.pack()
input_box = tk.Text(root, height=10, width=50)
input_box.pack()
submit_button = tk.Button(root, text="Submit", command=get_chat_text, font=("Arial", 12), bg="white", padx=10, pady=5)
submit_button.pack()

# Create the output box
output_label = tk.Label(root, text="Output:", anchor="w", font=("Arial", 12), bg="white", padx=10, pady=10)
output_label.pack()
output_box = tk.Text(root, height=10, width=50)
output_box.pack()

# Create the file selection box and button
file_label = tk.Label(root, text="Select a file:", anchor="w", font=("Arial", 12), bg="white", padx=10, pady=10)
file_label.pack()
file_box = tk.Text(root, height=3, width=50)
file_box.pack()
browse_button = tk.Button(root, text="Browse", command=select_file, font=("Arial", 12), bg="white", padx=10, pady=5)
browse_button.pack()


# Start the main loop
root.mainloop()
