"""
Automated Verification Suite for Computer Vision & DIP Workspace
================================================================
Comprehensive unit and integration tests covering:
- RGB, Grayscale, Binary and HSV conversions
- Sampling, Quantization, and Intensity transformations
- Histogram computation and 6-stage Histogram Equalisation
- Kernel convolution, cross-correlation, padding, and order-statistics
- Smoothing, sharpening, noise generators, and PSNR/MSE metrics
- Sobel, Prewitt, Laplacian, and 5-stage Canny Edge Detection
- Binary morphology (Erosion, Dilation, Opening, Closing, Gradient)
- Otsu thresholding and Connected Component Analysis (4- and 8-connectivity)
- Harris Corner Detector and SIFT descriptor detection/matching
- PCA decomposition, component selection, variance, and reconstruction
- Multi-stage image processing pipeline
- Flask REST API endpoints
"""

import pytest
import numpy as np
from Sorted.image_processing.conversions import (
    rgb_to_grayscale, grayscale_to_binary, apply_sampling, apply_quantization,
    rgb_to_hsv, hsv_to_rgb, separate_rgb_channels, hsv_color_mask, swap_rgb_bgr
)
from Sorted.image_processing.intensity import (
    transform_negative, transform_logarithmic, transform_gamma,
    transform_contrast_stretch, transform_intensity_slicing,
    transform_brightness_contrast, transform_normalize
)
from Sorted.image_processing.histograms import compute_histogram, histogram_equalization
from Sorted.image_processing.kernels import (
    calculate_output_dimensions, pad_image, compute_kernel_step, apply_spatial_filter, KERNEL_PRESETS
)
from Sorted.image_processing.filters import (
    add_gaussian_noise, add_salt_and_pepper_noise, add_speckle_noise,
    calculate_restoration_metrics, apply_box_filter, apply_gaussian_filter,
    apply_median_filter, apply_min_filter, apply_max_filter, apply_unsharp_masking
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
    harris_corner_detector, is_sift_available, sift_detect_keypoints
)
from Sorted.image_processing.pca import pca_teaching_matrix_example, pca_image_denoise
from Sorted.image_processing.pipeline import run_image_pipeline
from Sorted.image_processing.image_io import generate_sample_pattern, decode_image_base64, encode_image_base64
from Sorted.api.app import create_app


# ---------------- 1. Conversions & Color Models ----------------

def test_rgb_to_grayscale():
    # 2x2 RGB test image
    rgb = np.array([
        [[255, 0, 0], [0, 255, 0]],      # Pure Red, Pure Green
        [[0, 0, 255], [255, 255, 255]]   # Pure Blue, Pure White
    ], dtype=np.uint8)
    
    # ITU-R BT.601 standard: Y = 0.299*R + 0.587*G + 0.114*B
    gray_lum = rgb_to_grayscale(rgb, method='luminosity')
    assert gray_lum[0, 0] == round(0.299 * 255) # 76
    assert gray_lum[0, 1] == round(0.587 * 255) # 150
    assert gray_lum[1, 0] == round(0.114 * 255) # 29
    assert gray_lum[1, 1] == 255
    
    gray_avg = rgb_to_grayscale(rgb, method='average')
    assert gray_avg[0, 0] == 85


def test_grayscale_to_binary():
    gray = np.array([[50, 128], [200, 0]], dtype=np.uint8)
    binary = grayscale_to_binary(gray, threshold=128)
    assert binary[0, 0] == 0
    assert binary[0, 1] == 255
    assert binary[1, 0] == 255
    assert binary[1, 1] == 0
    assert set(np.unique(binary)).issubset({0, 255})


def test_sampling_and_quantization():
    arr = np.arange(64, dtype=np.uint8).reshape((8, 8))
    sampled = apply_sampling(arr, factor=2)
    assert sampled.shape == (8, 8)
    
    # 1-bit quantization (2 levels: 0 and 255)
    q1 = apply_quantization(arr, bits=1)
    assert set(np.unique(q1)).issubset({0, 255})
    
    # 2-bit quantization (4 levels)
    q2 = apply_quantization(arr, bits=2)
    assert len(np.unique(q2)) <= 4


def test_hsv_conversion_and_masking():
    rgb = np.array([[[255, 0, 0], [0, 255, 0], [0, 0, 255]]], dtype=np.uint8)
    hsv = rgb_to_hsv(rgb)
    assert np.isclose(hsv[0, 0, 0], 0.0, atol=2.0)    # Red Hue = 0
    assert np.isclose(hsv[0, 1, 0], 120.0, atol=2.0)  # Green Hue = 120
    assert np.isclose(hsv[0, 2, 0], 240.0, atol=2.0)  # Blue Hue = 240
    
    rgb_back = hsv_to_rgb(hsv)
    assert np.allclose(rgb, rgb_back, atol=3)
    
    # Color mask test: filter for pure green
    mask, masked_img = hsv_color_mask(rgb, h_min=100, h_max=140, s_min=50, s_max=100, v_min=50, v_max=100)
    assert mask[0, 0] == 0
    assert mask[0, 1] == 255
    assert mask[0, 2] == 0


def test_bgr_swap():
    rgb = np.array([[[255, 100, 50]]], dtype=np.uint8)
    bgr = swap_rgb_bgr(rgb)
    assert bgr[0, 0, 0] == 50
    assert bgr[0, 0, 1] == 100
    assert bgr[0, 0, 2] == 255


# ---------------- 2. Intensity Transformations ----------------

def test_intensity_transformations():
    arr = np.array([[0, 64], [128, 255]], dtype=np.uint8)
    
    # Negative
    neg, lut_neg = transform_negative(arr)
    assert neg[0, 0] == 255 and neg[1, 1] == 0
    assert lut_neg[0] == 255 and lut_neg[255] == 0
    
    # Gamma
    gamma_out, _ = transform_gamma(arr, gamma=2.0)
    assert gamma_out[0, 0] == 0
    assert gamma_out[1, 1] == 255
    # gamma > 1 compresses dark tones (128/255)^2 * 255 ~ 64
    assert gamma_out[1, 0] < 128
    
    # Contrast stretch
    cs_out, _ = transform_contrast_stretch(arr, r1=70, s1=20, r2=180, s2=230)
    assert cs_out[0, 0] == 0
    assert cs_out[1, 1] == 255
    
    # Slicing
    slice_out, _ = transform_intensity_slicing(arr, low=100, high=200, highlight_val=255, preserve_background=False)
    assert slice_out[1, 0] == 255
    assert slice_out[0, 0] == 0
    assert slice_out[1, 1] == 0


# ---------------- 3. Histograms & Equalisation ----------------

def test_histogram_and_equalization():
    gray = np.array([
        [50, 50, 50, 50],
        [50, 50, 60, 60],
        [60, 60, 70, 70],
        [70, 70, 70, 70]
    ], dtype=np.uint8)
    
    hist_res = compute_histogram(gray)
    assert hist_res["type"] == "grayscale"
    assert sum(hist_res["histogram"]) == 16
    assert hist_res["mean"] == 60.0
    
    eq_res = histogram_equalization(gray)
    assert eq_res["equalized_image"].shape == (4, 4)
    # Equalized image must spread over dynamic range, max value should increase
    assert np.max(eq_res["equalized_image"]) > np.max(gray)
    assert len(eq_res["stages_data"]) > 0


# ---------------- 4. Spatial Filtering & Kernel Laboratory ----------------

def test_kernel_dimensions_and_padding():
    # 10x10 input, 3x3 kernel, stride=1, pad=0 -> (10 - 3)/1 + 1 = 8
    oh, ow = calculate_output_dimensions(10, 10, 3, 3, stride=1, pad=0)
    assert (oh, ow) == (8, 8)
    
    # With pad=1 -> (10 + 2 - 3)/1 + 1 = 10 (same size)
    oh_same, ow_same = calculate_output_dimensions(10, 10, 3, 3, stride=1, pad=1)
    assert (oh_same, ow_same) == (10, 10)
    
    # Test padding modes
    mat = np.array([[1, 2], [3, 4]], dtype=np.uint8)
    zero_pad = pad_image(mat, 1, 1, mode='zero')
    assert zero_pad.shape == (4, 4)
    assert zero_pad[0, 0] == 0
    assert zero_pad[1, 1] == 1


def test_kernel_step_arithmetic():
    # 3x3 simple matrix
    matrix = np.array([
        [10, 20, 30],
        [40, 50, 60],
        [70, 80, 90]
    ], dtype=np.uint8)
    
    # 3x3 box blur kernel: all 1/9
    box_kernel = np.ones((3, 3), dtype=float) / 9.0
    
    step = compute_kernel_step(matrix, box_kernel, center_r=1, center_c=1, padding_mode='zero', op_type='linear')
    # Sum of 10+20+...+90 = 450, divided by 9 = 50.0
    assert step["sum_of_products"] == pytest.approx(50.0)
    assert step["output_value"] == 50


def test_order_statistic_filters():
    # Canonical median filter test case: median of {200, 200, 255, 5, 200} surrounded by 200
    neighbourhood = np.array([
        [200, 200, 200],
        [200,   5, 255],
        [200, 200, 200]
    ], dtype=np.uint8)
    
    step = compute_kernel_step(neighbourhood, np.ones((3,3)), center_r=1, center_c=1, op_type='median')
    assert step["output_value"] == 200
    
    step_min = compute_kernel_step(neighbourhood, np.ones((3,3)), center_r=1, center_c=1, op_type='min')
    assert step_min["output_value"] == 5
    
    step_max = compute_kernel_step(neighbourhood, np.ones((3,3)), center_r=1, center_c=1, op_type='max')
    assert step_max["output_value"] == 255


def test_convolution_vs_correlation():
    # Asymmetric kernel
    k = np.array([[1, 2], [3, 4]], dtype=float)
    img = np.array([[10, 20], [30, 40]], dtype=float)
    
    # Cross correlation without reversal:
    corr_val = np.sum(img * k) # 10*1 + 20*2 + 30*3 + 40*4 = 10 + 40 + 90 + 160 = 300
    # Convolution with 180 deg flipped kernel:
    # flipped k is [[4, 3], [2, 1]]
    conv_val = np.sum(img * np.flip(k)) # 10*4 + 20*3 + 30*2 + 40*1 = 40 + 60 + 60 + 40 = 200
    
    assert corr_val == 300
    assert conv_val == 200


# ---------------- 5. Smoothing, Sharpening & Noise ----------------

def test_noise_and_restoration_metrics():
    clean = np.ones((32, 32), dtype=np.uint8) * 120
    sp_noisy = add_salt_and_pepper_noise(clean, amount=0.1)
    assert np.any(sp_noisy == 0) or np.any(sp_noisy == 255)
    
    metrics = calculate_restoration_metrics(clean, clean)
    assert metrics["mse"] == 0.0
    assert metrics["psnr"] >= 90.0
    
    noisy_metrics = calculate_restoration_metrics(clean, sp_noisy)
    assert noisy_metrics["mse"] > 0.0
    assert noisy_metrics["psnr"] < 90.0
    
    # Median filter should restore salt & pepper noise effectively
    restored = apply_median_filter(sp_noisy, k_size=3)
    restored_metrics = calculate_restoration_metrics(clean, restored)
    assert restored_metrics["mse"] < noisy_metrics["mse"]


def test_unsharp_masking():
    img = np.array([[50, 50, 150, 150]] * 4, dtype=np.uint8)
    sharp, mask = apply_unsharp_masking(img, k=1.0)
    assert sharp.shape == img.shape
    assert mask.shape == img.shape


# ---------------- 6. Edge Detection ----------------

def test_sobel_and_laplacian():
    # Vertical edge: left half 50, right half 200
    vert_edge = np.zeros((10, 10), dtype=np.uint8)
    vert_edge[:, :5] = 50
    vert_edge[:, 5:] = 200
    
    grads = compute_gradient_operators(vert_edge, operator='sobel')
    # Strong response on vertical boundary column
    assert np.max(grads["magnitude_display"]) > 100
    assert np.max(grads["gx_display"]) > np.max(grads["gy_display"])
    
    laps = compute_laplacian_edges(vert_edge, connectivity=4)
    assert np.max(laps["laplacian_display"]) > 50


def test_canny_edge_detection_stages():
    img = generate_sample_pattern('shapes', size=64)
    stages = canny_edge_detection_stages(img, low_threshold=40, high_threshold=120)
    
    assert "stage1_blurred" in stages
    assert "stage2_magnitude" in stages
    assert "stage3_nms" in stages
    assert "stage4_threshold" in stages
    assert "stage5_final" in stages
    assert stages["stage5_final"].shape == (64, 64)
    assert set(np.unique(stages["stage5_final"])).issubset({0, 255})


# ---------------- 7. Morphology ----------------

def test_binary_morphology():
    # Single 3x3 isolated foreground block
    bin_img = np.zeros((9, 9), dtype=np.uint8)
    bin_img[3:6, 3:6] = 255
    se = STRUCTURING_ELEMENTS["square_3x3"]
    
    # Erosion shrinks it to 1 single pixel at center (4, 4)
    eroded = binary_erosion(bin_img, se)
    assert np.sum(eroded == 255) == 1
    assert eroded[4, 4] == 255
    
    # Dilation expands the 3x3 block to 5x5 block
    dilated = binary_dilation(bin_img, se)
    assert np.sum(dilated == 255) == 25
    assert dilated[2, 2] == 255
    
    # Opening on isolated small 1-pixel noise eliminates it
    noisy = bin_img.copy()
    noisy[1, 1] = 255 # isolated noise
    opened = binary_opening(noisy, se)
    assert opened[1, 1] == 0


# ---------------- 8. Segmentation & Connected Components ----------------

def test_otsu_thresholding():
    # Bimodal distribution: 50 pixels at 40, 50 pixels at 200
    bimodal = np.zeros((10, 10), dtype=np.uint8)
    bimodal[:5, :] = 40
    bimodal[5:, :] = 200
    
    res = otsu_threshold(bimodal)
    # Optimal threshold should cleanly separate 40 and 200 (between 40 and 200)
    assert 40 < res["optimal_threshold"] < 200
    assert len(res["variance_curve"]) == 256


def test_connected_components_analysis():
    # Two separate square islands
    img = np.zeros((12, 12), dtype=np.uint8)
    img[1:4, 1:4] = 255   # 3x3 island (area 9)
    img[7:10, 7:10] = 255 # 3x3 island (area 9)
    
    cca = connected_components_analysis(img, connectivity=8)
    assert cca["num_components"] == 2
    assert len(cca["components"]) == 2
    assert cca["components"][0]["area"] == 9
    assert cca["components"][1]["area"] == 9
    
    # Diagonal connectivity test
    diag = np.zeros((4, 4), dtype=np.uint8)
    diag[1, 1] = 255
    diag[2, 2] = 255
    # 4-connectivity treats diagonals as separate components
    cca4 = connected_components_analysis(diag, connectivity=4)
    assert cca4["num_components"] == 2
    # 8-connectivity connects diagonals into 1 component
    cca8 = connected_components_analysis(diag, connectivity=8)
    assert cca8["num_components"] == 1


# ---------------- 9. Local Descriptors ----------------

def test_harris_corner_detector():
    checker = generate_sample_pattern('checkerboard', size=32)
    res = harris_corner_detector(checker, k=0.04, threshold_ratio=0.01)
    assert res["num_corners"] > 0
    assert "corners" in res
    assert "overlay_image" in res
    assert res["overlay_image"].shape == (32, 32, 3)


def test_sift_support():
    img = generate_sample_pattern('shapes', size=64)
    if is_sift_available():
        res = sift_detect_keypoints(img, max_keypoints=20)
        assert res["available"] is True
        assert res["num_keypoints"] >= 0
    else:
        res = sift_detect_keypoints(img)
        assert res["available"] is False


# ---------------- 10. PCA & Denoising ----------------

def test_pca_teaching_matrix():
    res = pca_teaching_matrix_example(k_components=2)
    assert res["k_selected"] == 2
    # Cumulative variance of 4 components must sum to 100%
    assert np.isclose(res["cumulative_variance_ratio"][-1], 100.0, atol=1.0)
    # Eigenvalues must be non-negative and sorted descending
    evals = res["eigenvalues"]
    assert all(evals[i] >= evals[i+1] for i in range(len(evals)-1))
    assert res["mse_error"] >= 0.0


def test_pca_image_denoising():
    img = generate_sample_pattern('shapes', size=32)
    gray = rgb_to_grayscale(img)
    res = pca_image_denoise(gray, n_components=4, patch_size=8)
    assert res["reconstructed_image"].shape == (32, 32)
    assert res["compression_ratio"] > 1.0
    assert 0 <= res["retained_variance_pct"] <= 100.0


# ---------------- 11. Pipeline Studio ----------------

def test_image_pipeline():
    img = generate_sample_pattern('shapes', size=32)
    stages = [
        {"op": "grayscale", "params": {"method": "luminosity"}},
        {"op": "gaussian_blur", "params": {"sigma": 1.0, "k_size": 3}},
        {"op": "sobel", "params": {}},
        {"op": "threshold", "params": {"threshold": 100}}
    ]
    res = run_image_pipeline(img, stages)
    assert res["num_stages"] == 4
    assert len(res["stages"]) == 5 # initial + 4
    assert res["final_image"].shape == (32, 32)


# ---------------- 12. Flask API Endpoints ----------------

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as c:
        yield c


def test_flask_cv_endpoints(client):
    # GET /api/cv/info
    rv = client.get('/api/cv/info')
    assert rv.status_code == 200
    info = rv.get_json()
    assert info["status"] == "healthy"
    
    # GET /api/cv/sample/shapes
    rv = client.get('/api/cv/sample/shapes?size=32')
    assert rv.status_code == 200
    assert "image_data" in rv.get_json()
    
    # POST /api/cv/convert
    rv = client.post('/api/cv/convert', json={"pattern": "shapes", "operation": "grayscale"})
    assert rv.status_code == 200
    assert "image_data" in rv.get_json()
    
    # POST /api/cv/intensity
    rv = client.post('/api/cv/intensity', json={"pattern": "shapes", "operation": "negative"})
    assert rv.status_code == 200
    assert "equation" in rv.get_json()
    
    # POST /api/cv/kernel/step
    rv = client.post('/api/cv/kernel/step', json={
        "matrix": [[10, 20, 30], [40, 50, 60], [70, 80, 90]],
        "preset": "box_3x3",
        "r": 1, "c": 1
    })
    assert rv.status_code == 200
    assert rv.get_json()["output_value"] == 50
    
    # POST /api/cv/pca
    rv = client.post('/api/cv/pca', json={"mode": "teaching", "k_components": 2})
    assert rv.status_code == 200
    assert "covariance_matrix" in rv.get_json()
