from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import functions as f
import math

img = Image.open("sheldon.png").convert('RGB')
pixel_array = np.array(img)

for i in range(len(pixel_array)):
    for j in range(len(pixel_array)):
        R = pixel_array[i][j][0]/255
        G = pixel_array[i][j][1]/255
        B = pixel_array[i][j][2]/255
        plt.scatter(j,i,color=(R,G,B),marker='s',s=100)

        print(f"Pixel {i},{j}")

plt.gca().invert_yaxis()
plt.show()