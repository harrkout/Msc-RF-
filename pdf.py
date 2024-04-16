import fitz
from tkinter import *
from PIL import Image, ImageTk

# Open PDF file
file_name = "5_Propagation_1_HMMY_STR.pdf"
doc = fitz.open(file_name)

# Transformation matrix we can apply on pages
zoom = 1
mat = fitz.Matrix(zoom, zoom)

# Count number of pages
num_pages = len(doc)

# Initialize and set screen size
root = Tk()
root.geometry('800x700')

# Initialize list to hold canvas objects for each page
page_canvases = []

# Define a function to create a canvas for each page
def create_page_canvas(page_num):
    # Load the page and convert it to an image
    page = doc.load_page(page_num)
    im = pdf_to_img(page_num)
    img_tk = ImageTk.PhotoImage(im)
    
    # Create a canvas for the image
    canvas = Canvas(canvas_frame)
    canvas.create_image(0, 0, anchor='nw', image=img_tk)
    canvas.config(width=im.width, height=im.height)
    canvas.img_tk = img_tk
    canvas.pack(side=TOP, fill=BOTH, expand=YES)
    
    return canvas

# Define a function to convert PDF page to image
def pdf_to_img(page_num):
    page = doc.load_page(page_num)
    pix = page.get_pixmap(matrix=mat)
    return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

# Create a canvas frame to hold the canvases
canvas_frame = Frame(root)
canvas_frame.pack(side=TOP, fill=BOTH, expand=YES)

# Create a canvas for each page and add it to the list
for i in range(num_pages):
    canvas = create_page_canvas(i)
    page_canvases.append(canvas)

# Add a vertical scrollbar
scrollbar = Scrollbar(root, orient=VERTICAL)
scrollbar.pack(side=RIGHT, fill=Y)

# Create a canvas to attach the scrollbar
canvas = Canvas(root, yscrollcommand=scrollbar.set)
canvas.pack(side=LEFT, fill=BOTH, expand=YES)

# Configure scrollbar
scrollbar.config(command=canvas.yview)

# Attach canvas frame to the scrollable canvas
canvas.create_window((0, 0), window=canvas_frame, anchor='nw')

# Set visual locations for entry and button
entry = Entry(root)
entry.pack(side=TOP, fill=X)
button = Button(root, text="Go to Page", command=lambda: show_page(int(entry.get()) - 1))
button.pack(side=TOP, fill=X)

# Define a function to show the selected page
def show_page(page_num):
    for canvas in page_canvases:
        canvas.pack_forget()
    page_canvases[page_num].pack(side=TOP, fill=BOTH, expand=YES)

# Start the Tkinter main loop
root.mainloop()

# Close the PDF document
doc.close()
