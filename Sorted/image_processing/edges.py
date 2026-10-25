"""
Edge Detection & Multi-Stage Canny Laboratory
=============================================
Implements 1st and 2nd derivative edge operators:
- Sobel X and Sobel Y
- Prewitt X and Prewitt Y
- Laplacian (4- and 8-connectivity)
- Gradient Magnitude and Gradient Direction
- Full 5-stage Canny Edge Detector with inspectable intermediate stages
  (Gaussian -> Gradient -> Non-Maximum Suppression -> Double Threshold -> Hysteresis)
"""

import numpy as np
from typing import Dict, Any, Tuple
from .kernels import apply_spatial_filter
from .conversions import rgb_to_grayscale


PREWITT_X = np.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]], dtype=float)
PREWITT_Y = np.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]], dtype=float)
SOBEL_X = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], dtype=float)
SOBEL_Y = np.array([[-1, -2, -1], [0, 0, 0], [1, 2, 1]], dtype=float)


def compute_gradient_operators(gray: np.ndarray, operator: str = 'sobel') -> Dict[str, np.ndarray]:
    """
    Computes horizontal derivative Gx, vertical derivative Gy,
    gradient magnitude G = sqrt(Gx^2 + Gy^2), and gradient direction angle.
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
        
    kx = SOBEL_X if operator == 'sobel' else PREWITT_X
    ky = SOBEL_Y if operator == 'sobel' else PREWITT_Y
    
    # We apply correlation with unclipped float
    h, w = gray.shape
    pad_img = np.pad(gray.astype(float), ((1, 1), (1, 1)), mode='edge')
    
    gx = np.zeros_like(gray, dtype=float)
    gy = np.zeros_like(gray, dtype=float)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + 3, c : c + 3]
            gx[r, c] = np.sum(win * kx)
            gy[r, c] = np.sum(win * ky)
            
    magnitude = np.sqrt(gx**2 + gy**2)
    direction = np.arctan2(gy, gx) * (180.0 / np.pi) % 180.0  # [0, 180) degrees
    
    # Normalized for display [0, 255]
    gx_disp = np.clip(np.abs(gx), 0, 255).astype(np.uint8)
    gy_disp = np.clip(np.abs(gy), 0, 255).astype(np.uint8)
    mag_disp = np.clip(np.round(magnitude), 0, 255).astype(np.uint8)
    dir_disp = np.clip(np.round((direction / 180.0) * 255.0), 0, 255).astype(np.uint8)
    
    return {
        "gx_raw": gx,
        "gy_raw": gy,
        "magnitude_raw": magnitude,
        "direction_raw": direction,
        "gx_display": gx_disp,
        "gy_display": gy_disp,
        "magnitude_display": mag_disp,
        "direction_display": dir_disp
    }


def compute_laplacian_edges(gray: np.ndarray, connectivity: int = 4) -> Dict[str, np.ndarray]:
    """
    Calculates 2nd derivative Laplacian operator.
    Highlights areas of rapid intensity transitions.
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
        
    if connectivity == 8:
        kernel = np.array([[1, 1, 1], [1, -8, 1], [1, 1, 1]], dtype=float)
    else:
        kernel = np.array([[0, 1, 0], [1, -4, 1], [0, 1, 0]], dtype=float)
        
    h, w = gray.shape
    pad_img = np.pad(gray.astype(float), ((1, 1), (1, 1)), mode='edge')
    lap = np.zeros_like(gray, dtype=float)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + 3, c : c + 3]
            lap[r, c] = np.sum(win * kernel)
            
    # Zero crossings / absolute display
    lap_disp = np.clip(np.abs(lap), 0, 255).astype(np.uint8)
    return {
        "laplacian_raw": lap,
        "laplacian_display": lap_disp
    }


def canny_edge_detection_stages(
    gray: np.ndarray,
    low_threshold: int = 50,
    high_threshold: int = 150,
    sigma: float = 1.0
) -> Dict[str, Any]:
    """
    Complete 5-Stage Canny Edge Detector:
      Stage 1: Gaussian Smoothing (Low-pass noise reduction)
      Stage 2: Gradient Computation (Sobel magnitude and quantized angles)
      Stage 3: Non-Maximum Suppression (Thinning along gradient direction)
      Stage 4: Double Thresholding (Separates strong, weak, and non-edge pixels)
      Stage 5: Edge Tracking by Hysteresis (Keeps weak edges connected to strong edges)
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
        
    h, w = gray.shape
    
    # Stage 1: Gaussian Smoothing
    from .filters import apply_gaussian_filter
    stage1_blur = apply_gaussian_filter(gray, sigma=sigma, k_size=5)
    
    # Stage 2: Gradient Computation
    grads = compute_gradient_operators(stage1_blur, operator='sobel')
    mag = grads["magnitude_raw"]
    angle = grads["direction_raw"]
    stage2_mag_disp = grads["magnitude_display"]
    
    # Stage 3: Non-Maximum Suppression (NMS)
    nms = np.zeros((h, w), dtype=float)
    pad_mag = np.pad(mag, ((1, 1), (1, 1)), mode='constant')
    
    for r in range(h):
        for c in range(w):
            theta = angle[r, c]
            pr = r + 1
            pc = c + 1
            val = pad_mag[pr, pc]
            
            # Quantize angle into 4 principal directions (0, 45, 90, 135 deg)
            if (0 <= theta < 22.5) or (157.5 <= theta <= 180):
                # Horizontal gradient -> check left and right
                q = pad_mag[pr, pc + 1]
                p = pad_mag[pr, pc - 1]
            elif 22.5 <= theta < 67.5:
                # 45 deg diagonal -> check top-right and bottom-left
                q = pad_mag[pr - 1, pc + 1]
                p = pad_mag[pr + 1, pc - 1]
            elif 67.5 <= theta < 112.5:
                # Vertical gradient -> check top and bottom
                q = pad_mag[pr - 1, pc]
                p = pad_mag[pr + 1, pc]
            else:  # 112.5 <= theta < 157.5
                # 135 deg diagonal -> check top-left and bottom-right
                q = pad_mag[pr - 1, pc - 1]
                p = pad_mag[pr + 1, pc + 1]
                
            if val >= q and val >= p:
                nms[r, c] = val
            else:
                nms[r, c] = 0
                
    stage3_nms_disp = np.clip(np.round(nms), 0, 255).astype(np.uint8)
    
    # Stage 4: Double Thresholding
    res = np.zeros((h, w), dtype=np.uint8)
    strong_val = 255
    weak_val = 75
    
    strong_r, strong_c = np.where(nms >= high_threshold)
    weak_r, weak_c = np.where((nms >= low_threshold) & (nms < high_threshold))
    
    res[strong_r, strong_c] = strong_val
    res[weak_r, weak_c] = weak_val
    stage4_threshold_disp = res.copy()
    
    # Stage 5: Edge Tracking by Hysteresis (8-connectivity)
    hysteresis = np.zeros((h, w), dtype=np.uint8)
    hysteresis[strong_r, strong_c] = 255
    
    # Queue for breadth-first flood-fill of connected weak edges
    queue = list(zip(strong_r.tolist(), strong_c.tolist()))
    visited = set(queue)
    
    while queue:
        cr, cc = queue.pop(0)
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                if dr == 0 and dc == 0:
                    continue
                nr, nc = cr + dr, cc + dc
                if 0 <= nr < h and 0 <= nc < w:
                    if (nr, nc) not in visited and res[nr, nc] == weak_val:
                        hysteresis[nr, nc] = 255
                        visited.add((nr, nc))
                        queue.append((nr, nc))
                        
    stage5_final_edges = hysteresis
    
    return {
        "stage1_blurred": stage1_blur,
        "stage2_magnitude": stage2_mag_disp,
        "stage3_nms": stage3_nms_disp,
        "stage4_threshold": stage4_threshold_disp,
        "stage5_final": stage5_final_edges,
        "metrics": {
            "low_threshold": low_threshold,
            "high_threshold": high_threshold,
            "strong_pixels": len(strong_r),
            "weak_pixels": len(weak_r),
            "retained_edge_pixels": int(np.sum(stage5_final_edges == 255))
        }
    }
