from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

canvas = None
ax = None

IMAGE_RES = 256
R = 200

# Set the mirror's radius and focal length
f = -R / 2  # Focal length for a convex mirror

# Coordinates of the object's top-left corner relative to the mirror's origin (0,0)
object_coordinates = [250, -128]  # Start object outside the mirror's view


# Function to create a PIL image and prepare it for processing
def createPILImage(picture):
    img = Image.open(picture).convert('RGB')
    return img.resize((IMAGE_RES, IMAGE_RES))


def createVirtualConvexMirrorImage(pil_image, ax):
    pixel_array = np.array(pil_image)
    height, width, _ = pixel_array.shape

    # Create object coordinates relative to the center of the mirror
    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

    # Calculate absolute object coordinates based on the top-left corner
    x_object = x_coords + object_coordinates[0]
    y_object = y_coords + object_coordinates[1]

    x_flat = x_object.flatten()
    y_flat = y_object.flatten()

    # Initialize arrays for the new pixel positions
    new_x_flat = np.zeros_like(x_flat, dtype=float)
    new_y_flat = np.zeros_like(y_flat, dtype=float)

    # Perform the transformation for each pixel
    for i in range(len(x_flat)):
        do = x_flat[i]

        # Only process pixels in front of the mirror (where do > 0)
        if do > 0:
            # Calculate image distance using the mirror equation
            di = (do * f) / (do - f)

            # Calculate magnification
            M = -di / do

            # Calculate the new coordinates for the virtual image
            new_x_flat[i] = di
            new_y_flat[i] = M * y_flat[i]
        else:
            # Pixels behind the mirror are not visible, so mark them for removal
            new_x_flat[i] = np.nan
            new_y_flat[i] = np.nan

        # Filter out invalid (NaN) points before plotting
    valid_indices = ~np.isnan(new_x_flat)

    ax.clear()
    ax.set_xlim(-IMAGE_RES, IMAGE_RES)
    ax.set_ylim(-IMAGE_RES, IMAGE_RES)
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)

    # Draw the convex mirror as a curve
    theta = np.linspace(-np.pi / 2, np.pi / 2, 100)
    mirror_x = -R * np.cos(theta)
    mirror_y = R * np.sin(theta)
    ax.plot(mirror_x, mirror_y, color='blue', linewidth=2)

    # Plot the virtual image pixels
    colours = pixel_array.reshape(-1, 3)[valid_indices] / 255
    ax.scatter(new_x_flat[valid_indices], new_y_flat[valid_indices], c=colours, marker='s', s=1)

    # === ADDED CODE: Plot the original object pixels ===
    object_colors = pixel_array.reshape(-1, 3) / 255
    ax.scatter(x_flat, y_flat, c=object_colors, marker='s', s=1)
    # ===================================================

    ax.set_aspect('equal', adjustable='box')
    ax.invert_yaxis()


def moveImage(noPixels, direction, event):
    match direction:
        case 0:  # LEFT
            object_coordinates[0] -= noPixels
        case 1:  # UP
            object_coordinates[1] -= noPixels
        case 2:  # RIGHT
            object_coordinates[0] += noPixels
        case 3:  # DOWN
            object_coordinates[1] += noPixels

    createVirtualConvexMirrorImage(picture, ax)
    canvas.draw()


# Setup the main window and plotting area
window = tk.Tk()
window.title("Convex Mirror Simulation")

picture = createPILImage("sheldon.png")

figure = Figure(figsize=(8, 8))
ax = figure.add_subplot(111)

createVirtualConvexMirrorImage(picture, ax)

canvas = FigureCanvasTkAgg(figure, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# Event handling for key presses
window.bind("<Left>", lambda event: moveImage(IMAGE_RES // 16, 0, event))
window.bind("<Right>", lambda event: moveImage(IMAGE_RES // 16, 2, event))
window.bind("<Up>", lambda event: moveImage(IMAGE_RES // 16, 1, event))
window.bind("<Down>", lambda event: moveImage(IMAGE_RES // 16, 3, event))

window.mainloop()