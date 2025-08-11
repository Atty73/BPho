from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

IMAGE_RES = 512

def plotImage(PILImage):
    pixel_array = np.array(PILImage)
    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()

    colours = pixel_array.reshape(-1, 3) / 255

    ax.scatter(x_flat, y_flat, c=colours, marker='s', s=1)
    ax.invert_yaxis()

def createPILImage(picture):
    #Convert png into PIL image, and resize to a 1:1 image of IMAGE_RES resolution
    img = Image.open(picture).convert('RGB')
    img = img.resize((IMAGE_RES, IMAGE_RES))

    #Create a blank canvas of size of image
    canvas_size = img.size
    background = Image.new('RGB', canvas_size, 'white')

    #Shrink image to be half of original size
    new_size = (img.width // 2, img.height // 2)
    shrunken_image = img.resize(new_size, Image.LANCZOS)

    #Centre image in middle of canvas
    x_offset = (canvas_size[0] - new_size[0]) // 2
    y_offset = (canvas_size[1] - new_size[1]) // 2

    #Place shrunken image on top of canvas
    background.paste(shrunken_image, (x_offset, y_offset))

    return background


fig, ax = plt.subplots(figsize=(8, 8))

picture = createPILImage("sheldon.png")
plotImage(picture)

radius = np.sqrt(2 * ((IMAGE_RES)/4)**2)

circle = Circle((256,256), radius=radius, edgecolor='red', facecolor='none', linewidth=5)
ax.add_patch(circle)

plt.show()