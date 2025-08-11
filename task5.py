from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import tkinter as tk
import io

IMAGE_RES = 256

LEFT = 0
UP = 1
RIGHT = 2
DOWN = 3

coordinates = [0,0]

#Function to mirror image
def createInvertedImage(PILImage, ax):
    pixel_array = np.array(PILImage)
    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
    x_flat = x_coords.flatten() + coordinates[0]
    y_flat = y_coords.flatten() + coordinates[1] - IMAGE_RES//2

    colours = pixel_array.reshape(-1, 4) / 255

    #Negating all x values to flip image
    neg_x_flat = -1*x_flat

    #Clear axes, set x and y limits, plot original and inverted image, then invert the y-axis
    ax.clear()
    ax.set_xlim(-IMAGE_RES, IMAGE_RES)
    ax.set_ylim(-IMAGE_RES, IMAGE_RES)
    ax.scatter(neg_x_flat, y_flat, c=colours, marker='s', s=0.75)
    ax.scatter(x_flat, y_flat, c=colours, marker='s', s=0.75)
    ax.invert_yaxis()

def moveImage(noPixels, direction, event):
    #Switch statement to deal with moving image, based on direction
    match direction:
        case 0:
            if coordinates[0] > -64:
                coordinates[0] -= noPixels
        case 1:
            coordinates[1] -= noPixels
        case 2:
            coordinates[0] += noPixels
        case 3:
            coordinates[1] += noPixels

    createInvertedImage(picture, ax)
    canvas.draw()

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

window = tk.Tk()
window.title("Image")

#Create initial image to be displayed in window
picture = createPILImage("sheldon.png")

figure = Figure(figsize=(8,8))
ax = figure.add_subplot(111)

createInvertedImage(picture, ax)

canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

#Event handling for key presses to move image
window.bind("<Left>", lambda event:moveImage(IMAGE_RES//16, LEFT, event))
window.bind("<Right>", lambda event:moveImage(IMAGE_RES//16, RIGHT, event))
window.bind("<Down>", lambda event:moveImage(IMAGE_RES//16, DOWN, event))
window.bind("<Up>", lambda event:moveImage(IMAGE_RES//16, UP, event))

window.mainloop()