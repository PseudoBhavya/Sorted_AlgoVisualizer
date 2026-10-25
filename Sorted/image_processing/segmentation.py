"""
Image Segmentation & Connected Component Analysis
=================================================
Implements image thresholding and region segmentation:
- Global Binary Thresholding
- Adaptive Local Thresholding
- Otsu's Optimal Between-Class Variance Thresholding
- Connected Component Analysis (CCA) with 4- and 8-connectivity (Unit 1 Slide 31)
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from .conversions import rgb_to_grayscale


def global_threshold(gray: np.ndarray, thresh: int = 128) -> np.ndarray:
    """Basic global thresholding: s = 255 if r >= thresh else 0."""
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
    return np.where(gray >= thresh, 255, 0).astype(np.uint8)


def adaptive_threshold(gray: np.ndarray, block_size: int = 11, c_offset: int = 2) -> np.ndarray:
    """
    Local Adaptive Thresholding:
    Calculates threshold for each pixel based on mean of local block_size x block_size neighbourhood minus c_offset.
    Robust to non-uniform illumination and lighting gradients.
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
        
    h, w = gray.shape
    rad = block_size // 2
    pad_img = np.pad(gray.astype(float), ((rad, rad), (rad, rad)), mode='edge')
    out = np.zeros((h, w), dtype=np.uint8)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + block_size, c : c + block_size]
            local_thresh = np.mean(win) - c_offset
            if gray[r, c] >= local_thresh:
                out[r, c] = 255
            else:
                out[r, c] = 0
                
    return out


def otsu_threshold(gray: np.ndarray) -> Dict[str, Any]:
    """
    Otsu's Thresholding:
    Automatically calculates optimal threshold T* that maximizes between-class variance:
      sigma_b^2(t) = w0(t) * w1(t) * (mu0(t) - mu1(t))^2
    where w0, w1 are probabilities of background and foreground classes,
    and mu0, mu1 are the class means.
    """
    if gray.ndim == 3:
        gray = rgb_to_grayscale(gray)
        
    total_pixels = gray.size
    hist, _ = np.histogram(gray, bins=256, range=(0, 256))
    prob = hist.astype(float) / total_pixels
    
    # Cumulative sums
    q = np.cumsum(prob)
    # Intensity sums
    m = np.cumsum(prob * np.arange(256))
    global_mean = m[-1]
    
    variances = np.zeros(256, dtype=float)
    
    for t in range(256):
        w0 = q[t]
        w1 = 1.0 - w0
        
        if w0 < 1e-6 or w1 < 1e-6:
            continue
            
        mu0 = m[t] / w0
        mu1 = (global_mean - m[t]) / w1
        
        variances[t] = w0 * w1 * ((mu0 - mu1) ** 2)
        
    max_var = np.max(variances)
    candidates = np.where(np.isclose(variances, max_var, rtol=1e-5))[0]
    optimal_t = int(np.round(np.mean(candidates))) if len(candidates) > 0 else 128
    binary_img = np.where(gray >= optimal_t, 255, 0).astype(np.uint8)
    
    return {
        "optimal_threshold": optimal_t,
        "max_variance": round(float(variances[optimal_t]), 4),
        "variance_curve": np.round(variances, 4).tolist(),
        "binary_image": binary_img,
        "histogram": hist.tolist()
    }


def connected_components_analysis(binary_img: np.ndarray, connectivity: int = 8) -> Dict[str, Any]:
    """
    Connected Component Analysis (CCA) using two-pass or flood-fill labeling.
    Supports 4-neighborhood (N4) and 8-neighborhood (N8) as taught in Unit 1 Slide 31.
    Computes area, bounding box, and centroid for each distinct object.
    """
    if binary_img.ndim == 3:
        binary_img = rgb_to_grayscale(binary_img)
    binary_mask = (binary_img > 128)
    
    h, w = binary_img.shape
    labeled = np.zeros((h, w), dtype=int)
    current_label = 0
    
    # Offsets based on connectivity
    if connectivity == 4:
        neighbors = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    else:  # 8-connectivity
        neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        
    visited = np.zeros((h, w), dtype=bool)
    components = []
    
    # Breadth-first flood fill labeling
    for r in range(h):
        for c in range(w):
            if binary_mask[r, c] and not visited[r, c]:
                current_label += 1
                queue = [(r, c)]
                visited[r, c] = True
                labeled[r, c] = current_label
                
                coords = [(r, c)]
                
                while queue:
                    cr, cc = queue.pop(0)
                    for dr, dc in neighbors:
                        nr, nc = cr + dr, cc + dc
                        if 0 <= nr < h and 0 <= nc < w:
                            if binary_mask[nr, nc] and not visited[nr, nc]:
                                visited[nr, nc] = True
                                labeled[nr, nc] = current_label
                                queue.append((nr, nc))
                                coords.append((nr, nc))
                                
                coords_arr = np.array(coords)
                min_r, min_c = np.min(coords_arr, axis=0)
                max_r, max_c = np.max(coords_arr, axis=0)
                area = len(coords)
                centroid_r = float(np.mean(coords_arr[:, 0]))
                centroid_c = float(np.mean(coords_arr[:, 1]))
                
                components.append({
                    "label": current_label,
                    "area": int(area),
                    "bbox": [int(min_c), int(min_r), int(max_c - min_c + 1), int(max_r - min_r + 1)], # [x, y, w, h]
                    "centroid": [round(centroid_c, 1), round(centroid_r, 1)]
                })
                
    # Sort components descending by area
    components.sort(key=lambda x: x["area"], reverse=True)
    
    # Generate colorful RGB visualization
    color_map = np.zeros((h, w, 3), dtype=np.uint8)
    np.random.seed(42)
    colors = np.random.randint(50, 240, (max(1, current_label) + 1, 3), dtype=np.uint8)
    # Background is dark slate
    colors[0] = [15, 20, 32]
    
    for lbl in range(1, current_label + 1):
        color_map[labeled == lbl] = colors[lbl]
        
    return {
        "num_components": current_label,
        "connectivity": connectivity,
        "components": components,
        "labeled_mask": labeled,
        "color_visualization": color_map
    }
