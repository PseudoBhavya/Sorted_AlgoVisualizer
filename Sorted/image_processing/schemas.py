"""
JSON Serializers and Schemas for Computer Vision API
====================================================
Formats image arrays and computational responses for REST API responses.
"""

from typing import Dict, Any, List, Tuple
import numpy as np
from .image_io import encode_image_base64, get_image_metadata


def serialize_image_response(
    result_img: np.ndarray,
    metadata: Dict[str, Any] = None,
    extra_data: Dict[str, Any] = None
) -> Dict[str, Any]:
    """
    Encodes an image numpy array into a base64 data URL and bundles metadata.
    """
    data_uri = encode_image_base64(result_img, format='png')
    img_meta = get_image_metadata(result_img, format_name='PNG')
    
    payload = {
        "status": "success",
        "image_data": data_uri,
        "metadata": img_meta
    }
    
    if metadata:
        payload["metadata"].update(metadata)
    if extra_data:
        payload.update(extra_data)
        
    return payload


def serialize_error_response(error_message: str, code: int = 400) -> Tuple[Dict[str, Any], int]:
    """Standardized error response."""
    return {
        "status": "error",
        "error": error_message
    }, code
