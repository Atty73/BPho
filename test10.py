from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle

IMAGE_RES = 512
ARC_DEG = 160  # arc extent in degrees
RF = 3  # radius factor for the arc mapping


def createPILImage(picture):
    img = Image.open(picture).convert('RGB')
    img = img.resize((IMAGE_RES, IMAGE_RES))
    return img


def anamorphic_transform(img, arc_deg=160, Rf=3):
    pixel_array = np.array(img)
    height, width, _ = pixel_array.shape

    # Normalized coordinates (-1 to 1)
    x_coords = np.linspace(-1, 1, width)
    y_coords = np.linspace(-1, 1, height)
    xv, yv = np.meshgrid(x_coords, y_coords)

    # Polar coords
    r = np.sqrt(xv ** 2 + yv ** 2)
    theta = np.arctan2(yv, xv)

    # Mask: unit circle only
    mask = r <= 1

    # Map theta from [-pi, pi] to arc range (centered horizontally)
    arc_theta = (theta / np.pi) * (arc_deg / 2)
    arc_theta_rad = np.deg2rad(arc_theta)

    # Flip radius for inversion effect
    new_r = Rf + r * (Rf)

    # Cartesian coordinates of transformed pixels
    X = new_r * np.sin(arc_theta_rad)
    Y = -new_r * np.cos(arc_theta_rad)

    colours = pixel_array.reshape(-1, 3) / 255.0
    return xv[mask], yv[mask], X[mask], Y[mask], colours[mask.flatten()]


# Load image
picture = createPILImage("sheldon.png")

# Get original and transformed coordinates
x_orig, y_orig, X_arc, Y_arc, colours = anamorphic_transform(picture, ARC_DEG, RF)

# Plot
fig, ax = plt.subplots(figsize=(8, 8))

# Plot arc-transformed image
ax.scatter(X_arc, Y_arc, c=colours, s=2, marker='s')

# Plot original image in the small circle
ax.scatter(x_orig, y_orig, c=colours, s=2, marker='s')

# Draw reference small circle outline
ax.add_patch(Circle((0, 0), 1, edgecolor='black', facecolor='none', linewidth=2))

ax.set_aspect('equal')
ax.set_xlim(-6, 6)
ax.set_ylim(-7, 2)
plt.show()
