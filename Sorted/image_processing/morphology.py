"""
Binary Morphology Laboratory
============================
Implements mathematical morphology on binary images:
- Structuring Elements (Cross 3x3, Square 3x3, Disk 5x5)
- Erosion: A (-) B
- Dilation: A (+) B
- Opening: (A (-) B) (+) B
- Closing: (A (+) B) (-) B
- Morphological Gradient: Dilation - Erosion
"""

import numpy as np
from typing import Dict, Any, Tuple


STRUCTURING_ELEMENTS = {
    "cross_3x3": np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=np.uint8),
    "square_3x3": np.array([[1, 1, 1], [1, 1, 1], [1, 1, 1]], dtype=np.uint8),
    "disk_5x5": np.array([
        [0, 1, 1, 1, 0],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1],
        [0, 1, 1, 1, 0]
    ], dtype=np.uint8)
}


def binary_erosion(binary_img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Erosion: A (-) B
    An output pixel is 255 if and only if EVERY active pixel of the structuring element
    fits completely within the foreground (255) of the input image.
    Shrinks foreground regions and eliminates small isolated noise spots.
    """
    h, w = binary_img.shape
    kh, kw = se.shape
    rad_h = kh // 2
    rad_w = kw // 2
    
    pad_img = np.pad(binary_img, ((rad_h, rad_h), (rad_w, rad_w)), mode='constant', constant_values=0)
    out = np.zeros_like(binary_img, dtype=np.uint8)
    
    se_mask = (se == 1)
    se_count = np.sum(se_mask)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + kh, c : c + kw]
            # Check if all SE foreground pixels match image foreground
            if np.sum((win == 255) & se_mask) == se_count:
                out[r, c] = 255
                
    return out


def binary_dilation(binary_img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Dilation: A (+) B
    An output pixel is 255 if AT LEAST ONE active pixel of the structuring element
    hits the foreground (255) of the input image.
    Expands foreground regions, closes small holes, and bridges narrow breaks.
    """
    h, w = binary_img.shape
    kh, kw = se.shape
    rad_h = kh // 2
    rad_w = kw // 2
    
    pad_img = np.pad(binary_img, ((rad_h, rad_h), (rad_w, rad_w)), mode='constant', constant_values=0)
    out = np.zeros_like(binary_img, dtype=np.uint8)
    
    se_mask = (se == 1)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + kh, c : c + kw]
            if np.any((win == 255) & se_mask):
                out[r, c] = 255
                
    return out


def binary_opening(binary_img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Opening: (A (-) B) (+) B
    Erosion followed by Dilation.
    Eliminates thin protrusions and small isolated islands while preserving object sizes.
    """
    eroded = binary_erosion(binary_img, se)
    return binary_dilation(eroded, se)


def binary_closing(binary_img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Closing: (A (+) B) (-) B
    Dilation followed by Erosion.
    Fills small holes, fuses narrow breaks, and smooths boundaries.
    """
    dilated = binary_dilation(binary_img, se)
    return binary_erosion(dilated, se)


def morphological_gradient(binary_img: np.ndarray, se: np.ndarray) -> np.ndarray:
    """
    Morphological Gradient: Dilation - Erosion
    Extracts the inner and outer boundary profile of foreground regions.
    """
    dil = binary_dilation(binary_img, se)
    ero = binary_erosion(binary_img, se)
    return np.clip(dil.astype(int) - ero.astype(int), 0, 255).astype(np.uint8)
