from PIL import Image
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np
import io

def create_image_from_maze(maze, scale_factor=1):
    fig = Figure()
    ax = fig.add_subplot(111)
    ax.imshow(maze, cmap='gray')
    ax.axis('off')
    img_buff = io.BytesIO()
    fig.savefig(img_buff, format='jpeg', bbox_inches='tight', pad_inches=0)
    img_buff.seek(0)
    # Use PIL to open the image
    img_pil = Image.open(img_buff)
    img_pil = img_pil.resize((int(img_pil.width * scale_factor), int(img_pil.height * scale_factor)))

    # Convert the PIL image to a NumPy array
    img_array = np.array(img_pil)
    copy_image = np.copy(img_array)
    img_buff.close()

    return copy_image