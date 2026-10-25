"""
Spatial Filtering and Kernel Movement Laboratory
================================================
Implements 2D spatial convolution and correlation, neighbourhood padding,
stride calculations, linear and order-statistic filters, and step-by-step
arithmetic traces for the interactive Kernel Movement Laboratory.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional


KERNEL_PRESETS = {
    "box_3x3": {
        "name": "3x3 Mean / Box Filter",
        "category": "Smoothing (Low-Pass)",
        "kernel": [[1/9, 1/9, 1/9], [1/9, 1/9, 1/9], [1/9, 1/9, 1/9]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Standard moving average. Treats all 9 neighbouring pixels equally to suppress high-frequency noise."
    },
    "weighted_3x3": {
        "name": "Weighted Average (Gaussian Approx)",
        "category": "Smoothing (Low-Pass)",
        "kernel": [[1/16, 2/16, 1/16], [2/16, 4/16, 2/16], [1/16, 2/16, 1/16]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Weights center pixel highest (4/16) and diagonals lowest (1/16) to reduce blurring of edges."
    },
    "gaussian_3x3": {
        "name": "Gaussian Blur (sigma=1.0)",
        "category": "Smoothing (Low-Pass)",
        "kernel": [[0.0751, 0.1238, 0.0751], [0.1238, 0.2044, 0.1238], [0.0751, 0.1238, 0.0751]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "True 2D Gaussian distribution filter. Best linear filter for suppressing zero-mean Gaussian noise."
    },
    "gaussian_5x5": {
        "name": "Gaussian Blur 5x5",
        "category": "Smoothing (Low-Pass)",
        "kernel": [
            [1/256, 4/256, 6/256, 4/256, 1/256],
            [4/256, 16/256, 24/256, 16/256, 4/256],
            [6/256, 24/256, 36/256, 24/256, 6/256],
            [4/256, 16/256, 24/256, 16/256, 4/256],
            [1/256, 4/256, 6/256, 4/256, 1/256]
        ],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Larger 5x5 spatial support for substantial noise reduction."
    },
    "median_3x3": {
        "name": "Median Filter 3x3",
        "category": "Non-Linear Order-Statistic",
        "kernel": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "median",
        "description": "Replaces center pixel with the median of sorted 9 neighbourhood pixels. Optimal for Salt-and-Pepper noise without edge blurring."
    },
    "min_3x3": {
        "name": "Minimum Filter 3x3 (Erosion-like)",
        "category": "Non-Linear Order-Statistic",
        "kernel": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "min",
        "description": "Replaces center pixel with minimum neighbourhood intensity. Enhances dark regions and erodes bright points."
    },
    "max_3x3": {
        "name": "Maximum Filter 3x3 (Dilation-like)",
        "category": "Non-Linear Order-Statistic",
        "kernel": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "max",
        "description": "Replaces center pixel with maximum neighbourhood intensity. Expands bright regions and bridges small dark gaps."
    },
    "sobel_x": {
        "name": "Sobel X (Vertical Edge Detector)",
        "category": "Gradient / Edge Detection",
        "kernel": [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Calculates horizontal derivative dF/dx. Emphasizes vertical boundaries."
    },
    "sobel_y": {
        "name": "Sobel Y (Horizontal Edge Detector)",
        "category": "Gradient / Edge Detection",
        "kernel": [[-1, -2, -1], [0, 0, 0], [1, 2, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Calculates vertical derivative dF/dy. Emphasizes horizontal boundaries."
    },
    "laplacian_4": {
        "name": "Laplacian (4-Connectivity)",
        "category": "Sharpening / 2nd Derivative",
        "kernel": [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Isotropic 2nd derivative operator using 4-neighbourhood. Detects rapid rate of intensity changes."
    },
    "laplacian_8": {
        "name": "Laplacian (8-Connectivity)",
        "category": "Sharpening / 2nd Derivative",
        "kernel": [[1, 1, 1], [1, -8, 1], [1, 1, 1]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Isotropic 2nd derivative operator including diagonals (8-neighbourhood)."
    },
    "sharpen_3x3": {
        "name": "High-Pass Sharpening",
        "category": "Sharpening (High-Pass)",
        "kernel": [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
        "norm": 1.0,
        "offset": 0,
        "type": "linear",
        "description": "Enhances edge transitions by adding Laplacian high-pass details back to the central original pixel."
    }
}


def calculate_output_dimensions(in_h: int, in_w: int, k_h: int, k_w: int, stride: int = 1, pad: int = 0) -> Tuple[int, int]:
    """
    Standard spatial output dimension formula:
      out = floor((in + 2*pad - kernel) / stride) + 1
    """
    out_h = int(np.floor((in_h + 2 * pad - k_h) / float(stride))) + 1
    out_w = int(np.floor((in_w + 2 * pad - k_w) / float(stride))) + 1
    return max(0, out_h), max(0, out_w)


def pad_image(arr: np.ndarray, pad_h: int, pad_w: int, mode: str = 'zero') -> np.ndarray:
    """
    Applies spatial padding to 2D image matrix:
      - 'zero': constant 0 padding
      - 'replicate': clamp to border pixels
      - 'reflect': mirror boundary pixels
    """
    if pad_h <= 0 and pad_w <= 0:
        return arr.copy()
        
    pad_width = ((pad_h, pad_h), (pad_w, pad_w))
    if arr.ndim == 3:
        pad_width = ((pad_h, pad_h), (pad_w, pad_w), (0, 0))
        
    if mode == 'replicate' or mode == 'edge':
        return np.pad(arr, pad_width, mode='edge')
    elif mode == 'reflect':
        return np.pad(arr, pad_width, mode='reflect')
    else:  # default zero padding
        return np.pad(arr, pad_width, mode='constant', constant_values=0)


def compute_kernel_step(
    input_mat: np.ndarray,
    kernel_mat: np.ndarray,
    center_r: int,
    center_c: int,
    padding_mode: str = 'zero',
    is_convolution: bool = False,
    op_type: str = 'linear',
    stride: int = 1
) -> Dict[str, Any]:
    """
    Computes a single educational step of spatial filtering at position (center_r, center_c).
    Returns complete breakdown of neighbourhood, products, summation, clipping, and explanation.
    """
    k_h, k_w = kernel_mat.shape
    rad_h = k_h // 2
    rad_w = k_w // 2
    
    pad_h = rad_h if padding_mode != 'valid' else 0
    pad_w = rad_w if padding_mode != 'valid' else 0
    
    padded = pad_image(input_mat, pad_h, pad_w, mode=padding_mode)
    
    # Coordinates in padded matrix
    pr = center_r + pad_h
    pc = center_c + pad_w
    
    neighbourhood = padded[pr - rad_h : pr + rad_h + 1, pc - rad_w : pc + rad_w + 1].astype(float)
    
    # Kernel for operation
    effective_kernel = np.flip(kernel_mat).astype(float) if is_convolution else kernel_mat.astype(float)
    
    if op_type == 'median':
        sorted_vals = sorted(neighbourhood.flatten().tolist())
        med_val = float(np.median(neighbourhood))
        return {
            "r": center_r,
            "c": center_c,
            "neighbourhood": neighbourhood.tolist(),
            "kernel": effective_kernel.tolist(),
            "sorted_values": sorted_vals,
            "calculated_value": med_val,
            "output_value": int(np.clip(round(med_val), 0, 255)),
            "operation": "Median Filter",
            "explanation": f"Sorted neighbourhood: {sorted_vals}. Median value is {med_val}."
        }
    elif op_type == 'min':
        min_val = float(np.min(neighbourhood))
        return {
            "r": center_r,
            "c": center_c,
            "neighbourhood": neighbourhood.tolist(),
            "kernel": effective_kernel.tolist(),
            "calculated_value": min_val,
            "output_value": int(np.clip(round(min_val), 0, 255)),
            "operation": "Minimum Filter",
            "explanation": f"Minimum neighbourhood value is {min_val}."
        }
    elif op_type == 'max':
        max_val = float(np.max(neighbourhood))
        return {
            "r": center_r,
            "c": center_c,
            "neighbourhood": neighbourhood.tolist(),
            "kernel": effective_kernel.tolist(),
            "calculated_value": max_val,
            "output_value": int(np.clip(round(max_val), 0, 255)),
            "operation": "Maximum Filter",
            "explanation": f"Maximum neighbourhood value is {max_val}."
        }
    else:  # Linear Spatial Filter (Sum of Products)
        products = neighbourhood * effective_kernel
        raw_sum = float(np.sum(products))
        clipped_val = int(np.clip(round(raw_sum), 0, 255))
        
        return {
            "r": center_r,
            "c": center_c,
            "neighbourhood": neighbourhood.tolist(),
            "kernel": effective_kernel.tolist(),
            "products": np.round(products, 3).tolist(),
            "sum_of_products": round(raw_sum, 3),
            "output_value": clipped_val,
            "is_convolution": is_convolution,
            "operation": "2D Convolution" if is_convolution else "2D Cross-Correlation",
            "explanation": f"At ({center_r}, {center_c}): sum of products = {raw_sum:.2f} -> clipped to {clipped_val}."
        }


def apply_spatial_filter(
    arr: np.ndarray,
    kernel_mat: np.ndarray,
    padding_mode: str = 'replicate',
    is_convolution: bool = False,
    op_type: str = 'linear',
    stride: int = 1
) -> np.ndarray:
    """
    Applies spatial filter over the complete 2D or 3D array.
    """
    if arr.ndim == 3:
        # Process each channel independently
        chans = []
        for c in range(arr.shape[2]):
            chans.append(apply_spatial_filter(arr[:, :, c], kernel_mat, padding_mode, is_convolution, op_type, stride))
        return np.stack(chans, axis=2)
        
    in_h, in_w = arr.shape
    k_h, k_w = kernel_mat.shape
    rad_h = k_h // 2
    rad_w = k_w // 2
    
    pad_h = rad_h if padding_mode != 'valid' else 0
    pad_w = rad_w if padding_mode != 'valid' else 0
    
    out_h, out_w = calculate_output_dimensions(in_h, in_w, k_h, k_w, stride, pad_h)
    padded = pad_image(arr, pad_h, pad_w, mode=padding_mode).astype(float)
    effective_kernel = np.flip(kernel_mat).astype(float) if is_convolution else kernel_mat.astype(float)
    
    out = np.zeros((out_h, out_w), dtype=float)
    
    for r_idx in range(out_h):
        r_orig = r_idx * stride
        for c_idx in range(out_w):
            c_orig = c_idx * stride
            window = padded[r_orig : r_orig + k_h, c_orig : c_orig + k_w]
            
            if op_type == 'median':
                out[r_idx, c_idx] = np.median(window)
            elif op_type == 'min':
                out[r_idx, c_idx] = np.min(window)
            elif op_type == 'max':
                out[r_idx, c_idx] = np.max(window)
            else:
                out[r_idx, c_idx] = np.sum(window * effective_kernel)
                
    return np.clip(np.round(out), 0, 255).astype(np.uint8)
