"""
Image Conversions, Sampling, Quantization & Color Models
========================================================
Implements mathematical transformations between image representations:
- Spatial Sampling & Intensity Quantization (Unit 1 Slide 22)
- RGB to Grayscale (Standard ITU-R BT.601 / NTSC)
- Grayscale to Binary (Thresholding)
- RGB <-> HSV Color Space
- Channel Separation and Recombination
- RGB vs BGR Channel Ordering analysis
"""

import numpy as np
from typing import Dict, Any, Tuple, Optional


def apply_sampling(arr: np.ndarray, factor: int) -> np.ndarray:
    """
    Simulates spatial sampling: converts continuous space to discrete grid.
    Higher factor = lower sampling resolution (downsampled blocks).
    """
    if factor <= 1:
        return arr.copy()
    h, w = arr.shape[:2]
    # Downsample by block averaging or nearest neighbor
    small_h = max(1, h // factor)
    small_w = max(1, w // factor)
    
    # Simple, transparent nearest-neighbor / block sampling
    sampled = np.zeros_like(arr)
    for r in range(0, h, factor):
        for c in range(0, w, factor):
            block = arr[r:min(r+factor, h), c:min(c+factor, w)]
            mean_val = np.mean(block, axis=(0, 1)).astype(arr.dtype)
            sampled[r:min(r+factor, h), c:min(c+factor, w)] = mean_val
    return sampled


def apply_quantization(arr: np.ndarray, bits: int) -> np.ndarray:
    """
    Simulates intensity quantization: maps continuous intensity into discrete levels.
    bits: 1 to 8 (levels = 2^bits, e.g., 1-bit -> 2 levels, 8-bit -> 256 levels).
    Demonstrates contouring / intensity banding when bits are low.
    """
    bits = max(1, min(8, bits))
    levels = 2 ** bits
    # Step size between discrete bins
    step = 256.0 / levels
    # Quantize: floor(val / step) * (255 / (levels - 1))
    quantized = np.floor(arr.astype(float) / step) * (255.0 / (levels - 1))
    return np.clip(np.round(quantized), 0, 255).astype(np.uint8)


def rgb_to_grayscale(rgb: np.ndarray, method: str = 'luminosity') -> np.ndarray:
    """
    Converts 3-channel RGB image to 1-channel Grayscale.
    Methods:
      - 'luminosity' (standard NTSC / ITU-R BT.601): Y = 0.299*R + 0.587*G + 0.114*B
      - 'average': Y = (R + G + B) / 3
      - 'lightness': Y = (max(R,G,B) + min(R,G,B)) / 2
    """
    if rgb.ndim == 2:
        return rgb.copy()
    
    r = rgb[:, :, 0].astype(float)
    g = rgb[:, :, 1].astype(float)
    b = rgb[:, :, 2].astype(float)
    
    if method == 'average':
        gray = (r + g + b) / 3.0
    elif method == 'lightness':
        gray = (np.maximum(np.maximum(r, g), b) + np.minimum(np.minimum(r, g), b)) / 2.0
    else:  # Standard weighted luminosity
        gray = 0.299 * r + 0.587 * g + 0.114 * b
        
    return np.clip(np.round(gray), 0, 255).astype(np.uint8)


def grayscale_to_binary(gray: np.ndarray, threshold: int = 128) -> np.ndarray:
    """
    Converts 1-channel Grayscale image to Binary image:
    f_bin(x, y) = 255 if f(x, y) >= threshold else 0
    (Unit 1 Slide 15: 1 bit per pixel, 0=Black, 1/255=White)
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
    binary = np.where(gray >= threshold, 255, 0).astype(np.uint8)
    return binary


def rgb_to_hsv(rgb: np.ndarray) -> np.ndarray:
    """
    Pure NumPy implementation of RGB to HSV conversion.
    Returns array of same shape where:
      H in [0, 360) degrees
      S in [0, 100]%
      V in [0, 100]%
    """
    arr = rgb.astype(float) / 255.0
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    
    max_c = np.maximum(np.maximum(r, g), b)
    min_c = np.minimum(np.minimum(r, g), b)
    delta = max_c - min_c
    
    # Value
    v = max_c
    
    # Saturation
    s = np.zeros_like(v)
    non_zero = max_c > 1e-6
    s[non_zero] = delta[non_zero] / max_c[non_zero]
    
    # Hue
    h = np.zeros_like(v)
    delta_non_zero = delta > 1e-6
    
    # Where max is R
    mask_r = delta_non_zero & (max_c == r)
    h[mask_r] = 60.0 * (((g[mask_r] - b[mask_r]) / delta[mask_r]) % 6)
    
    # Where max is G
    mask_g = delta_non_zero & (max_c == g)
    h[mask_g] = 60.0 * (((b[mask_g] - r[mask_g]) / delta[mask_g]) + 2)
    
    # Where max is B
    mask_b = delta_non_zero & (max_c == b)
    h[mask_b] = 60.0 * (((r[mask_b] - g[mask_b]) / delta[mask_b]) + 4)
    
    # Scale to educational user-friendly percentages
    hsv = np.zeros_like(arr)
    hsv[:, :, 0] = h  # 0 - 360
    hsv[:, :, 1] = s * 100.0  # 0 - 100%
    hsv[:, :, 2] = v * 100.0  # 0 - 100%
    return hsv


def hsv_to_rgb(hsv: np.ndarray) -> np.ndarray:
    """
    Converts HSV (H:[0,360], S:[0,100], V:[0,100]) back to RGB uint8 [0, 255].
    """
    h = hsv[:, :, 0] % 360.0
    s = np.clip(hsv[:, :, 1] / 100.0, 0.0, 1.0)
    v = np.clip(hsv[:, :, 2] / 100.0, 0.0, 1.0)
    
    c = v * s
    x = c * (1.0 - np.abs((h / 60.0) % 2 - 1.0))
    m = v - c
    
    r_prime = np.zeros_like(h)
    g_prime = np.zeros_like(h)
    b_prime = np.zeros_like(h)
    
    m0 = (h >= 0) & (h < 60)
    r_prime[m0], g_prime[m0], b_prime[m0] = c[m0], x[m0], 0
    m1 = (h >= 60) & (h < 120)
    r_prime[m1], g_prime[m1], b_prime[m1] = x[m1], c[m1], 0
    m2 = (h >= 120) & (h < 180)
    r_prime[m2], g_prime[m2], b_prime[m2] = 0, c[m2], x[m2]
    m3 = (h >= 180) & (h < 240)
    r_prime[m3], g_prime[m3], b_prime[m3] = 0, x[m3], c[m3]
    m4 = (h >= 240) & (h < 300)
    r_prime[m4], g_prime[m4], b_prime[m4] = x[m4], 0, c[m4]
    m5 = (h >= 300) & (h < 360)
    r_prime[m5], g_prime[m5], b_prime[m5] = c[m5], 0, x[m5]
    
    rgb = np.zeros_like(hsv)
    rgb[:, :, 0] = (r_prime + m) * 255.0
    rgb[:, :, 1] = (g_prime + m) * 255.0
    rgb[:, :, 2] = (b_prime + m) * 255.0
    return np.clip(np.round(rgb), 0, 255).astype(np.uint8)


def separate_rgb_channels(rgb: np.ndarray) -> Dict[str, np.ndarray]:
    """
    Separates an RGB image into individual single-channel grayscale views
    and colored channel isolate views.
    """
    r = rgb[:, :, 0]
    g = rgb[:, :, 1]
    b = rgb[:, :, 2]
    
    # Colored channel isolates
    r_iso = np.zeros_like(rgb)
    r_iso[:, :, 0] = r
    
    g_iso = np.zeros_like(rgb)
    g_iso[:, :, 1] = g
    
    b_iso = np.zeros_like(rgb)
    b_iso[:, :, 2] = b
    
    return {
        "red_gray": r,
        "green_gray": g,
        "blue_gray": b,
        "red_isolate": r_iso,
        "green_isolate": g_iso,
        "blue_isolate": b_iso
    }


def hsv_color_mask(rgb: np.ndarray, h_min: float, h_max: float, s_min: float, s_max: float, v_min: float, v_max: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Applies color segmentation mask in HSV color space.
    Returns (binary_mask, masked_rgb_image).
    """
    hsv = rgb_to_hsv(rgb)
    h, s, v = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]
    
    if h_min <= h_max:
        h_cond = (h >= h_min) & (h <= h_max)
    else:  # Hue wraps around 0/360 (e.g. red: 340 to 20)
        h_cond = (h >= h_min) | (h <= h_max)
        
    s_cond = (s >= s_min) & (s <= s_max)
    v_cond = (v >= v_min) & (v <= v_max)
    
    mask = h_cond & s_cond & v_cond
    bin_mask = np.where(mask, 255, 0).astype(np.uint8)
    
    masked_rgb = rgb.copy()
    masked_rgb[~mask] = [30, 30, 45] # Dark background
    
    return bin_mask, masked_rgb


def swap_rgb_bgr(rgb: np.ndarray) -> np.ndarray:
    """
    Demonstrates OpenCV's BGR order versus standard web RGB order.
    Swaps channel 0 and channel 2 (Red <-> Blue).
    """
    bgr = rgb.copy()
    bgr[:, :, 0] = rgb[:, :, 2]
    bgr[:, :, 2] = rgb[:, :, 0]
    return bgr
