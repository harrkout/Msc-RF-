import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import webbrowser

# Propagation models

def free_space_model(distance, frequency):
    """
    Calculate path loss using the Free Space Propagation Model.

    Parameters:
    - distance (float): Distance between transmitter and receiver (in km).
    - frequency (float): Frequency of the signal (in Hz).

    Returns:
    - float: Path loss (in dB).
    """
    return 20 * np.log10(distance) + 20 * np.log10(frequency) - 147.55

def two_ray_ground_model(distance, frequency, height_transmitter, height_receiver):
    """
    Calculate path loss using the Two-Ray Ground Reflection Model.

    Parameters:
    - distance (float): Distance between transmitter and receiver (in km).
    - frequency (float): Frequency of the signal (in Hz).
    - height_transmitter (float): Height of the transmitter (in meters).
    - height_receiver (float): Height of the receiver (in meters).

    Returns:
    - float: Path loss (in dB).
    """
    wavelength = 3e8 / frequency
    d1 = np.sqrt((distance ** 2) + ((height_receiver - height_transmitter) ** 2))
    d2 = np.sqrt((distance ** 2) + ((height_receiver + height_transmitter) ** 2))
    path_loss = (wavelength / (4 * np.pi * d1 * d2)) ** 2
    return 10 * np.log10(path_loss)

def okumura_model(distance, frequency):
    """
    Calculate path loss using the Okumura model.

    Parameters:
    - distance (float): Distance between transmitter and receiver (in km).
    - frequency (float): Frequency of the signal (in Hz).

    Returns:
    - float: Path loss (in dB).
    """
    return 69.55 + 26.16 * np.log10(distance) + 20 * np.log10(frequency / 1e6)

def hata_model(distance, frequency, height_transmitter, height_receiver):
    """
    Calculate path loss using the Hata model.

    Parameters:
    - distance (float): Distance between transmitter and receiver (in km).
    - frequency (float): Frequency of the signal (in Hz).
    - height_transmitter (float): Height of the transmitter (in meters).
    - height_receiver (float): Height of the receiver (in meters).

    Returns:
    - float: Path loss (in dB).
    """
    C1 = 69.55
    C2 = 26.16
    C3 = 13.82
    C4 = 4.97
    C5 = 0.38
    C6 = 0.1

    path_loss = (C1 + C2 * np.log10(distance) + C3 * np.log10(frequency / 1e6)
                - C4 + (C5 + C6 * np.log10(frequency / 1e6)) *
                np.log10(height_transmitter * height_receiver))
    return path_loss

def ccir_model(distance, frequency):
    """
    Calculate path loss using the CCIR model.

    Parameters:
    - distance (float): Distance between transmitter and receiver (in km).
    - frequency (float): Frequency of the signal (in Hz).

    Returns:
    - float: Path loss (in dB).
    """
    return 36.6 * np.log10(distance) + 22.8 * np.log10(frequency) + 27.2

# Function to update formula label

def update_formula_label(event):
    """
    Update the formula label based on the selected propagation model.

    Parameters:
    - event: Event object.
    """
    selected_model = model_combo.get()
    if selected_model != "Select a model":
        if selected_model == "Free Space Propagation Model":
            formula_label.config(text="Path Loss (dB) = 20 × log₁₀(distance) + 20 × log₁₀(frequency) − 147.55")
        elif selected_model == "2-ray Ground Reflection Model":
            formula_label.config(text="Path Loss (dB) = 10 × log₁₀((λ / (4 × π × d₁ × d₂))²)")
        elif selected_model == "Okumura":
            formula_label.config(text="Path Loss (dB) = 69.55 + 26.16 × log₁₀(distance) + 20 × log₁₀(frequency / 1e6)")
        elif selected_model == "Hata":
            formula_label.config(text="Path Loss (dB) = C₁ + C₂ × log₁₀(distance) + C₃ × log₁₀(frequency / 1e6) − C₄ + (C₅ + C₆ × log₁₀(frequency / 1e6)) × log₁₀(height_transmitter × height_receiver)")
        elif selected_model == "CCIR":
            formula_label.config(text="Path Loss (dB) = 36.6 × log₁₀(distance) + 22.8 × log₁₀(frequency) + 27.2")
    else:
        formula_label.config(text="Please select a propagation model.")

# Function to calculate and plot

def calculate_and_plot():
    """
    Calculate path loss based on selected parameters and plot the results.
    """
    distance = np.linspace(1, 10, 1000)  # distances from 1 to 10 km
    frequency = float(frequency_entry.get()) * 1e6  # MHz to Hz
    height_transmitter = float(height_transmitter_entry.get())
    height_receiver = float(height_receiver_entry.get())

    selected_model = model_combo.get()
    ax.clear()  # Clear previous plot

    if selected_model == "Free Space Propagation Model":
        path_loss = free_space_model(distance, frequency)
    elif selected_model == "2-ray Ground Reflection Model":
        path_loss = two_ray_ground_model(distance, frequency, height_transmitter, height_receiver)
    elif selected_model == "Okumura":
        path_loss = okumura_model(distance, frequency)
    elif selected_model == "Hata":
        path_loss = hata_model(distance, frequency, height_transmitter, height_receiver)
    elif selected_model == "CCIR":
        path_loss = ccir_model(distance, frequency)

    ax.plot(distance, path_loss)
    ax.set_title("Propagation Model - {}".format(selected_model))
    ax.set_xlabel("Distance (km)")
    ax.set_ylabel("Path Loss (dB)")
    ax.grid(True)
    canvas.draw()

# Function to open the PDF file

def open_pdf():
    """
    Open a PDF file containing propagation model information.
    """
    webbrowser.open("5_Propagation_1_HMMY_STR.pdf")

# Function to open the Help tab and take focus

def open_help():
    """
    Open the Help tab and take focus.
    """
    tabs = notebook.tabs()
    if "Help" not in tabs:
        help_tab = ttk.Frame(notebook)
        notebook.add(help_tab, text="Help")

        help_text = tk.Text(help_tab, wrap="word", font=("Arial", 12), spacing1=10)
        help_text.pack(fill="both", expand=True, padx=10, pady=10)

        formulas = {
            "Free Space Propagation Model": "Path Loss (dB) = 20 × log₁₀(distance) + 20 × log₁₀(frequency) − 147.55",
            "2-ray Ground Reflection Model": "Path Loss (dB) = 10 × log₁₀((λ / (4 × π × d₁ × d₂))²)",
            "Okumura": "Path Loss (dB) = 69.55 + 26.16 × log₁₀(distance) + 20 × log₁₀(frequency / 1e6)",
            "Hata": "Path Loss (dB) = C₁ + C₂ × log₁₀(distance) + C₃ × log₁₀(frequency / 1e6) − C₄ + (C₅ + C₆ × log₁₀(frequency / 1e6)) × log₁₀(height_transmitter × height_receiver)",
            "CCIR": "Path Loss (dB) = 36.6 × log₁₀(distance) + 22.8 × log₁₀(frequency) + 27.2"
        }

        for model, formula in formulas.items():
            help_text.insert("end", f"<b>{model}:</b>\n{formula}\n\n", "bold")

        help_text.tag_configure("bold", font=("Arial", 12, "bold"))
        help_text.config(state="disabled")
        notebook.select(help_tab)

# Create main application window

root = tk.Tk()
root.title("Propagation Model Calculator")
root.configure(bg="#f0f0f0")  # Set background color

# Create color palette
style = ttk.Style(root)
style.theme_use("clam")

# Create decoration frame
decoration_frame = tk.Frame(root, bg="#ccc", padx=10, pady=10)
decoration_frame.pack(fill=tk.BOTH, expand=True)

# Create input frame
input_frame = ttk.Frame(decoration_frame, padding="20", borderwidth=2, relief="groove")
input_frame.pack(side=tk.LEFT)

frequency_label = ttk.Label(input_frame, text="Frequency (MHz):")
frequency_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")
frequency_entry = ttk.Entry(input_frame)
frequency_entry.grid(row=0, column=1, padx=5, pady=5)

height_transmitter_label = ttk.Label(input_frame, text="Height Transmitter (m):")
height_transmitter_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")
height_transmitter_entry = ttk.Entry(input_frame)
height_transmitter_entry.grid(row=1, column=1, padx=5, pady=5)

height_receiver_label = ttk.Label(input_frame, text="Height Receiver (m):")
height_receiver_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")
height_receiver_entry = ttk.Entry(input_frame)
height_receiver_entry.grid(row=2, column=1, padx=5, pady=5)

model_label = ttk.Label(input_frame, text="Select Propagation Model:", font=("Helvetica", 10, "bold"))
model_label.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky="w")

models = [
    "Select a model",
    "Free Space Propagation Model",
    "2-ray Ground Reflection Model",
    "Okumura",
    "Hata",
    "CCIR",
]
max_model_length = max(len(model) for model in models)
model_combo = ttk.Combobox(input_frame, values=models, state="readonly", width=max_model_length+2)
model_combo.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
model_combo.current(0)

calculate_button = ttk.Button(input_frame, text="Calculate and Plot", command=calculate_and_plot)
calculate_button.grid(row=5, columnspan=2, padx=5, pady=5)

notebook = ttk.Notebook(decoration_frame)
notebook.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

style = ttk.Style()
style.configure('TNotebook.Tab', padding=[30, 10])
style.map('TNotebook.Tab', padding=[('selected', [30, 10])])

plot_frame = ttk.Frame(notebook)
notebook.add(plot_frame, text="Plot")

fig, ax = plt.subplots(figsize=(8, 4))
ax.set_facecolor('#ffffff')
canvas = FigureCanvasTkAgg(fig, master=plot_frame)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack(fill=tk.BOTH, expand=True)

formula_frame = tk.Frame(root, bg="#f0f0f0", bd=1, relief=tk.RIDGE)
formula_frame.pack(fill=tk.X)

formula_label = tk.Label(formula_frame, text="Formula:", font=("Helvetica", 12, "bold"), bg="#f0f0f0")
formula_label.pack(pady=(5, 0))

model_combo.bind("<<ComboboxSelected>>", update_formula_label)

help_button = ttk.Button(root, text="Help", command=open_help)
help_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="sw")

pdf_button = ttk.Button(root, text="PDF", command=open_pdf)
pdf_button.pack(side=tk.LEFT, padx=10, pady=10, anchor="sw")

root.mainloop()
