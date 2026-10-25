"""
Intensity Transformations (Point Operations)
============================================
Implements spatial domain point operations where output intensity s = T(r):
- Image Negative: s = (L - 1) - r
- Logarithmic: s = c * log(1 + r)
- Power-Law (Gamma): s = c * r^gamma
- Piecewise Linear Contrast Stretching
- Intensity-Level Slicing (with and without background preservation)
- Thresholding
- Linear Brightness & Contrast: s = alpha * r + beta
- Min-Max Intensity Normalisation
"""

import numpy as np
from typing import Dict, Any, Tuple, List


def transform_negative(arr: np.ndarray) -> Tuple[np.ndarray, List[int]]:
    """
    Image Negative: s = 255 - r
    Inverts pixel values (reverses light and dark tones).
    """
    out = (255 - arr).astype(np.uint8)
    lut = [255 - r for r in range(256)]
    return out, lut


def transform_logarithmic(arr: np.ndarray, c: float = None) -> Tuple[np.ndarray, List[int]]:
    """
    Logarithmic Transformation: s = c * log(1 + r)
    Expands dark pixels and compresses high-intensity dynamic range.
    """
    r_float = arr.astype(float)
    max_val = np.max(r_float)
    if c is None:
        c = 255.0 / np.log(1.0 + max(1.0, max_val))
    
    out_float = c * np.log(1.0 + r_float)
    out = np.clip(np.round(out_float), 0, 255).astype(np.uint8)
    
    lut = [int(np.clip(round(c * np.log(1.0 + r)), 0, 255)) for r in range(256)]
    return out, lut


def transform_gamma(arr: np.ndarray, gamma: float = 1.0, c: float = 1.0) -> Tuple[np.ndarray, List[int]]:
    """
    Power-Law (Gamma) Transformation: s = c * 255 * (r / 255)^gamma
    gamma < 1.0: expands dark pixels (brightens shadow detail).
    gamma > 1.0: compresses dark pixels and expands bright pixels (increases contrast in highlights).
    """
    norm = arr.astype(float) / 255.0
    out_float = c * 255.0 * np.power(norm, gamma)
    out = np.clip(np.round(out_float), 0, 255).astype(np.uint8)
    
    lut = [int(np.clip(round(c * 255.0 * ((r / 255.0) ** gamma)), 0, 255)) for r in range(256)]
    return out, lut


def transform_contrast_stretch(arr: np.ndarray, r1: int = 70, s1: int = 20, r2: int = 180, s2: int = 230) -> Tuple[np.ndarray, List[int]]:
    """
    Piecewise Linear Contrast Stretching:
    Stretches narrow dynamic range across full [0, 255] spectrum:
      r < r1: slope = s1 / r1
      r1 <= r <= r2: slope = (s2 - s1) / (r2 - r1)
      r > r2: slope = (255 - s2) / (255 - r2)
    """
    r1 = max(1, min(253, r1))
    r2 = max(r1 + 1, min(254, r2))
    
    lut = []
    for r in range(256):
        if r < r1:
            val = (s1 / float(r1)) * r
        elif r <= r2:
            val = s1 + ((s2 - s1) / float(r2 - r1)) * (r - r1)
        else:
            val = s2 + ((255 - s2) / float(255 - r2)) * (r - r2)
        lut.append(int(np.clip(round(val), 0, 255)))
        
    lut_arr = np.array(lut, dtype=np.uint8)
    out = lut_arr[arr]
    return out, lut


def transform_intensity_slicing(arr: np.ndarray, low: int = 100, high: int = 200, highlight_val: int = 255, preserve_background: bool = True) -> Tuple[np.ndarray, List[int]]:
    """
    Intensity-Level Slicing:
    Highlights specific intensity interval [low, high].
    If preserve_background is True: outside interval retains original r.
    If False: outside interval is suppressed to 0.
    """
    lut = []
    for r in range(256):
        if low <= r <= high:
            val = highlight_val
        else:
            val = r if preserve_background else 0
        lut.append(val)
        
    lut_arr = np.array(lut, dtype=np.uint8)
    out = lut_arr[arr]
    return out, lut


def transform_brightness_contrast(arr: np.ndarray, alpha: float = 1.0, beta: float = 0.0) -> Tuple[np.ndarray, List[int]]:
    """
    Linear Brightness and Contrast:
    s = alpha * r + beta
    alpha: Contrast multiplier (1.0 = normal, >1.0 = higher contrast)
    beta: Brightness offset (-100 to +100)
    """
    out_float = alpha * arr.astype(float) + beta
    out = np.clip(np.round(out_float), 0, 255).astype(np.uint8)
    
    lut = [int(np.clip(round(alpha * r + beta), 0, 255)) for r in range(256)]
    return out, lut


def transform_normalize(arr: np.ndarray) -> Tuple[np.ndarray, List[int]]:
    """
    Min-Max Normalisation:
    Maps [min_val, max_val] linearly to [0, 255].
    """
    min_val = float(np.min(arr))
    max_val = float(np.max(arr))
    
    if max_val - min_val < 1e-5:
        return arr.copy(), list(range(256))
        
    lut = []
    scale = 255.0 / (max_val - min_val)
    for r in range(256):
        val = (r - min_val) * scale
        lut.append(int(np.clip(round(val), 0, 255)))
        
    lut_arr = np.array(lut, dtype=np.uint8)
    out = lut_arr[arr]
    return out, lut
