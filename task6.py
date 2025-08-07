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

focal_length = 100  # in arbitrary units
object_distance = 200  # > focal_length


def compute_image_params(d_o, f):
    d_i = 1 / (1/f - 1/d_o)
    M = -d_i / d_o
    return d_i, M

#simulate the lens
def simulateLens(PILImage, d_o, f):
    d_i, M = compute_image_params(d_o, f)

    # Resize according to magnification
    width, height = PILImage.size
    new_size = (int(abs(M) * width), int(abs(M) * height))
    transformed_image = PILImage.resize(new_size, Image.LANCZOS)

    # Flip vertically for real inverted image
    transformed_image = transformed_image.transpose(Image.FLIP_TOP_BOTTOM)

    # Paste image on canvas (to represent screen)
    canvas = Image.new('RGB', (IMAGE_RES, IMAGE_RES), 'white')
    x_offset = (IMAGE_RES - new_size[0]) // 2
    y_offset = (IMAGE_RES - new_size[1]) // 2

    canvas.paste(transformed_image, (x_offset, y_offset))

    return canvas


#Function to mirror image
def invertImage(PILImage):
    pixel_array = np.array(PILImage)

    height, width, _ = pixel_array.shape

    x_coords, y_coords = np.meshgrid(np.arange(width), np.arange(height))

    x_flat = x_coords.flatten()
    y_flat = y_coords.flatten()
    colors = pixel_array.reshape(-1, 3) / 255

    #Negating all x values to flip image
    neg_x_flat = -1*x_flat

    #Plot image correct way around, and the flipped image; y-axis inverted because images mapped from origin at top-left
    plt.figure(figsize=(16, 8))
    plt.scatter(x_flat, y_flat, c=colors, marker='s', s=1)
    plt.scatter(neg_x_flat, y_flat, c=colors, marker='s', s=1)
    plt.gca().invert_yaxis()

    #Save to a buffer in memory
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()

    buffer.seek(0)
    return Image.open(buffer)

#Function to move image
def moveImage(noPixels, direction, event):
    global picture
    global coordinates

    cut_off = np.array([[[]]])

    #Convert picture into numpy array
    pixel_array = np.array(picture)

    #Switch statement to deal with moving image, based on direction
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

    #Convert numpy array back into PIL image
    picture = Image.fromarray(pixel_array)

    #Call invertImage to create matplotlib plot of inverted image against axes and then call updateWindow to display new plot in window
    invertedImage = invertImage(picture)
    updateWindow()

#Function to convert png file into a PIL image, then make it smaller
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

#Function to update the image shown in the window
def updateWindow():
    global picture
    d_o = object_distance_var.get()
    f = focal_length_var.get()
    simulated = simulateLens(picture, d_o, f)

    # If you still want to show mirrored version too:
    image = invertImage(simulated)

    img_tk = ImageTk.PhotoImage(image)
    image_label.config(image=img_tk)
    image_label.image = img_tk



window = tk.Tk()
window.title("Image")

focal_length_var = tk.IntVar(value=100)
object_distance_var = tk.IntVar(value=200)

#Create initial image to be displayed in window
picture = createPILImage("peterbot.png")
initialImage = invertImage(picture)
coordinates = [0,0]

#Display initial image
img_tk = ImageTk.PhotoImage(initialImage)
image_label = tk.Label(window, image=img_tk)
image_label.image = img_tk
image_label.pack()

#Event handling for key presses to move image
window.bind("<Left>", lambda event:moveImage(20, left, event))
window.bind("<Right>", lambda event:moveImage(20, right, event))
window.bind("<Down>", lambda event:moveImage(20, down, event))
window.bind("<Up>", lambda event:moveImage(20, up, event))

slider_frame = tk.Frame(window)
slider_frame.pack()

tk.Label(slider_frame, text="Object Distance").pack()
tk.Scale(slider_frame, from_=focal_length+1, to=500, variable=object_distance,
         orient='horizontal', command=lambda e: updateWindow()).pack()

tk.Label(slider_frame, text="Focal Length").pack()
tk.Scale(slider_frame, from_=10, to=200, variable=focal_length_var,
         orient='horizontal', command=lambda e: updateWindow()).pack()


window.mainloop()