from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse

canvas = None
ax = None

IMAGE_RES = 256
f = IMAGE_RES * 4

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

coordinates = [0,0]

#Function to convert png file into a PIL image, then make it smaller
def createPILImage(picture):
    #Convert png into PIL image, and resize to a 1:1 image of IMAGE_RES resolution
    img = Image.open(picture).convert('RGB')
    img = img.resize((IMAGE_RES, IMAGE_RES))

    #Create a blank canvas of size of image
    canvas_size = img.size
    background = Image.new('RGBA', canvas_size, (255,255,255,0))

    #Shrink image to be half of original size
    new_size = (img.width // 2, img.height // 2)
    shrunken_image = img.resize(new_size, Image.LANCZOS)

    #Centre image in middle of canvas
    x_offset = (canvas_size[0] - new_size[0]) // 2
    y_offset = (canvas_size[1] - new_size[1]) // 2

    #Place shrunken image on top of canvas
    background.paste(shrunken_image, (x_offset, y_offset))

    return background

#Function to calculate new X coordinate
def calcNewX(x):
    denominator = x-f
    newX = abs((f/denominator)*x)
    return newX

#Function to calculate new Y coordinate
def calcNewY(x, y, X):
    newY = (y/x)*X
    return newY

def createVirtualEnlargedImage(PILImage, ax):
    pixel_array = np.array(PILImage)
    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
    x_flat = x_coords.flatten() + coordinates[0] + IMAGE_RES
    y_flat = y_coords.flatten() + coordinates[1] - IMAGE_RES // 2

    new_x_flat = x_flat.copy()
    new_y_flat = y_flat.copy()

    new_pixel_array = pixel_array.copy()

    for i in range(len(x_flat)):
        if 0 < x_flat[i] < f:
            new_x_flat[i] = calcNewX(x_flat[i])
            new_y_flat[i] = calcNewY(x_flat[i], y_flat[i], new_x_flat[i])

    colours = new_pixel_array.reshape(-1, 4) / 255

    ax.clear()
    ax.set_xlim(-2 * IMAGE_RES, IMAGE_RES*3)
    ax.set_ylim(-2 * IMAGE_RES, IMAGE_RES*3)
    ax.scatter(new_x_flat, new_y_flat, c=colours, marker='s', s=1)
    ax.scatter(x_flat, y_flat, c=colours, marker='s', s=1)
    ax.invert_yaxis()

def moveImage(noPixels, direction, event):
    #Switch statement to deal with moving image, based on direction
    match direction:
        case 0:
            coordinates[0] -= noPixels
        case 1:
            coordinates[1] -= noPixels
        case 2:
            coordinates[0] += noPixels
        case 3:
            coordinates[1] += noPixels

    #Call invertImage to create matplotlib plot of inverted image against axes and then call updateWindow to display new plot in window
    createVirtualEnlargedImage(picture, ax)

    lens = Ellipse(xy=(0, 0), width=25, height=125, linewidth=2, facecolor='none', edgecolor='red')
    ax.add_patch(lens)

    canvas.draw()

window = tk.Tk()
window.title("Thin Lens Simulation")

picture = createPILImage("sheldon.png")

figure = Figure(figsize=(8, 8))
ax = figure.add_subplot(111)

createVirtualEnlargedImage(picture, ax)

lens = Ellipse(xy=(0, 0), width=25, height=125, linewidth=2, facecolor='none', edgecolor='red')
ax.add_patch(lens)

canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#Event handling for key presses to move image
window.bind("<Left>", lambda event:moveImage(IMAGE_RES//16, LEFT, event))
window.bind("<Right>", lambda event:moveImage(IMAGE_RES//16, RIGHT, event))
window.bind("<Down>", lambda event:moveImage(IMAGE_RES//16, DOWN, event))
window.bind("<Up>", lambda event:moveImage(IMAGE_RES//16, UP, event))

window.mainloop()