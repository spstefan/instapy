"""pure Python implementation of image filters"""
from __future__ import annotations

import numpy as np


def python_color2gray(image: np.array) -> np.array:
    """Convert rgb pixel array to grayscale

    Args:
        image (np.array)
    Returns:
        np.array: gray_image
    """
    gray_image = np.empty_like(image)
    # iterate through the pixels, and apply the grayscale transform

    row_index = 0
    for row in image:
        col_index = 0
        for col in row:
            gray_value = col[0] * 0.21 + col[1] * 0.72 + col[2] * 0.07
            gray_image[row_index, col_index, 0] = gray_value
            gray_image[row_index, col_index, 1] = gray_value
            gray_image[row_index, col_index, 2] = gray_value
            col_index += 1
        row_index += 1

    return gray_image


def python_color2sepia(image: np.array) -> np.array:
    """Convert rgb pixel array to sepia

    Args:
        image (np.array)
    Returns:
        np.array: sepia_image
    """
    sepia_image = np.empty_like(image)
    
    # Iterate through the pixels
    row_index = 0
    for row in image:
        col_index = 0
        for col in row:
            # calculate new color values for each channel using the sepia matrix
            R_new = col[0] * 0.393 + col[1] * 0.769 + col[2] * 0.189
            G_new = col[0] * 0.349 + col[1] * 0.686 + col[2] * 0.168
            B_new = col[0] * 0.272 + col[1] * 0.534 + col[2] * 0.131
            
            # clipping the values to the maximum value of 255, if necessary
            sepia_image[row_index, col_index, 0] = min(R_new, 255)
            sepia_image[row_index, col_index, 1] = min(G_new, 255)
            sepia_image[row_index, col_index, 2] = min(B_new, 255)
            
            col_index += 1
        row_index += 1

    # Return image
    # don't forget to make sure it's the right type!
    return sepia_image.astype(image.dtype)
