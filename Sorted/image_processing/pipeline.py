"""
Image Processing Pipeline Builder
=================================
Executes multi-stage sequential pipelines:
e.g. Upload -> Grayscale -> Gaussian Filter -> Contrast Stretch -> Sobel/Canny -> Morphology
Tracks intermediate stage outputs, dimensions, statistics, and handles format conversions.
"""

import time
import numpy as np
from typing import Dict, Any, List, Optional
from .conversions import rgb_to_grayscale, grayscale_to_binary, apply_sampling, apply_quantization
from .intensity import transform_negative, transform_gamma, transform_contrast_stretch, transform_brightness_contrast
from .histograms import histogram_equalization
from .filters import apply_gaussian_filter, apply_median_filter, apply_box_filter, apply_unsharp_masking
from .edges import compute_gradient_operators, canny_edge_detection_stages, compute_laplacian_edges
from .morphology import binary_erosion, binary_dilation, binary_opening, binary_closing, STRUCTURING_ELEMENTS
from .segmentation import global_threshold, adaptive_threshold, otsu_threshold, connected_components_analysis


def execute_pipeline_step(img: np.ndarray, op_name: str, params: Dict[str, Any]) -> Tuple[np.ndarray, str]:
    """
    Executes a single pipeline operation on an image matrix.
    Returns (result_image, status_message).
    """
    op = op_name.lower()
    
    # --- Conversions ---
    if op == 'grayscale':
        return rgb_to_grayscale(img, method=params.get('method', 'luminosity')), "Converted to 8-bit Grayscale"
        
    elif op == 'binary' or op == 'threshold':
        thresh = int(params.get('threshold', 128))
        return grayscale_to_binary(img, threshold=thresh), f"Binarized at threshold {thresh}"
        
    elif op == 'sampling':
        factor = int(params.get('factor', 4))
        return apply_sampling(img, factor=factor), f"Sampled at 1/{factor} resolution"
        
    elif op == 'quantization':
        bits = int(params.get('bits', 4))
        return apply_quantization(img, bits=bits), f"Quantized to {2**bits} intensity levels"
        
    # --- Intensity Transformations ---
    elif op == 'negative':
        out, _ = transform_negative(img)
        return out, "Inverted image intensities (Negative)"
        
    elif op == 'gamma':
        gamma = float(params.get('gamma', 1.5))
        out, _ = transform_gamma(img, gamma=gamma)
        return out, f"Power-law gamma transform (gamma={gamma})"
        
    elif op == 'contrast_stretch':
        r1 = int(params.get('r1', 70))
        s1 = int(params.get('s1', 20))
        r2 = int(params.get('r2', 180))
        s2 = int(params.get('s2', 230))
        out, _ = transform_contrast_stretch(img, r1, s1, r2, s2)
        return out, "Piecewise linear contrast stretching applied"
        
    elif op == 'brightness_contrast':
        alpha = float(params.get('alpha', 1.2))
        beta = float(params.get('beta', 10.0))
        out, _ = transform_brightness_contrast(img, alpha=alpha, beta=beta)
        return out, f"Brightness & Contrast adjusted (alpha={alpha}, beta={beta})"
        
    elif op == 'hist_eq':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        res = histogram_equalization(gray)
        return res["equalized_image"], "Histogram equalisation applied across full dynamic range"
        
    # --- Spatial Smoothing & Sharpening ---
    elif op == 'box_blur':
        k = int(params.get('k_size', 3))
        return apply_box_filter(img, k_size=k), f"Mean/Box blur filter ({k}x{k})"
        
    elif op == 'gaussian_blur':
        sigma = float(params.get('sigma', 1.0))
        k = int(params.get('k_size', 5))
        return apply_gaussian_filter(img, sigma=sigma, k_size=k), f"Gaussian blur (sigma={sigma})"
        
    elif op == 'median_filter':
        k = int(params.get('k_size', 3))
        return apply_median_filter(img, k_size=k), f"Median filter ({k}x{k}) for noise removal"
        
    elif op == 'unsharp_mask':
        k_factor = float(params.get('k', 1.0))
        sharp, _ = apply_unsharp_masking(img, k=k_factor)
        return sharp, f"Unsharp masking sharpening (k={k_factor})"
        
    # --- Edge Detection ---
    elif op == 'sobel':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        grads = compute_gradient_operators(gray, operator='sobel')
        return grads["magnitude_display"], "Sobel gradient magnitude edge detection"
        
    elif op == 'prewitt':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        grads = compute_gradient_operators(gray, operator='prewitt')
        return grads["magnitude_display"], "Prewitt gradient magnitude edge detection"
        
    elif op == 'laplacian':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        laps = compute_laplacian_edges(gray, connectivity=int(params.get('connectivity', 4)))
        return laps["laplacian_display"], "Laplacian 2nd derivative edge detection"
        
    elif op == 'canny':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        low = int(params.get('low_threshold', 50))
        high = int(params.get('high_threshold', 150))
        canny_res = canny_edge_detection_stages(gray, low_threshold=low, high_threshold=high)
        return canny_res["stage5_final"], f"Canny edge detector (low={low}, high={high})"
        
    # --- Morphology ---
    elif op in ('erosion', 'dilation', 'opening', 'closing'):
        # Ensure image is binary
        if img.ndim == 3:
            gray = rgb_to_grayscale(img)
            bin_img = grayscale_to_binary(gray, 128)
        elif len(np.unique(img)) > 2:
            bin_img = grayscale_to_binary(img, 128)
        else:
            bin_img = img
            
        se_key = params.get('structuring_element', 'square_3x3')
        se = STRUCTURING_ELEMENTS.get(se_key, STRUCTURING_ELEMENTS['square_3x3'])
        
        if op == 'erosion':
            return binary_erosion(bin_img, se), f"Binary erosion ({se_key})"
        elif op == 'dilation':
            return binary_dilation(bin_img, se), f"Binary dilation ({se_key})"
        elif op == 'opening':
            return binary_opening(bin_img, se), f"Binary opening ({se_key})"
        elif op == 'closing':
            return binary_closing(bin_img, se), f"Binary closing ({se_key})"
            
    # --- Segmentation ---
    elif op == 'otsu':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        otsu_res = otsu_threshold(gray)
        return otsu_res["binary_image"], f"Otsu optimal thresholding (T*={otsu_res['optimal_threshold']})"
        
    elif op == 'adaptive_thresh':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        blk = int(params.get('block_size', 11))
        return adaptive_threshold(gray, block_size=blk), f"Adaptive local thresholding (block={blk})"
        
    elif op == 'connected_components':
        gray = rgb_to_grayscale(img) if img.ndim == 3 else img
        bin_img = grayscale_to_binary(gray, 128) if len(np.unique(gray)) > 2 else gray
        cca_res = connected_components_analysis(bin_img, connectivity=int(params.get('connectivity', 8)))
        return cca_res["color_visualization"], f"Connected components ({cca_res['num_components']} labeled regions)"
        
    else:
        return img.copy(), f"Passthrough / Unknown operation: {op_name}"


def run_image_pipeline(input_image: np.ndarray, stages: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Executes an ordered pipeline of processing stages sequentially.
    Tracks intermediate stage images and metrics without mutating input.
    """
    current_img = input_image.copy()
    stage_results = []
    
    # Stage 0: Initial input
    h, w = current_img.shape[:2]
    c = 1 if current_img.ndim == 2 else current_img.shape[2]
    stage_results.append({
        "stage_index": 0,
        "name": "Initial Source Image",
        "description": "Original unmanipulated input",
        "image": current_img.copy(),
        "dimensions": [w, h],
        "channels": c,
        "time_ms": 0.0
    })
    
    for idx, stage in enumerate(stages, start=1):
        op_name = stage.get("op", "grayscale")
        params = stage.get("params", {})
        
        t0 = time.perf_counter()
        next_img, desc = execute_pipeline_step(current_img, op_name, params)
        elapsed_ms = round((time.perf_counter() - t0) * 1000.0, 2)
        
        h_s, w_s = next_img.shape[:2]
        c_s = 1 if next_img.ndim == 2 else next_img.shape[2]
        
        stage_results.append({
            "stage_index": idx,
            "name": op_name,
            "description": desc,
            "params": params,
            "image": next_img.copy(),
            "dimensions": [w_s, h_s],
            "channels": c_s,
            "time_ms": elapsed_ms
        })
        
        current_img = next_img
        
    total_time = sum(s["time_ms"] for s in stage_results)
    
    return {
        "num_stages": len(stages),
        "total_time_ms": round(total_time, 2),
        "final_image": current_img,
        "stages": stage_results
    }
