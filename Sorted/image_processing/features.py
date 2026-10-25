"""
Local Image Descriptors: Harris Corner Detector & SIFT
======================================================
Implements feature detection and local image descriptors:
- Harris Corner Detector:
  Gradients -> Structure Tensor M -> Corner Response R = det(M) - k*trace(M)^2 -> NMS
- Scale-Invariant Feature Transform (SIFT):
  Scale-space DoG extrema -> Keypoint localization -> Orientation -> 128-dim Descriptors
  Two-image matching with Lowe's ratio test.
"""

import numpy as np
from typing import Dict, Any, List, Tuple, Optional
from .conversions import rgb_to_grayscale
from .edges import SOBEL_X, SOBEL_Y

try:
    import cv2
    HAS_CV2 = True
    HAS_SIFT = hasattr(cv2, 'SIFT_create')
except ImportError:
    HAS_CV2 = False
    HAS_SIFT = False


def harris_corner_detector(
    img: np.ndarray,
    k: float = 0.04,
    threshold_ratio: float = 0.01,
    gaussian_sigma: float = 1.0,
    nms_radius: int = 3
) -> Dict[str, Any]:
    """
    Harris Corner Detector Architecture:
      1. Convert to grayscale.
      2. Compute spatial image gradients Ix, Iy.
      3. Compute products of derivatives: Ix^2, Iy^2, Ix*Iy.
      4. Apply Gaussian smoothing to form components of structure tensor M:
           M = [[Sxx, Sxy], [Sxy, Syy]]
      5. Compute corner response function R:
           det(M) = Sxx * Syy - Sxy^2
           trace(M) = Sxx + Syy
           R = det(M) - k * (trace(M))^2
      6. Threshold and Non-Maximum Suppression to detect distinct corner points.
    """
    if img.ndim == 3:
        gray = rgb_to_grayscale(img)
    else:
        gray = img.copy()
        
    h, w = gray.shape
    gray_f = gray.astype(float)
    
    # 2. Gradients using Sobel
    pad_img = np.pad(gray_f, ((1, 1), (1, 1)), mode='edge')
    ix = np.zeros((h, w), dtype=float)
    iy = np.zeros((h, w), dtype=float)
    
    for r in range(h):
        for c in range(w):
            win = pad_img[r : r + 3, c : c + 3]
            ix[r, c] = np.sum(win * SOBEL_X)
            iy[r, c] = np.sum(win * SOBEL_Y)
            
    # 3. Gradient products
    ix2 = ix ** 2
    iy2 = iy ** 2
    ixiy = ix * iy
    
    # 4. Gaussian smoothing of structure tensor (in float domain to preserve precision)
    if HAS_CV2:
        sxx = cv2.GaussianBlur(ix2, (3, 3), gaussian_sigma)
        syy = cv2.GaussianBlur(iy2, (3, 3), gaussian_sigma)
        sxy = cv2.GaussianBlur(ixiy, (3, 3), gaussian_sigma)
    else:
        rad = 1
        y_g, x_g = np.mgrid[-rad:rad+1, -rad:rad+1]
        g_kernel = np.exp(-(x_g**2 + y_g**2) / (2.0 * gaussian_sigma**2))
        g_kernel /= np.sum(g_kernel)
        
        pad_ix2 = np.pad(ix2, ((1, 1), (1, 1)), mode='reflect')
        pad_iy2 = np.pad(iy2, ((1, 1), (1, 1)), mode='reflect')
        pad_ixiy = np.pad(ixiy, ((1, 1), (1, 1)), mode='reflect')
        sxx = np.zeros((h, w), dtype=float)
        syy = np.zeros((h, w), dtype=float)
        sxy = np.zeros((h, w), dtype=float)
        for r in range(h):
            for c in range(w):
                sxx[r, c] = np.sum(pad_ix2[r:r+3, c:c+3] * g_kernel)
                syy[r, c] = np.sum(pad_iy2[r:r+3, c:c+3] * g_kernel)
                sxy[r, c] = np.sum(pad_ixiy[r:r+3, c:c+3] * g_kernel)
    
    # 5. Harris Corner Response R
    det_m = (sxx * syy) - (sxy ** 2)
    trace_m = sxx + syy
    r_response = det_m - k * (trace_m ** 2)
    
    # 6. Thresholding
    r_max = np.max(r_response)
    threshold = max(0.0, r_max * threshold_ratio)
    
    # Non-maximum suppression in local window
    corners = []
    pad_r = np.pad(r_response, ((nms_radius, nms_radius), (nms_radius, nms_radius)), mode='constant', constant_values=-1e9)
    
    for r in range(h):
        for c in range(w):
            val = r_response[r, c]
            if val > threshold:
                pr = r + nms_radius
                pc = c + nms_radius
                local_window = pad_r[pr - nms_radius : pr + nms_radius + 1, pc - nms_radius : pc + nms_radius + 1]
                if val == np.max(local_window):
                    corners.append({
                        "x": int(c),
                        "y": int(r),
                        "response": round(float(val), 2)
                    })
                    
    # Generate overlay image with red markers
    overlay = img.copy() if img.ndim == 3 else np.stack([gray, gray, gray], axis=2)
    for pt in corners:
        cx, cy = pt["x"], pt["y"]
        for dr in range(-2, 3):
            for dc in range(-2, 3):
                if 0 <= cy + dr < h and 0 <= cx + dc < w:
                    if dr**2 + dc**2 <= 5:
                        overlay[cy + dr, cx + dc] = [255, 50, 50] # Bright red corner marker
                        
    # Normalize response for visual display
    norm_r = np.clip(np.round((np.maximum(0, r_response) / max(1.0, r_max)) * 255), 0, 255).astype(np.uint8)
    
    return {
        "num_corners": len(corners),
        "corners": corners,
        "response_map": norm_r,
        "overlay_image": overlay,
        "k_factor": k,
        "threshold": round(float(threshold), 2)
    }


def is_sift_available() -> bool:
    """Checks whether OpenCV SIFT is available in current environment."""
    return HAS_SIFT


def sift_detect_keypoints(img: np.ndarray, max_keypoints: int = 50) -> Dict[str, Any]:
    """
    Extracts SIFT keypoints and 128-dimensional descriptors (Slides 61-71):
      - Scale-space Difference of Gaussians (DoG)
      - Sub-pixel keypoint localization
      - Orientation assignment from local gradient histogram
      - 128-D descriptor computation from 4x4 sub-blocks
    """
    if not HAS_SIFT:
        return {
            "available": False,
            "message": "OpenCV SIFT algorithm is not available in the current environment.",
            "keypoints": []
        }
        
    if img.ndim == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    else:
        gray = img
        
    sift = cv2.SIFT_create(nfeatures=max_keypoints)
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    # Draw keypoints with scale circles and orientation rays
    rgb_base = img.copy() if img.ndim == 3 else cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)
    kp_drawn = cv2.drawKeypoints(rgb_base, keypoints, None, flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    
    kp_list = []
    for kp in keypoints:
        kp_list.append({
            "x": round(float(kp.pt[0]), 1),
            "y": round(float(kp.pt[1]), 1),
            "size": round(float(kp.size), 2),
            "angle": round(float(kp.angle), 1),
            "response": round(float(kp.response), 4),
            "octave": int(kp.octave)
        })
        
    return {
        "available": True,
        "num_keypoints": len(keypoints),
        "keypoints": kp_list,
        "overlay_image": kp_drawn,
        "descriptor_shape": list(descriptors.shape) if descriptors is not None else [0, 128]
    }


def sift_match_images(img1: np.ndarray, img2: np.ndarray, max_matches: int = 30) -> Dict[str, Any]:
    """
    Matches SIFT feature descriptors between two images using FLANN/BFMatcher
    and Lowe's distance ratio test (Feature Vector Matching).
    """
    if not HAS_SIFT:
        return {
            "available": False,
            "message": "SIFT is not available."
        }
        
    g1 = cv2.cvtColor(img1, cv2.COLOR_RGB2GRAY) if img1.ndim == 3 else img1
    g2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY) if img2.ndim == 3 else img2
    
    sift = cv2.SIFT_create(nfeatures=150)
    kp1, des1 = sift.detectAndCompute(g1, None)
    kp2, des2 = sift.detectAndCompute(g2, None)
    
    if des1 is None or des2 is None or len(kp1) < 2 or len(kp2) < 2:
        return {
            "available": True,
            "num_matches": 0,
            "message": "Insufficient feature keypoints detected to establish matching pairs."
        }
        
    # BFMatcher with default params
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(des1, des2, k=2)
    
    # Apply Lowe's ratio test
    good_matches = []
    for m, n in matches:
        if m.distance < 0.75 * n.distance:
            good_matches.append(m)
            
    good_matches = sorted(good_matches, key=lambda x: x.distance)[:max_matches]
    
    # Draw matched lines
    rgb1 = img1 if img1.ndim == 3 else cv2.cvtColor(g1, cv2.COLOR_GRAY2RGB)
    rgb2 = img2 if img2.ndim == 3 else cv2.cvtColor(g2, cv2.COLOR_GRAY2RGB)
    match_img = cv2.drawMatches(rgb1, kp1, rgb2, kp2, good_matches, None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    
    return {
        "available": True,
        "num_matches": len(good_matches),
        "keypoints_img1": len(kp1),
        "keypoints_img2": len(kp2),
        "matched_image": match_img
    }
