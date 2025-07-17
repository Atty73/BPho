from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

img = Image.open("sheldon.png").convert('RGB')
pixel_array = np.array(img)

inverse_pixel_array = np.array(img)

for i in range(len(pixel_array)):
    print(inverse_pixel_array[-(i+1)])
    print(pixel_array[0])
    #inverse_pixel_array[:, [0, i]] = pixel_array[:, [i, 0]]
    inverse_pixel_array = pixel_array[:, ::-1]

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
#plt.axis('off')
plt.show()