"""
Principal Component Analysis (PCA) & Image Denoising
====================================================
Implements PCA dimensionality reduction, image decomposition, and denoising:
1. Data Matrix Creation X (patches / flattened rows)
2. Mean Centering: X_c = X - mu
3. Covariance Matrix: C = (1/M) * X_c^T * X_c
4. Eigenvalue & Eigenvector Decomposition (sorted descending)
5. Explained Variance Ratio & Cumulative Energy
6. Top-K Component Selection
7. Subspace Projection: Z = X_c * V_k
8. Reconstruction: X_recon = Z * V_k^T + mu
9. Quality Comparison (MSE, PSNR, Compression Ratio)
"""

import numpy as np
from typing import Dict, Any, List, Tuple
from .conversions import rgb_to_grayscale
from .filters import calculate_restoration_metrics


def pca_teaching_matrix_example(k_components: int = 2) -> Dict[str, Any]:
    """
    Transparent matrix walkthrough of PCA mathematics:
    Uses a 5x4 matrix of numbers for exact step-by-step telemetry
    of mean, covariance, eigenvalues, eigenvectors, and projection.
    """
    # Deterministic teaching dataset: 5 samples, 4 features
    X = np.array([
        [150, 140, 160, 170],
        [40,  45,  35,  50],
        [190, 200, 210, 195],
        [80,  75,  85,  90],
        [120, 110, 130, 125]
    ], dtype=float)
    
    m, n = X.shape
    k = max(1, min(n, k_components))
    
    # 1. Mean vector
    mu = np.mean(X, axis=0)
    
    # 2. Mean centering
    X_centered = X - mu
    
    # 3. Covariance matrix
    cov_matrix = np.cov(X_centered, rowvar=False)
    
    # 4. Eigendecomposition
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)
    
    # Sort descending
    idx = np.argsort(eigenvalues)[::-1]
    sorted_eigenvalues = np.maximum(0, eigenvalues[idx])
    sorted_eigenvectors = eigenvectors[:, idx]
    
    total_var = np.sum(sorted_eigenvalues)
    explained_variance = sorted_eigenvalues / max(1e-9, total_var)
    cum_variance = np.cumsum(explained_variance)
    
    # 5. Select top k components
    V_k = sorted_eigenvectors[:, :k]
    
    # 6. Project onto subspace
    Z = np.dot(X_centered, V_k)
    
    # 7. Reconstruct
    X_reconstructed = np.dot(Z, V_k.T) + mu
    
    reconstruction_error = float(np.mean((X - X_reconstructed) ** 2))
    
    return {
        "X_original": X.tolist(),
        "mean_vector": np.round(mu, 2).tolist(),
        "X_centered": np.round(X_centered, 2).tolist(),
        "covariance_matrix": np.round(cov_matrix, 2).tolist(),
        "eigenvalues": np.round(sorted_eigenvalues, 2).tolist(),
        "eigenvectors": np.round(sorted_eigenvectors, 3).tolist(),
        "explained_variance_ratio": np.round(explained_variance * 100.0, 2).tolist(),
        "cumulative_variance_ratio": np.round(cum_variance * 100.0, 2).tolist(),
        "k_selected": k,
        "projection_Z": np.round(Z, 2).tolist(),
        "X_reconstructed": np.round(X_reconstructed, 2).tolist(),
        "mse_error": round(reconstruction_error, 4)
    }


def pca_image_denoise(
    gray_img: np.ndarray,
    n_components: int = 10,
    patch_size: int = 8
) -> Dict[str, Any]:
    """
    Practical PCA Image Compression & Denoising using non-overlapping block patches.
    Decomposes image into patch vectors, performs PCA, keeps top components, and reconstructs.
    """
    if gray_img.ndim == 3:
        gray_img = rgb_to_grayscale(gray_img)
        
    h, w = gray_img.shape
    # Crop to multiple of patch_size
    crop_h = (h // patch_size) * patch_size
    crop_w = (w // patch_size) * patch_size
    cropped = gray_img[:crop_h, :crop_w].astype(float)
    
    # Extract patches into matrix X: M patches, N = patch_size^2 features
    patches = []
    for r in range(0, crop_h, patch_size):
        for c in range(0, crop_w, patch_size):
            p = cropped[r : r + patch_size, c : c + patch_size].flatten()
            patches.append(p)
            
    X = np.array(patches, dtype=float)
    m, n = X.shape
    k = max(1, min(n, n_components))
    
    # Mean centering
    mu = np.mean(X, axis=0)
    X_centered = X - mu
    
    # Efficient SVD / PCA
    # Covariance matrix C is n x n (e.g. 64 x 64 for 8x8 patches)
    cov = np.dot(X_centered.T, X_centered) / max(1, m - 1)
    eigenvalues, eigenvectors = np.linalg.eigh(cov)
    
    # Sort descending
    idx = np.argsort(eigenvalues)[::-1]
    sorted_evals = np.maximum(0, eigenvalues[idx])
    sorted_evecs = eigenvectors[:, idx]
    
    total_var = np.sum(sorted_evals)
    explained_ratio = sorted_evals / max(1e-9, total_var)
    cum_ratio = np.cumsum(explained_ratio)
    
    # Select top k
    V_k = sorted_evecs[:, :k]
    
    # Project and reconstruct
    Z = np.dot(X_centered, V_k)
    X_recon = np.dot(Z, V_k.T) + mu
    
    # Reassemble image from reconstructed patches
    recon_img = np.zeros((crop_h, crop_w), dtype=float)
    patch_idx = 0
    for r in range(0, crop_h, patch_size):
        for c in range(0, crop_w, patch_size):
            recon_img[r : r + patch_size, c : c + patch_size] = X_recon[patch_idx].reshape((patch_size, patch_size))
            patch_idx += 1
            
    recon_uint8 = np.clip(np.round(recon_img), 0, 255).astype(np.uint8)
    orig_cropped_uint8 = cropped.astype(np.uint8)
    
    metrics = calculate_restoration_metrics(orig_cropped_uint8, recon_uint8)
    
    # Compression ratio: original needed m*n floats; PCA stores m*k + k*n floats
    orig_params = m * n
    pca_params = m * k + k * n
    compression_ratio = round(orig_params / float(max(1, pca_params)), 2)
    
    return {
        "reconstructed_image": recon_uint8,
        "original_cropped": orig_cropped_uint8,
        "total_components": n,
        "retained_components": k,
        "retained_variance_pct": round(float(cum_ratio[k - 1]) * 100.0, 2),
        "eigenvalues": np.round(sorted_evals[:min(16, n)], 2).tolist(),
        "explained_variance_curve": np.round(cum_ratio * 100.0, 2).tolist(),
        "metrics": metrics,
        "compression_ratio": compression_ratio
    }
