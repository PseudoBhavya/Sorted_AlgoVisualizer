"""
Image I/O, Safe Decoding, and Sample Generation
===============================================
Handles safe decoding of base64 images, dimension validation,
format conversion, and synthetic educational test patterns.
"""

import base64
import io
import numpy as np
from typing import Tuple, Dict, Any, Optional

try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

try:
    import cv2
    HAS_CV2 = True
except ImportError:
    HAS_CV2 = False


def decode_image_base64(data_str: str, max_dim: int = 512) -> np.ndarray:
    """
    Safely decode a base64 encoded data URI or raw string into an RGB uint8 numpy array.
    Restricts dimensions to max_dim x max_dim to prevent memory exhaustion.
    """
    if ',' in data_str:
        data_str = data_str.split(',', 1)[1]
    
    img_bytes = base64.b64decode(data_str)
    
    if HAS_PIL:
        img = Image.open(io.BytesIO(img_bytes))
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Resize if oversized
        w, h = img.size
        if max(w, h) > max_dim:
            scale = max_dim / float(max(w, h))
            new_w = max(1, int(w * scale))
            new_h = max(1, int(h * scale))
            img = img.resize((new_w, new_h), Image.Resampling.BILINEAR)
        return np.array(img, dtype=np.uint8)
    
    elif HAS_CV2:
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError("Failed to decode image with OpenCV.")
        # OpenCV reads BGR by default, convert to RGB
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img.shape[:2]
        if max(w, h) > max_dim:
            scale = max_dim / float(max(w, h))
            img = cv2.resize(img, (int(w * scale), int(h * scale)))
        return img
    else:
        raise RuntimeError("Neither PIL nor OpenCV is available for image decoding.")


def encode_image_base64(arr: np.ndarray, format: str = 'png') -> str:
    """
    Encode a 2D (grayscale/binary) or 3D (RGB) numpy array to a data URL string.
    """
    arr = np.clip(arr, 0, 255).astype(np.uint8)
    
    if HAS_PIL:
        if arr.ndim == 2:
            img = Image.fromarray(arr, mode='L')
        elif arr.ndim == 3 and arr.shape[2] == 3:
            img = Image.fromarray(arr, mode='RGB')
        elif arr.ndim == 3 and arr.shape[2] == 4:
            img = Image.fromarray(arr, mode='RGBA')
        else:
            raise ValueError(f"Unsupported array shape: {arr.shape}")
        
        buf = io.BytesIO()
        img.save(buf, format=format.upper())
        b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
        return f"data:image/{format.lower()};base64,{b64}"
    
    elif HAS_CV2:
        if arr.ndim == 3 and arr.shape[2] == 3:
            save_arr = cv2.cvtColor(arr, cv2.COLOR_RGB2BGR)
        else:
            save_arr = arr
        ext = f".{format.lower()}"
        success, buf = cv2.imencode(ext, save_arr)
        if not success:
            raise ValueError(f"Failed to encode image to {format}.")
        b64 = base64.b64encode(buf.tobytes()).decode('utf-8')
        return f"data:image/{format.lower()};base64,{b64}"
    
    raise RuntimeError("Neither PIL nor OpenCV is available for image encoding.")


def generate_sample_pattern(name: str = 'shapes', size: int = 128) -> np.ndarray:
    """
    Generates deterministic educational teaching images (RGB uint8).
    """
    arr = np.zeros((size, size, 3), dtype=np.uint8)
    
    if name == 'checkerboard':
        block = max(4, size // 8)
        for r in range(size):
            for c in range(size):
                if ((r // block) + (c // block)) % 2 == 0:
                    arr[r, c] = [235, 235, 235]
                else:
                    arr[r, c] = [25, 30, 45]
                    
    elif name == 'gradient':
        for c in range(size):
            val = int((c / (size - 1)) * 255)
            arr[:, c] = [val, val, val]
            
    elif name == 'mri_brain':
        # Simulated medical phantom slice (Unit 1 Slide 21/25 application)
        center = size // 2
        y, x = np.ogrid[:size, :size]
        # Outer skull ellipse
        skull = ((x - center)**2) / ((size * 0.42)**2) + ((y - center)**2) / ((size * 0.46)**2) <= 1.0
        # Brain tissue ellipse
        brain = ((x - center)**2) / ((size * 0.36)**2) + ((y - center)**2) / ((size * 0.40)**2) <= 1.0
        # Ventricles
        v1 = ((x - center + size*0.08)**2) / ((size * 0.05)**2) + ((y - center)**2) / ((size * 0.15)**2) <= 1.0
        v2 = ((x - center - size*0.08)**2) / ((size * 0.05)**2) + ((y - center)**2) / ((size * 0.15)**2) <= 1.0
        # Simulated lesion / tumor
        tumor = ((x - center + size*0.18)**2 + (y - center - size*0.12)**2) <= (size * 0.08)**2
        
        arr[skull] = [180, 180, 180]
        arr[brain] = [120, 120, 130]
        # Texture
        np.random.seed(42)
        noise = np.random.randint(-15, 15, (size, size))
        arr[brain, 0] = np.clip(arr[brain, 0].astype(int) + noise[brain], 0, 255)
        arr[brain, 1] = arr[brain, 0]
        arr[brain, 2] = arr[brain, 0]
        arr[v1 | v2] = [30, 30, 40]
        arr[tumor] = [245, 245, 255] # Hyperintense lesion
        
    elif name == 'coins' or name == 'dots':
        # Distinct circles for morphology, segmentation & connected components
        arr[:] = [20, 25, 35]
        centers = [
            (int(size*0.25), int(size*0.25), int(size*0.12), [240, 210, 60]),
            (int(size*0.75), int(size*0.25), int(size*0.10), [200, 200, 220]),
            (int(size*0.35), int(size*0.70), int(size*0.14), [230, 140, 50]),
            (int(size*0.75), int(size*0.70), int(size*0.08), [100, 220, 240]),
            (int(size*0.50), int(size*0.45), int(size*0.06), [180, 240, 120])
        ]
        y, x = np.ogrid[:size, :size]
        for cx, cy, rad, col in centers:
            mask = (x - cx)**2 + (y - cy)**2 <= rad**2
            arr[mask] = col
            
    else:  # default 'shapes'
        arr[:] = [20, 24, 38]
        # Rectangle
        arr[int(size*0.15):int(size*0.45), int(size*0.15):int(size*0.55)] = [76, 215, 246]
        # Circle
        center = (int(size*0.72), int(size*0.35))
        rad = int(size*0.2)
        y, x = np.ogrid[:size, :size]
        mask = (x - center[0])**2 + (y - center[1])**2 <= rad**2
        arr[mask] = [255, 185, 95]
        # Diagonal line
        for i in range(int(size*0.55), int(size*0.9)):
            for w in range(-1, 2):
                if 0 <= i+w < size and 0 <= i < size:
                    arr[i, i+w] = [16, 185, 129]
                    
    return arr


def get_image_metadata(arr: np.ndarray, format_name: str = "PNG") -> Dict[str, Any]:
    """
    Returns image dimensions, bit depth, channel count, and estimated file size.
    """
    h, w = arr.shape[:2]
    c = 1 if arr.ndim == 2 else arr.shape[2]
    dtype_str = str(arr.dtype)
    bytes_per_pixel = arr.itemsize * c
    raw_size_bytes = h * w * bytes_per_pixel
    
    # Formats info from Unit 1 Slide 12
    fmt_info = {
        "JPEG": {"compression": "Lossy", "quality": "Good", "best_for": "Everyday photos, continuous tone"},
        "PNG": {"compression": "Lossless", "quality": "Excellent", "best_for": "Web graphics, icons, transparency"},
        "TIFF": {"compression": "Lossless", "quality": "Maximum", "best_for": "Archival, printing, medical scans"},
        "RAW": {"compression": "None", "quality": "Maximum (unprocessed)", "best_for": "Professional camera sensors"}
    }
    
    return {
        "width": w,
        "height": h,
        "channels": c,
        "dtype": dtype_str,
        "bit_depth": arr.itemsize * 8 * c,
        "raw_size_bytes": raw_size_bytes,
        "raw_size_kb": round(raw_size_bytes / 1024, 2),
        "format_guide": fmt_info.get(format_name.upper(), fmt_info["PNG"])
    }
