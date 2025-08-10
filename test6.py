import tkinter as tk
from tkinter import ttk
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse

# === Load and prepare object image ===
img = Image.open("sheldon.png").resize((80, 80))
img_arr = np.array(img)

# === Optical parameters ===
focal_length = 1.0
object_x = -2.0
object_y = -1.0

# === Compute image position and magnification ===
def compute_image_pos(d_o, f):
    try:
        d_i = 1 / (1/f - 1/d_o)
    except ZeroDivisionError:
        d_i = 1e6
    M = -d_i / d_o
    return d_i, M

# === Redraw everything ===
def draw_scene():
    ax.clear()
    ax.set_xlim(-4, 4)
    ax.set_ylim(-2, 2)
    ax.invert_yaxis()
    ax.set_aspect('equal')
    ax.set_title("Thin Lens Simulation")
    ax.set_xlabel("x")
    ax.grid(True)

    # Lens
    lens = Ellipse((0, 0), width=0.1, height=3.0, edgecolor='blue', facecolor='none', linewidth=2)
    ax.add_patch(lens)
    ax.plot([focal_length, -focal_length], [0, 0], 'b*', markersize=15)

    # Object
    d_o = abs(object_x)
    d_i, M = compute_image_pos(d_o, focal_length)
    image_x = d_i
    image_y = M * object_yc

    # Draw object image
    extent_obj = [object_x - 0.4, object_x + 0.4, object_y - 0.6, object_y + 0.6]
    ax.imshow(img_arr, cmap='gray', extent=extent_obj, origin='lower', zorder=5)
    ax.plot(object_x, object_y, 'g*', markersize=10)
    ax.text(object_x, object_y - 0.3, "(X, Y)", fontsize=10)

    # Draw image (inverted)
    img_inv = np.flipud(img_arr)
    width = 0.8 * abs(M)
    height = 1.2 * abs(M)
    extent_img = [image_x - width/2, image_x + width/2, image_y - height/2, image_y + height/2]
    ax.imshow(img_inv, cmap='gray', extent=extent_img, origin='lower', zorder=5)
    ax.plot(image_x, image_y, 'r*', markersize=10)
    ax.text(image_x, image_y + 0.3, "(x, y)", fontsize=10)

    # Ray 1: parallel → through focus
    ax.plot([object_x, 0], [object_y, object_y], 'r')
    ax.plot([0, image_x], [object_y, image_y], 'r')

    # Ray 2: through center
    ax.plot([object_x, image_x], [object_y, image_y], 'r')
    ax.text(0.4, 0.2, "Ray Optics", rotation=-15, fontsize=9)

    canvas.draw()

# === Key event handler ===
def on_key(event):
    global object_x, object_y
    if event.keysym == 'Left':
        object_x -= 0.2
    elif event.keysym == 'Right':
        object_x += 0.2
    elif event.keysym == 'Up':
        object_y += 0.2
    elif event.keysym == 'Down':
        object_y -= 0.2
    draw_scene()

# === Tkinter GUI Setup ===
root = tk.Tk()
root.title("Interactive Lens Simulation")

frame = ttk.Frame(root)
frame.pack()

# Embed matplotlib figure
fig, ax = plt.subplots(figsize=(8, 5))
canvas = FigureCanvasTkAgg(fig, master=frame)
canvas.get_tk_widget().pack()
draw_scene()

# Bind keyboard events
root.bind('<Left>', on_key)
root.bind('<Right>', on_key)
root.bind('<Up>', on_key)
root.bind('<Down>', on_key)

root.mainloop()
