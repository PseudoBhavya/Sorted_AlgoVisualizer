"""
AlgoLens REST API Routes
========================
Provides RESTful endpoints for algorithm inspection, execution traces,
comparisons, and dataset management.
"""

from flask import Blueprint, request, jsonify
try:
    from Sorted.algorithms.registry import AlgorithmRegistry
    from Sorted.algorithms.base import AlgorithmError
    from Sorted.validation.validators import InputValidator, ValidationError
    from Sorted.data.datasets import DatasetGenerator
    from Sorted.analytics.pandas_analysis import PerformanceAnalytics
except ImportError:
    from algolens.algorithms.registry import AlgorithmRegistry
    from algolens.algorithms.base import AlgorithmError
    from algolens.validation.validators import InputValidator, ValidationError
    from algolens.data.datasets import DatasetGenerator
    from algolens.analytics.pandas_analysis import PerformanceAnalytics
from .schemas import serialize_trace

api_bp = Blueprint('api', __name__, url_prefix='/api')


@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "service": "AlgoLens Execution Engine API",
        "version": "1.0.0",
        "registered_algorithms": len(AlgorithmRegistry.get_all())
    }), 200


@api_bp.route('/algorithms', methods=['GET'])
def list_algorithms():
    """List all registered algorithms with their metadata and complexity profiles."""
    category = request.args.get('category')
    if category:
        algos = AlgorithmRegistry.get_by_category(category)
        data = [a.get_info() for a in algos]
    else:
        data = AlgorithmRegistry.list_all_info()
    return jsonify({"count": len(data), "algorithms": data}), 200


@api_bp.route('/algorithms/<name>', methods=['GET'])
def get_algorithm_detail(name: str):
    """Retrieve metadata and source code for a specific algorithm."""
    try:
        algo = AlgorithmRegistry.get(name)
        info = algo.get_info()
        info['source_code'] = algo.source_code
        return jsonify(info), 200
    except AlgorithmError as e:
        return jsonify({"error": str(e)}), 404


@api_bp.route('/execute', methods=['POST'])
def execute_algorithm():
    """Execute an algorithm on provided array data and return the full step-by-step trace."""
    body = request.get_json(silent=True) or {}
    
    algo_name = body.get('algorithm')
    if not algo_name:
        return jsonify({"error": "Missing 'algorithm' parameter in JSON payload."}), 400
    
    raw_data = body.get('data')
    if raw_data is None:
        return jsonify({"error": "Missing 'data' parameter in JSON payload."}), 400
    
    try:
        if isinstance(raw_data, str):
            data = InputValidator.parse_array_input(raw_data)
        elif isinstance(raw_data, list):
            data = [int(x) if isinstance(x, (int, float)) and x == int(x) else float(x) for x in raw_data]
        else:
            return jsonify({"error": "Data must be a list of numbers or comma-separated string."}), 400
    except ValidationError as ve:
        return jsonify({"error": f"Validation failed: {str(ve)}"}), 422
    
    extra_params = body.get('params', {})
    
    # If target is provided directly in body, pass it
    if 'target' in body and 'target' not in extra_params:
        extra_params['target'] = body['target']
    
    try:
        algo = AlgorithmRegistry.get(algo_name)
        trace = algo.execute(data, **extra_params)
        return jsonify(serialize_trace(trace)), 200
    except AlgorithmError as ae:
        return jsonify({"error": str(ae)}), 400
    except Exception as e:
        return jsonify({"error": f"Internal execution error: {str(e)}"}), 500


@api_bp.route('/compare', methods=['POST'])
def compare_algorithms():
    """Run multiple algorithms on the same dataset and return comparative performance metrics."""
    body = request.get_json(silent=True) or {}
    
    algo_names = body.get('algorithms')
    if not algo_names or not isinstance(algo_names, list):
        return jsonify({"error": "Missing 'algorithms' list in JSON payload."}), 400
        
    raw_data = body.get('data')
    if raw_data is None:
        data = DatasetGenerator.DEFAULT_WORKSPACE_DATA
    elif isinstance(raw_data, str):
        try:
            data = InputValidator.parse_array_input(raw_data)
        except ValidationError as ve:
            return jsonify({"error": str(ve)}), 422
    elif isinstance(raw_data, list):
        data = raw_data
    else:
        return jsonify({"error": "Data must be a list of numbers or formatted string."}), 400
        
    df = PerformanceAnalytics.compare_on_dataset(algo_names, data)
    return jsonify({
        "dataset_size": len(data),
        "results": df.to_dict(orient="records")
    }), 200


@api_bp.route('/datasets', methods=['GET'])
def list_datasets():
    """List all available preset benchmark datasets."""
    presets = DatasetGenerator.list_presets()
    result = {name: DatasetGenerator.get_preset(name) for name in presets}
    return jsonify({"presets": result}), 200


@api_bp.route('/datasets/<name>', methods=['GET'])
def get_dataset(name: str):
    """Retrieve data elements for a specific preset."""
    if name not in DatasetGenerator.PRESETS:
        return jsonify({"error": f"Dataset '{name}' not found."}), 404
    return jsonify({
        "name": name,
        "data": DatasetGenerator.get_preset(name),
        "size": len(DatasetGenerator.get_preset(name))
    }), 200


@api_bp.route('/validate', methods=['POST'])
def validate_input_data():
    """Validate user input string using regex validator."""
    body = request.get_json(silent=True) or {}
    raw_text = body.get('text', '')
    try:
        parsed = InputValidator.parse_array_input(raw_text)
        return jsonify({
            "valid": True,
            "parsed": parsed,
            "count": len(parsed)
        }), 200
    except ValidationError as ve:
        return jsonify({
            "valid": False,
            "error": str(ve)
        }), 400
