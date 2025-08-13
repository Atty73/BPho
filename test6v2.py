from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Ellipse
import tkinter as tk

# -------------------------------------------------------------------
# Global parameters and state
# -------------------------------------------------------------------
IMAGE_RES = 256
f = IMAGE_RES // 5

LEFT, UP, RIGHT, DOWN = 0, 1, 2, 3
coordinates = [0, 0]  # Pan offsets [dx, dy]

picture = None
canvas = None
ax = None


# -------------------------------------------------------------------
# 1. Load and prepare the image
# -------------------------------------------------------------------
def create_pil_image(path):
    """
    Load a PNG, convert to RGBA, resize to IMAGE_RES²,
    shrink by 50%, and center on a transparent canvas.
    """
    img = Image.open(path).convert('RGBA')
    img = img.resize((IMAGE_RES, IMAGE_RES), Image.LANCZOS)

    bg = Image.new('RGBA', (IMAGE_RES, IMAGE_RES), (255, 255, 255, 0))
    shrunken = img.resize((IMAGE_RES // 2, IMAGE_RES // 2), Image.LANCZOS)

    offset = ((IMAGE_RES - shrunken.width) // 2,
              (IMAGE_RES - shrunken.height) // 2)
    bg.paste(shrunken, offset, shrunken)
    return bg


# -------------------------------------------------------------------
# 2. Build coordinate grids
# -------------------------------------------------------------------
def build_coordinate_grids(pil_img):
    """
    Returns:
      pixel_array:  HxWx4 uint8 RGBA array
      x_flat, y_flat: flattened 1D coords offset by pan
    """
    pixel_array = np.array(pil_img)
    H, W = pixel_array.shape[:2]

    x_grid, y_grid = np.meshgrid(np.arange(W), np.arange(H))
    x_flat = x_grid.flatten() + coordinates[0]
    y_flat = y_grid.flatten() + coordinates[1]

    return pixel_array, x_flat, y_flat


# -------------------------------------------------------------------
# 3. Apply the thin‐lens transformation
# -------------------------------------------------------------------
def apply_lens_transform(x_flat, y_flat):
    """
    Vectorized thin-lens mapping for points where x > f.
    """
    new_x = x_flat.copy()
    new_y = y_flat.copy()

    mask = x_flat > f
    denom = x_flat[mask] - f

    new_x[mask] = -(f / denom) * x_flat[mask]
    new_y[mask] = (y_flat[mask] / x_flat[mask]) * new_x[mask]
    # new_x[mask] = -x_flat[mask]
    # new_y[mask] = -y_flat[mask]
    return new_x, new_y


# -------------------------------------------------------------------
# 4. Normalize colors
# -------------------------------------------------------------------
def normalize_colors(pixel_array):
    """
    Flattens HxWx4 → (H·W)x4 floats in [0,1].
    """
    flat = pixel_array.reshape(-1, pixel_array.shape[2])
    return flat.astype(float) / 255.0


# -------------------------------------------------------------------
# 5. Render the scene
# -------------------------------------------------------------------
def render(ax, x_flat, y_flat, new_x, new_y, colors):
    ax.clear()
    ax.invert_yaxis()
    ax.set_xlim(-1.5 * IMAGE_RES, 1.5 * IMAGE_RES)
    ax.set_ylim(-1.5 * IMAGE_RES, 1.5 * IMAGE_RES)
    ax.invert_yaxis()

    # Draw gridlines for reference
    ax.grid(
        True, which='major', color='gray', linestyle='--', linewidth=0.5, alpha=0.7)

    # Warped pixels (big squares) + original (tiny points)
    ax.scatter(new_x, new_y, c=colors, marker='s', s=1)
    ax.scatter(x_flat, y_flat, c=colors, marker='s', s=1)

    # Lens outline
    lens = Ellipse((0, 0), width=25, height=125,
                   linewidth=2, edgecolor='red', facecolor='none')
    ax.add_patch(lens)

    # Mark the focal point at (f, 0)
    ax.scatter(f, 0, c='blue', marker='x', s=100, label='Focal Point')


# -------------------------------------------------------------------
# Redraw helper
# -------------------------------------------------------------------
def update_canvas():
    """
    Recompute grids, transform, color-map, and redraw.
    """
    pixel_array, x_flat, y_flat = build_coordinate_grids(picture)
    new_x, new_y = apply_lens_transform(x_flat, y_flat)
    colors = normalize_colors(pixel_array)

    render(ax, x_flat, y_flat, new_x, new_y, colors)
    canvas.draw()


# -------------------------------------------------------------------
# 6. Interactive panning
# -------------------------------------------------------------------
def move_image(no_pixels, direction, event):
    """
    Update pan offsets and redraw.
    """
    if direction == LEFT:
        coordinates[0] -= no_pixels
    elif direction == RIGHT:
        coordinates[0] += no_pixels
    elif direction == UP:
        coordinates[1] -= no_pixels
    elif direction == DOWN:
        coordinates[1] += no_pixels

    update_canvas()


# -------------------------------------------------------------------
# Main application setup
# -------------------------------------------------------------------
def main():
    global picture, canvas, ax

    window = tk.Tk()
    window.title("Thin Lens Simulation")

    # Load and preprocess
    picture = create_pil_image("sheldon.png")

    # Matplotlib figure embedded in Tkinter
    fig = Figure(figsize=(8, 8))
    ax = fig.add_subplot(111)

    canvas = FigureCanvasTkAgg(fig, master=window)
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    update_canvas()

    # Key bindings for panning
    step = IMAGE_RES // 16
    window.bind("<Left>", lambda e: move_image(step, LEFT, e))
    window.bind("<Right>", lambda e: move_image(step, RIGHT, e))
    window.bind("<Up>", lambda e: move_image(step, UP, e))
    window.bind("<Down>", lambda e: move_image(step, DOWN, e))

    window.mainloop()


if __name__ == "__main__":
    main()