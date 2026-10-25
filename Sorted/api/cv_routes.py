"""
Flask REST API Endpoints for Computer Vision & DIP Workspace
============================================================
Provides RESTful endpoints for image processing, transformations,
filtering, edge detection, morphology, segmentation, features, and PCA.
"""

from flask import Blueprint, request, jsonify
import numpy as np
from typing import Dict, Any

from Sorted.image_processing.image_io import (
    decode_image_base64, encode_image_base64, generate_sample_pattern, get_image_metadata
)
from Sorted.image_processing.conversions import (
    apply_sampling, apply_quantization, rgb_to_grayscale, grayscale_to_binary,
    rgb_to_hsv, hsv_to_rgb, separate_rgb_channels, hsv_color_mask, swap_rgb_bgr
)
from Sorted.image_processing.intensity import (
    transform_negative, transform_logarithmic, transform_gamma,
    transform_contrast_stretch, transform_intensity_slicing,
    transform_brightness_contrast, transform_normalize
)
from Sorted.image_processing.histograms import compute_histogram, histogram_equalization
from Sorted.image_processing.kernels import (
    KERNEL_PRESETS, compute_kernel_step, apply_spatial_filter, calculate_output_dimensions
)
from Sorted.image_processing.filters import (
    add_gaussian_noise, add_salt_and_pepper_noise, add_speckle_noise, add_poisson_noise,
    calculate_restoration_metrics, apply_box_filter, apply_gaussian_filter,
    apply_median_filter, apply_min_filter, apply_max_filter, apply_bilateral_filter,
    apply_unsharp_masking
)
from Sorted.image_processing.edges import (
    compute_gradient_operators, compute_laplacian_edges, canny_edge_detection_stages
)
from Sorted.image_processing.morphology import (
    binary_erosion, binary_dilation, binary_opening, binary_closing,
    morphological_gradient, STRUCTURING_ELEMENTS
)
from Sorted.image_processing.segmentation import (
    global_threshold, adaptive_threshold, otsu_threshold, connected_components_analysis
)
from Sorted.image_processing.features import (
    harris_corner_detector, is_sift_available, sift_detect_keypoints, sift_match_images
)
from Sorted.image_processing.pca import pca_teaching_matrix_example, pca_image_denoise
from Sorted.image_processing.pipeline import run_image_pipeline
from Sorted.image_processing.schemas import serialize_image_response

cv_bp = Blueprint('cv', __name__, url_prefix='/api/cv')


def _get_input_array_from_request(req_json: Dict[str, Any]) -> np.ndarray:
    """Helper to decode base64 image or fetch sample pattern."""
    if 'image_data' in req_json and req_json['image_data']:
        return decode_image_base64(req_json['image_data'], max_dim=512)
    elif 'matrix' in req_json and req_json['matrix']:
        return np.array(req_json['matrix'], dtype=np.uint8)
    else:
        pattern = req_json.get('pattern', 'shapes')
        return generate_sample_pattern(name=pattern, size=128)


@cv_bp.route('/info', methods=['GET'])
def cv_info():
    """Returns capability status and preset metadata."""
    return jsonify({
        "status": "healthy",
        "service": "Sorted Computer Vision & DIP Engine",
        "sift_available": is_sift_available(),
        "kernel_presets": {k: {"name": v["name"], "category": v["category"], "type": v["type"], "description": v["description"]} for k, v in KERNEL_PRESETS.items()},
        "patterns": ["shapes", "checkerboard", "gradient", "mri_brain", "coins"]
    }), 200


@cv_bp.route('/sample/<name>', methods=['GET'])
def get_sample_image(name: str):
    """Returns a base64 encoded educational sample pattern."""
    size = int(request.args.get('size', 128))
    size = max(16, min(512, size))
    arr = generate_sample_pattern(name=name, size=size)
    return jsonify(serialize_image_response(arr, extra_data={"pattern_name": name})), 200


@cv_bp.route('/convert', methods=['POST'])
def convert_image():
    """Handles color conversions, sampling, and quantization."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    op = data.get('operation', 'grayscale')
    
    extra = {"operation": op}
    
    if op == 'sampling':
        factor = int(data.get('factor', 4))
        res = apply_sampling(arr, factor=factor)
        extra["factor"] = factor
    elif op == 'quantization':
        bits = int(data.get('bits', 4))
        res = apply_quantization(arr, bits=bits)
        extra["bits"] = bits
        extra["levels"] = 2 ** bits
    elif op == 'grayscale':
        method = data.get('method', 'luminosity')
        res = rgb_to_grayscale(arr, method=method)
        extra["method"] = method
        extra["formula"] = "Y = 0.299*R + 0.587*G + 0.114*B" if method == 'luminosity' else "Y = (R+G+B)/3"
    elif op == 'binary':
        thresh = int(data.get('threshold', 128))
        res = grayscale_to_binary(arr, threshold=thresh)
        extra["threshold"] = thresh
    elif op == 'hsv_mask':
        h_min = float(data.get('h_min', 0))
        h_max = float(data.get('h_max', 360))
        s_min = float(data.get('s_min', 20))
        s_max = float(data.get('s_max', 100))
        v_min = float(data.get('v_min', 20))
        v_max = float(data.get('v_max', 100))
        mask, masked_rgb = hsv_color_mask(arr, h_min, h_max, s_min, s_max, v_min, v_max)
        res = masked_rgb
        extra["binary_mask"] = encode_image_base64(mask, format='png')
    elif op == 'bgr_swap':
        res = swap_rgb_bgr(arr)
        extra["notice"] = "Red and Blue channels swapped (OpenCV BGR simulation)"
    elif op == 'channels':
        chans = separate_rgb_channels(arr)
        return jsonify({
            "status": "success",
            "red_gray": encode_image_base64(chans["red_gray"], format='png'),
            "green_gray": encode_image_base64(chans["green_gray"], format='png'),
            "blue_gray": encode_image_base64(chans["blue_gray"], format='png'),
            "red_isolate": encode_image_base64(chans["red_isolate"], format='png'),
            "green_isolate": encode_image_base64(chans["green_isolate"], format='png'),
            "blue_isolate": encode_image_base64(chans["blue_isolate"], format='png'),
            "metadata": get_image_metadata(arr)
        }), 200
    else:
        return jsonify({"status": "error", "error": f"Unknown conversion operation: {op}"}), 400
        
    return jsonify(serialize_image_response(res, extra_data=extra)), 200


@cv_bp.route('/intensity', methods=['POST'])
def intensity_transform():
    """Handles point operations: negative, log, gamma, contrast stretch, slicing, norm."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    op = data.get('operation', 'negative')
    
    if op == 'negative':
        out, lut = transform_negative(arr)
        eq = "s = 255 - r"
    elif op == 'log':
        c = float(data.get('c')) if data.get('c') is not None else None
        out, lut = transform_logarithmic(arr, c=c)
        eq = "s = c * log(1 + r)"
    elif op == 'gamma':
        gamma = float(data.get('gamma', 1.0))
        c = float(data.get('c', 1.0))
        out, lut = transform_gamma(arr, gamma=gamma, c=c)
        eq = f"s = {c} * 255 * (r/255)^{gamma}"
    elif op == 'contrast_stretch':
        r1 = int(data.get('r1', 70))
        s1 = int(data.get('s1', 20))
        r2 = int(data.get('r2', 180))
        s2 = int(data.get('s2', 230))
        out, lut = transform_contrast_stretch(arr, r1, s1, r2, s2)
        eq = f"Piecewise linear stretch: ({r1},{s1}) to ({r2},{s2})"
    elif op == 'slicing':
        low = int(data.get('low', 100))
        high = int(data.get('high', 200))
        preserve = bool(data.get('preserve_background', True))
        out, lut = transform_intensity_slicing(arr, low, high, preserve_background=preserve)
        eq = f"Intensity Slicing [{low}, {high}], preserve_bg={preserve}"
    elif op == 'brightness_contrast':
        alpha = float(data.get('alpha', 1.0))
        beta = float(data.get('beta', 0.0))
        out, lut = transform_brightness_contrast(arr, alpha, beta)
        eq = f"s = {alpha} * r + {beta}"
    elif op == 'normalize':
        out, lut = transform_normalize(arr)
        eq = "s = 255 * (r - min) / (max - min)"
    else:
        return jsonify({"status": "error", "error": f"Unknown intensity operation: {op}"}), 400
        
    hist_before = compute_histogram(arr)
    hist_after = compute_histogram(out)
    
    return jsonify(serialize_image_response(out, extra_data={
        "operation": op,
        "equation": eq,
        "transfer_lut": lut,
        "hist_before": hist_before,
        "hist_after": hist_after
    })), 200


@cv_bp.route('/histogram', methods=['POST'])
def histogram_analysis():
    """Computes histogram and 6-stage histogram equalisation."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    
    gray = rgb_to_grayscale(arr) if arr.ndim == 3 else arr
    eq_result = histogram_equalization(gray)
    
    return jsonify({
        "status": "success",
        "equalized_image": encode_image_base64(eq_result["equalized_image"], format='png'),
        "original_image": encode_image_base64(gray, format='png'),
        "input_histogram": eq_result["input_histogram"],
        "input_cdf": eq_result["input_cdf"],
        "output_histogram": eq_result["output_histogram"],
        "output_cdf": eq_result["output_cdf"],
        "mapping_lut": eq_result["mapping_lut"],
        "stages_data": eq_result["stages_data"],
        "input_metrics": eq_result["input_metrics"],
        "output_metrics": eq_result["output_metrics"]
    }), 200


@cv_bp.route('/kernel/step', methods=['POST'])
def kernel_step():
    """Calculates step breakdown for Kernel Laboratory at coordinate (r, c)."""
    data = request.get_json() or {}
    matrix = np.array(data.get('matrix', [[100, 150, 200], [50, 80, 120], [20, 60, 90]]), dtype=float)
    preset_key = data.get('preset', 'box_3x3')
    
    if preset_key in KERNEL_PRESETS:
        k_info = KERNEL_PRESETS[preset_key]
        kernel = np.array(k_info['kernel'], dtype=float)
        op_type = k_info['type']
    else:
        kernel = np.array(data.get('custom_kernel', [[1/9]*3]*3), dtype=float)
        op_type = data.get('op_type', 'linear')
        
    r = int(data.get('r', 1))
    c = int(data.get('c', 1))
    pad_mode = data.get('padding_mode', 'zero')
    is_conv = bool(data.get('is_convolution', False))
    stride = int(data.get('stride', 1))
    
    step_data = compute_kernel_step(
        matrix, kernel, center_r=r, center_c=c,
        padding_mode=pad_mode, is_convolution=is_conv,
        op_type=op_type, stride=stride
    )
    
    # Calculate output dimensions
    in_h, in_w = matrix.shape
    kh, kw = kernel.shape
    pad_amt = kh // 2 if pad_mode != 'valid' else 0
    out_h, out_w = calculate_output_dimensions(in_h, in_w, kh, kw, stride=stride, pad=pad_amt)
    
    step_data["output_dimensions"] = [out_w, out_h]
    step_data["status"] = "success"
    return jsonify(step_data), 200


@cv_bp.route('/filter', methods=['POST'])
def filter_and_noise():
    """Applies noise generation or filtering with comparative metrics."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    action = data.get('action', 'filter')
    
    if action == 'noise':
        ntype = data.get('noise_type', 'gaussian')
        if ntype == 'gaussian':
            mean = float(data.get('mean', 0.0))
            sigma = float(data.get('sigma', 25.0))
            out = add_gaussian_noise(arr, mean=mean, sigma=sigma)
        elif ntype == 'salt_pepper':
            amt = float(data.get('amount', 0.05))
            out = add_salt_and_pepper_noise(arr, amount=amt)
        elif ntype == 'speckle':
            var = float(data.get('var', 0.04))
            out = add_speckle_noise(arr, var=var)
        elif ntype == 'poisson':
            out = add_poisson_noise(arr)
        else:
            return jsonify({"status": "error", "error": f"Unknown noise: {ntype}"}), 400
            
        metrics = calculate_restoration_metrics(arr, out)
        return jsonify(serialize_image_response(out, extra_data={"noise_type": ntype, "metrics": metrics})), 200
        
    else:  # filtering
        ftype = data.get('filter_type', 'gaussian')
        k_size = int(data.get('k_size', 3))
        
        if ftype == 'box':
            out = apply_box_filter(arr, k_size=k_size)
        elif ftype == 'gaussian':
            sigma = float(data.get('sigma', 1.0))
            out = apply_gaussian_filter(arr, sigma=sigma, k_size=k_size)
        elif ftype == 'median':
            out = apply_median_filter(arr, k_size=k_size)
        elif ftype == 'min':
            out = apply_min_filter(arr, k_size=k_size)
        elif ftype == 'max':
            out = apply_max_filter(arr, k_size=k_size)
        elif ftype == 'bilateral':
            out = apply_bilateral_filter(arr)
        elif ftype == 'unsharp':
            k_val = float(data.get('k', 1.0))
            out, mask = apply_unsharp_masking(arr, k=k_val)
        else:
            return jsonify({"status": "error", "error": f"Unknown filter: {ftype}"}), 400
            
        metrics = calculate_restoration_metrics(arr, out)
        return jsonify(serialize_image_response(out, extra_data={"filter_type": ftype, "metrics": metrics})), 200


@cv_bp.route('/edges', methods=['POST'])
def edge_detection():
    """Computes Sobel, Prewitt, Laplacian, and 5-stage Canny."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    method = data.get('method', 'canny')
    gray = rgb_to_grayscale(arr) if arr.ndim == 3 else arr
    
    if method == 'canny':
        low = int(data.get('low_threshold', 50))
        high = int(data.get('high_threshold', 150))
        sigma = float(data.get('sigma', 1.0))
        stages = canny_edge_detection_stages(gray, low_threshold=low, high_threshold=high, sigma=sigma)
        
        return jsonify({
            "status": "success",
            "method": "canny",
            "stage1_blurred": encode_image_base64(stages["stage1_blurred"]),
            "stage2_magnitude": encode_image_base64(stages["stage2_magnitude"]),
            "stage3_nms": encode_image_base64(stages["stage3_nms"]),
            "stage4_threshold": encode_image_base64(stages["stage4_threshold"]),
            "stage5_final": encode_image_base64(stages["stage5_final"]),
            "metrics": stages["metrics"]
        }), 200
        
    elif method in ('sobel', 'prewitt'):
        grads = compute_gradient_operators(gray, operator=method)
        return jsonify({
            "status": "success",
            "method": method,
            "gx": encode_image_base64(grads["gx_display"]),
            "gy": encode_image_base64(grads["gy_display"]),
            "magnitude": encode_image_base64(grads["magnitude_display"]),
            "direction": encode_image_base64(grads["direction_display"])
        }), 200
        
    elif method == 'laplacian':
        conn = int(data.get('connectivity', 4))
        laps = compute_laplacian_edges(gray, connectivity=conn)
        return jsonify({
            "status": "success",
            "method": "laplacian",
            "laplacian": encode_image_base64(laps["laplacian_display"])
        }), 200
        
    return jsonify({"status": "error", "error": f"Unknown edge method: {method}"}), 400


@cv_bp.route('/morphology', methods=['POST'])
def morphology_ops():
    """Binary morphology: erosion, dilation, opening, closing, gradient."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    gray = rgb_to_grayscale(arr) if arr.ndim == 3 else arr
    bin_img = grayscale_to_binary(gray, int(data.get('threshold', 128)))
    
    op = data.get('operation', 'erosion')
    se_key = data.get('structuring_element', 'square_3x3')
    se = STRUCTURING_ELEMENTS.get(se_key, STRUCTURING_ELEMENTS['square_3x3'])
    
    if op == 'erosion':
        out = binary_erosion(bin_img, se)
    elif op == 'dilation':
        out = binary_dilation(bin_img, se)
    elif op == 'opening':
        out = binary_opening(bin_img, se)
    elif op == 'closing':
        out = binary_closing(bin_img, se)
    elif op == 'gradient':
        out = morphological_gradient(bin_img, se)
    else:
        return jsonify({"status": "error", "error": f"Unknown morphology op: {op}"}), 400
        
    return jsonify(serialize_image_response(out, extra_data={
        "operation": op,
        "binary_input": encode_image_base64(bin_img),
        "structuring_element": se_key,
        "se_matrix": se.tolist()
    })), 200


@cv_bp.route('/segmentation', methods=['POST'])
def segmentation_ops():
    """Segmentation: global threshold, adaptive threshold, Otsu, CCA."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    method = data.get('method', 'otsu')
    gray = rgb_to_grayscale(arr) if arr.ndim == 3 else arr
    
    if method == 'otsu':
        res = otsu_threshold(gray)
        return jsonify({
            "status": "success",
            "method": "otsu",
            "optimal_threshold": res["optimal_threshold"],
            "variance_curve": res["variance_curve"],
            "binary_image": encode_image_base64(res["binary_image"]),
            "histogram": res["histogram"]
        }), 200
        
    elif method == 'adaptive':
        blk = int(data.get('block_size', 11))
        out = adaptive_threshold(gray, block_size=blk)
        return jsonify(serialize_image_response(out, extra_data={"method": "adaptive", "block_size": blk})), 200
        
    elif method == 'cca':
        conn = int(data.get('connectivity', 8))
        bin_img = grayscale_to_binary(gray, int(data.get('threshold', 128)))
        res = connected_components_analysis(bin_img, connectivity=conn)
        return jsonify({
            "status": "success",
            "method": "cca",
            "num_components": res["num_components"],
            "connectivity": res["connectivity"],
            "components": res["components"][:50], # Cap table size
            "color_visualization": encode_image_base64(res["color_visualization"])
        }), 200
        
    return jsonify({"status": "error", "error": f"Unknown segmentation method: {method}"}), 400


@cv_bp.route('/features/harris', methods=['POST'])
def harris_features():
    """Harris Corner Detection."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    k = float(data.get('k', 0.04))
    thresh = float(data.get('threshold_ratio', 0.01))
    
    res = harris_corner_detector(arr, k=k, threshold_ratio=thresh)
    return jsonify({
        "status": "success",
        "num_corners": res["num_corners"],
        "corners": res["corners"][:100],
        "overlay_image": encode_image_base64(res["overlay_image"]),
        "response_map": encode_image_base64(res["response_map"]),
        "k_factor": res["k_factor"]
    }), 200


@cv_bp.route('/features/sift', methods=['POST'])
def sift_features():
    """SIFT Keypoint Detection."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    max_kps = int(data.get('max_keypoints', 50))
    
    res = sift_detect_keypoints(arr, max_keypoints=max_kps)
    if not res.get("available"):
        return jsonify(res), 200
        
    return jsonify({
        "status": "success",
        "available": True,
        "num_keypoints": res["num_keypoints"],
        "keypoints": res["keypoints"],
        "overlay_image": encode_image_base64(res["overlay_image"]),
        "descriptor_shape": res["descriptor_shape"]
    }), 200


@cv_bp.route('/features/sift-match', methods=['POST'])
def sift_match():
    """SIFT Feature Matching between two images."""
    data = request.get_json() or {}
    if 'image1' in data and 'image2' in data:
        img1 = decode_image_base64(data['image1'])
        img2 = decode_image_base64(data['image2'])
    else:
        img1 = generate_sample_pattern('shapes', size=128)
        img2 = generate_sample_pattern('checkerboard', size=128)
        
    res = sift_match_images(img1, img2, max_matches=int(data.get('max_matches', 30)))
    if not res.get("available") or "matched_image" not in res:
        return jsonify(res), 200
        
    return jsonify({
        "status": "success",
        "available": True,
        "num_matches": res["num_matches"],
        "keypoints_img1": res["keypoints_img1"],
        "keypoints_img2": res["keypoints_img2"],
        "matched_image": encode_image_base64(res["matched_image"])
    }), 200


@cv_bp.route('/pca', methods=['POST'])
def pca_operation():
    """PCA Decomposition, reconstruction, and denoising."""
    data = request.get_json() or {}
    mode = data.get('mode', 'teaching')
    
    if mode == 'teaching':
        k = int(data.get('k_components', 2))
        res = pca_teaching_matrix_example(k_components=k)
        res["status"] = "success"
        return jsonify(res), 200
    else:
        arr = _get_input_array_from_request(data)
        gray = rgb_to_grayscale(arr) if arr.ndim == 3 else arr
        n_comps = int(data.get('n_components', 10))
        patch_sz = int(data.get('patch_size', 8))
        res = pca_image_denoise(gray, n_components=n_comps, patch_size=patch_sz)
        
        return jsonify({
            "status": "success",
            "reconstructed_image": encode_image_base64(res["reconstructed_image"]),
            "original_cropped": encode_image_base64(res["original_cropped"]),
            "total_components": res["total_components"],
            "retained_components": res["retained_components"],
            "retained_variance_pct": res["retained_variance_pct"],
            "explained_variance_curve": res["explained_variance_curve"],
            "metrics": res["metrics"],
            "compression_ratio": res["compression_ratio"]
        }), 200


@cv_bp.route('/pipeline', methods=['POST'])
def run_pipeline():
    """Runs a multi-stage sequential image processing pipeline."""
    data = request.get_json() or {}
    arr = _get_input_array_from_request(data)
    stages = data.get('stages', [])
    
    res = run_image_pipeline(arr, stages)
    
    # Encode stage images to base64
    encoded_stages = []
    for s in res["stages"]:
        encoded_stages.append({
            "stage_index": s["stage_index"],
            "name": s["name"],
            "description": s["description"],
            "dimensions": s["dimensions"],
            "channels": s["channels"],
            "time_ms": s["time_ms"],
            "image_data": encode_image_base64(s["image"])
        })
        
    return jsonify({
        "status": "success",
        "num_stages": res["num_stages"],
        "total_time_ms": res["total_time_ms"],
        "final_image": encode_image_base64(res["final_image"]),
        "stages": encoded_stages
    }), 200
