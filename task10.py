from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Circle

IMAGE_RES = 512
RADIUS = np.sqrt(2 * ((IMAGE_RES)/4)**2)
ARC_DEG = 360
Rf = 500

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

def anamorphicTransformation(PILImage, ax):
    global RADIUS

    pixel_array = np.array(PILImage)
    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()

    r = 62 + (Rf) * (1 - y_flat / height)

    ARC_DEG_radians = np.deg2rad(ARC_DEG*2)

    start_angle = -np.pi / 2 - ARC_DEG_radians / 2
    theta = start_angle + (x_flat / width) * ARC_DEG_radians

    new_x_flat = r * np.cos(theta)
    new_y_flat = r * np.sin(theta)

    colours = pixel_array.reshape(-1, 4) / 255

    ax.clear()
    ax.set_xlim(-IMAGE_RES, IMAGE_RES)
    ax.set_ylim(-IMAGE_RES, IMAGE_RES)
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)
    ax.scatter(new_x_flat, new_y_flat, c=colours, marker='s', s=10)
    ax.scatter(x_flat-256, -y_flat+256, c=colours, marker='s', s=1)

def polarAnamorphicTransformation(PILImage, ax):

    pixel_array = np.array(PILImage)
    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))
    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()
    colours = pixel_array.reshape(-1, 4) / 255

    Rf = 600
    angle_span_deg = 720

    r = 200 + (Rf) * (1 - y_flat / height)

    # 2. Map the x-coordinate to the angle (theta)
    # We linearly map [0, width] to the desired angle span in radians
    angle_span_rad = np.deg2rad(angle_span_deg)
    # We center the angle span around the -90 degree mark (pointing down)
    start_angle = -np.pi/2 - angle_span_rad / 2
    theta = start_angle + (x_flat / width) * angle_span_rad

    print(width,height)

    # 3. Convert polar coordinates (r, theta) back to Cartesian (x, y) for plotting
    new_x = r * np.cos(theta)
    new_y = r * np.sin(theta)

    # --- Plotting ---
    ax.clear()
    ax.set_aspect('equal', adjustable='box') # Ensure the arc isn't squashed
    ax.set_xlim(-1000, 1000)
    ax.set_ylim(-1000, 1000)
    ax.grid(True, alpha=0.6)
    ax.set_axisbelow(True)

    # Plot the transformed "arc" image
    ax.scatter(new_x, new_y, c=colours, marker='s', s=5)

    # Plot the original image in a circle at the top for comparison (like the cat image)
    # This is an approximation. For an exact replica, you'd plot on a different axis.
    circle_radius = 150
    ax.scatter(x_flat-256, -y_flat+256, c=colours, marker='s', s=1)


fig, ax = plt.subplots(figsize=(8, 8))

picture = createPILImage("sheldon.png")
anamorphicTransformation(picture, ax)

circle = Circle((0,0), radius=RADIUS, edgecolor='black', facecolor='none', linewidth=4)
ax.add_patch(circle)

plt.show()