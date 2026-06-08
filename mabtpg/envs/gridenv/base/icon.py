

import numpy as np
from PIL import Image

def draw_icon(icon_folder_path, icon_name, img):
    image = Image.open(f"{icon_folder_path}\\{icon_name}.png")

    resized_image = image.resize(img.shape[:2], Image.Resampling.LANCZOS)
    image_data = np.array(resized_image)

    alpha_mask = image_data[:, :, 3] > 0.1
    img[alpha_mask] = image_data[:, :, :3][alpha_mask]

    return image

# class ICONS:
#     apple = icon("apple")


