"""
AlgoLens API Schemas & Serializers
==================================
Serialization utilities converting ExecutionTrace and AlgorithmStep objects
into JSON-compliant dictionaries for the REST API.
"""

from typing import Dict, Any
from dataclasses import asdict
from algolens.algorithms.steps import ExecutionTrace, AlgorithmStep


def serialize_step(step: AlgorithmStep) -> Dict[str, Any]:
    """Serialize a single AlgorithmStep into a JSON dictionary."""
    return asdict(step)


def serialize_trace(trace: ExecutionTrace) -> Dict[str, Any]:
    """Serialize an entire ExecutionTrace with summary statistics and steps."""
    return {
        "algorithm_name": trace.algorithm_name,
        "input_data": trace.input_data,
        "result": trace.result,
        "total_steps": trace.total_steps,
        "metrics": {
            "comparisons": trace.total_comparisons,
            "swaps": trace.total_swaps,
            "shifts": trace.total_shifts,
            "max_recursion_depth": trace.max_recursion_depth,
            "execution_duration_sec": round(trace.end_time - trace.start_time, 6) if trace.end_time else 0.0
        },
        "recursion_tree": trace.recursion_tree,
        "steps": [serialize_step(s) for s in trace.steps]
    }
