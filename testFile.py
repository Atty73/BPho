from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

def invertImage(picture):
    img = Image.open(picture).convert('RGB')
    pixel_array = np.array(img)

    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()
    colors = pixel_array.reshape(-1, 3) / 255

    neg_x_flat = -1*x_flat

    plt.figure(figsize=(16, 8))
    plt.scatter(x_flat, y_flat, c=colors, marker='s', s=1)
    plt.scatter(neg_x_flat, y_flat, c=colors, marker='s', s=1)
    plt.gca().invert_yaxis()

    newFilename = "matplotlib" + picture
    plt.savefig(newFilename)
    return newFilename

window = tk.Tk()
window.title("Image")

imageFilename = invertImage("sheldon.png")

image = Image.open(imageFilename)
image = ImageTk.PhotoImage(image)

image_label = tk.Label(window, image=image)
image_label.pack()

window.mainloop()