"""
Histograms and Histogram Equalisation
====================================
Implements histogram analysis, distribution interpretation, and the complete
6-stage Discrete Histogram Equalisation pipeline.
"""

import numpy as np
from typing import Dict, Any, List, Tuple


def compute_histogram(arr: np.ndarray) -> Dict[str, Any]:
    """
    Computes intensity histograms and statistics for grayscale or RGB image.
    """
    stats = {}
    
    if arr.ndim == 2:
        hist, _ = np.histogram(arr, bins=256, range=(0, 256))
        total_pixels = arr.size
        mean_val = float(np.mean(arr))
        std_val = float(np.std(arr))
        min_val = int(np.min(arr))
        max_val = int(np.max(arr))
        
        # Characteristic interpretation (Unit 1 Slide 28)
        if mean_val < 85:
            dist_desc = "Dark Image (intensities concentrated on left)"
        elif mean_val > 170:
            dist_desc = "Bright Image (intensities concentrated on right)"
        elif std_val < 35:
            dist_desc = "Low Contrast (narrow, clustered intensity peak)"
        else:
            dist_desc = "High / Well-Balanced Contrast (intensities spread widely)"
            
        return {
            "type": "grayscale",
            "histogram": hist.tolist(),
            "mean": round(mean_val, 2),
            "std": round(std_val, 2),
            "min": min_val,
            "max": max_val,
            "total_pixels": total_pixels,
            "interpretation": dist_desc
        }
    else:
        # RGB 3 channels
        hist_r, _ = np.histogram(arr[:, :, 0], bins=256, range=(0, 256))
        hist_g, _ = np.histogram(arr[:, :, 1], bins=256, range=(0, 256))
        hist_b, _ = np.histogram(arr[:, :, 2], bins=256, range=(0, 256))
        
        return {
            "type": "rgb",
            "red": hist_r.tolist(),
            "green": hist_g.tolist(),
            "blue": hist_b.tolist(),
            "mean_r": round(float(np.mean(arr[:, :, 0])), 2),
            "mean_g": round(float(np.mean(arr[:, :, 1])), 2),
            "mean_b": round(float(np.mean(arr[:, :, 2])), 2),
            "total_pixels": arr[:, :, 0].size
        }


def histogram_equalization(gray: np.ndarray) -> Dict[str, Any]:
    """
    Step-by-step Histogram Equalisation (Unit 1 Slide 28):
      Stage 1: Calculate raw frequency histogram n_k.
      Stage 2: Calculate normalized probabilities p(r_k) = n_k / N.
      Stage 3: Calculate Cumulative Distribution Function (CDF): c(k) = sum_{j=0}^k p(r_j).
      Stage 4: Construct intensity mapping: s_k = round((L - 1) * c(k)).
      Stage 5: Apply mapping to produce equalized image.
      Stage 6: Calculate output histogram and output CDF for comparison.
    """
    if gray.ndim == 3:
        # Convert to grayscale first
        from .conversions import rgb_to_grayscale
        gray = rgb_to_grayscale(gray)
        
    h, w = gray.shape
    total_pixels = h * w
    L = 256
    
    # 1. Frequency histogram n_k
    n_k, _ = np.histogram(gray, bins=L, range=(0, L))
    
    # 2. Probability p(r_k)
    p_k = n_k.astype(float) / total_pixels
    
    # 3. Cumulative Distribution Function CDF(k)
    cdf = np.cumsum(p_k)
    
    # 4. Intensity mapping s_k
    s_k = np.round((L - 1) * cdf).astype(np.uint8)
    
    # 5. Apply mapping to image
    equalized_img = s_k[gray]
    
    # 6. Output histogram and output CDF
    out_hist, _ = np.histogram(equalized_img, bins=L, range=(0, L))
    out_cdf = np.cumsum(out_hist.astype(float) / total_pixels)
    
    # Sample 16 key representative steps for numerical table display
    sample_indices = list(range(0, 256, 16)) + [255]
    table_sample = []
    for k in sample_indices:
        table_sample.append({
            "intensity_k": int(k),
            "count_nk": int(n_k[k]),
            "prob_pk": round(float(p_k[k]), 5),
            "cdf_k": round(float(cdf[k]), 4),
            "mapped_sk": int(s_k[k])
        })
        
    return {
        "equalized_image": equalized_img,
        "input_histogram": n_k.tolist(),
        "input_cdf": cdf.tolist(),
        "output_histogram": out_hist.tolist(),
        "output_cdf": out_cdf.tolist(),
        "mapping_lut": s_k.tolist(),
        "stages_data": table_sample,
        "input_metrics": {
            "mean": round(float(np.mean(gray)), 2),
            "std": round(float(np.std(gray)), 2),
            "min": int(np.min(gray)),
            "max": int(np.max(gray))
        },
        "output_metrics": {
            "mean": round(float(np.mean(equalized_img)), 2),
            "std": round(float(np.std(equalized_img)), 2),
            "min": int(np.min(equalized_img)),
            "max": int(np.max(equalized_img))
        }
    }
