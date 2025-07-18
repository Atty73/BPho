from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk
import io

IMAGE_RES = 256

left = 0
up = 1
right = 2
down = 3


# Function to mirror image
def invertImage(PILImage):
    pixel_array = np.array(PILImage)

    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()
    colors = pixel_array.reshape(-1, 3) / 255

    # Negating all x values to flip image
    neg_x_flat = -1 * x_flat

    # Plot image correct way around, and the flipped image; y-axis inverted because images mapped from origin at top-left
    plt.figure(figsize=(16, 8))
    plt.scatter(x_flat, y_flat, c=colors, marker='s', s=1)
    plt.scatter(neg_x_flat, y_flat, c=colors, marker='s', s=1)
    plt.gca().invert_yaxis()

    # Save to a buffer in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    return Image.open(buffer)


# Function to move image
def moveImage(noPixels, direction, event):
    global picture
    global coordinates

    cut_off = np.array([[[]]])

    # Convert picture into numpy array
    pixel_array = np.array(picture)

    # Switch statement to deal with moving image, based on direction
    match direction:
        case 0:
            pixel_array = np.roll(pixel_array, shift=-noPixels, axis=1)
            for i in range(1, noPixels + 1):
                pixel_array[:, -i] = [255, 255, 255]

        case 1:
            pixel_array = np.roll(pixel_array, shift=-noPixels, axis=0)
            for i in range(1, noPixels + 1):
                pixel_array[-i] = [255, 255, 255]
        case 2:
            pixel_array = np.roll(pixel_array, shift=noPixels, axis=1)
            for i in range(0, noPixels):
                pixel_array[:, -i] = [255, 255, 255]
        case 3:
            pixel_array = np.roll(pixel_array, shift=noPixels, axis=0)
            for i in range(0, noPixels):
                pixel_array[i] = [255, 255, 255]

    # Convert numpy array back into PIL image
    picture = Image.fromarray(pixel_array)

    # Call invertImage to create matplotlib plot of inverted image against axes and then call updateWindow to display new plot in window
    invertedImage = invertImage(picture)
    updateWindow(invertedImage)


# Function to convert png file into a PIL image, then make it smaller
def createPILImage(picture):
    # Convert png into PIL image, and resize to a 1:1 image of IMAGE_RES resolution
    img = Image.open(picture).convert('RGB')
    img = img.resize((IMAGE_RES, IMAGE_RES))

    # Create a blank canvas of size of image
    canvas_size = img.size
    background = Image.new('RGB', canvas_size, 'white')

    # Shrink image to be half of original size
    new_size = (img.width // 2, img.height // 2)
    shrunken_image = img.resize(new_size, Image.LANCZOS)

    # Centre image in middle of canvas
    x_offset = (canvas_size[0] - new_size[0]) // 2
    y_offset = (canvas_size[1] - new_size[1]) // 2

    # Place shrunken image on top of canvas
    background.paste(shrunken_image, (x_offset, y_offset))

    return background


# Function to update the image shown in the window
def updateWindow(PILImage):
    # Convert PILImage into tkinter image
    image = ImageTk.PhotoImage(PILImage)

    # Update image in window
    image_label.config(image=image)
    image_label.image = image


window = tk.Tk()
window.title("Image")

# Create initial image to be displayed in window
picture = createPILImage("peterbot.png")
initialImage = invertImage(picture)
coordinates = [0, 0]

# Display initial image
img_tk = ImageTk.PhotoImage(initialImage)
image_label = tk.Label(window, image=img_tk)
image_label.image = img_tk
image_label.pack()

# Event handling for key presses to move image
window.bind("<Left>", lambda event: moveImage(20, left, event))
window.bind("<Right>", lambda event: moveImage(20, right, event))
window.bind("<Down>", lambda event: moveImage(20, down, event))
window.bind("<Up>", lambda event: moveImage(20, up, event))

window.mainloop()