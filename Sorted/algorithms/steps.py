"""
AlgoLens Execution Trace Engine
================================
The MOST IMPORTANT technical component of AlgoLens.

Every visual event corresponds to a REAL algorithm event.
No fake animation frames — every step represents an actual operation:
comparison, swap, pointer movement, pivot selection, partition,
recursive call, return, merge.

Each AlgorithmStep captures the complete algorithm state at that moment.
"""

import time
import copy
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class AlgorithmStep:
    """Represents a single execution step in an algorithm's trace.
    
    This is the atomic unit of algorithm execution visualization.
    Every field reflects the REAL state of the algorithm at this point.
    """
    step_number: int
    operation: str  # COMPARISON, SWAP, PIVOT_SELECT, PARTITION, RECURSIVE_CALL, RETURN, MERGE, SHIFT, FOUND, NOT_FOUND, HEAPIFY, EXTRACT_MAX, INSERT_KEY
    array_state: list  # Current state of the entire array
    active_indices: list = field(default_factory=list)  # Indices currently being operated on
    comparison: Optional[dict] = None  # {'left_index': i, 'right_index': j, 'left_value': v1, 'right_value': v2, 'result': bool}
    swap: Optional[dict] = None  # {'index_a': i, 'index_b': j, 'value_a': v1, 'value_b': v2}
    variables: dict = field(default_factory=dict)  # All algorithm-specific variables
    pointers: dict = field(default_factory=dict)  # Named pointers: {'left': 2, 'right': 7, 'pivot_index': 0}
    pivot: Optional[dict] = None  # {'value': 45, 'index': 0}
    recursion_state: Optional[dict] = None  # {'depth': 2, 'call': 'quickSort(0, 7)', 'parent': 'quickSort(0, 15)'}
    explanation: str = ""  # Human-readable "Why this step?" text
    code_line: int = 0  # Line number in the algorithm's pseudocode/source
    code_highlight: str = ""  # The actual code text being executed
    metrics: dict = field(default_factory=dict)  # Running metrics: comparisons, swaps, etc.
    sorted_indices: list = field(default_factory=list)  # Indices confirmed in final sorted position
    partition_range: Optional[dict] = None  # {'low': 0, 'high': 7} - current partition boundaries
    subarrays: Optional[dict] = None  # For merge sort: {'left': [...], 'right': [...]}
    search_range: Optional[dict] = None  # For search: {'low': 0, 'mid': 4, 'high': 7}
    timestamp: float = 0.0  # Time relative to execution start


class ExecutionTrace:
    """Complete execution trace for an algorithm run.
    
    Stores all steps, manages metrics, and provides
    replay/navigation capabilities.
    """
    
    def __init__(self, algorithm_name: str, input_data: list):
        self.algorithm_name = algorithm_name
        self.input_data = list(input_data)  # Original input (immutable copy)
        self.steps: list[AlgorithmStep] = []
        self.result = None  # Final sorted array or search result
        self.start_time = 0.0
        self.end_time = 0.0
        self.total_comparisons = 0
        self.total_swaps = 0
        self.total_shifts = 0
        self.max_recursion_depth = 0
        self.current_recursion_depth = 0
        self.recursion_tree: list[dict] = []  # Tree structure for visualization
        self._step_counter = 0
    
    def begin(self):
        """Mark the beginning of algorithm execution."""
        self.start_time = time.time()
    
    def end(self, result):
        """Mark the end of algorithm execution with the result."""
        self.end_time = time.time()
        self.result = result
    
    def add_step(self, operation: str, array_state: list, **kwargs) -> AlgorithmStep:
        """Add a new execution step to the trace.
        
        Args:
            operation: The type of operation (COMPARISON, SWAP, etc.)
            array_state: Current state of the array (will be deep copied)
            **kwargs: Additional step fields
            
        Returns:
            The created AlgorithmStep
        """
        self._step_counter += 1
        
        # Build running metrics
        metrics = {
            'comparisons': self.total_comparisons,
            'swaps': self.total_swaps,
            'shifts': self.total_shifts,
            'recursion_depth': self.current_recursion_depth,
            'max_recursion_depth': self.max_recursion_depth,
            'step': self._step_counter,
            'total_steps': 0  # Updated after execution completes
        }
        
        step = AlgorithmStep(
            step_number=self._step_counter,
            operation=operation,
            array_state=copy.deepcopy(array_state),
            active_indices=kwargs.get('active_indices', []),
            comparison=kwargs.get('comparison'),
            swap=kwargs.get('swap'),
            variables=kwargs.get('variables', {}),
            pointers=kwargs.get('pointers', {}),
            pivot=kwargs.get('pivot'),
            recursion_state=kwargs.get('recursion_state'),
            explanation=kwargs.get('explanation', ''),
            code_line=kwargs.get('code_line', 0),
            code_highlight=kwargs.get('code_highlight', ''),
            metrics=metrics,
            sorted_indices=kwargs.get('sorted_indices', []),
            partition_range=kwargs.get('partition_range'),
            subarrays=kwargs.get('subarrays'),
            search_range=kwargs.get('search_range'),
            timestamp=time.time() - self.start_time if self.start_time else 0.0
        )
        
        self.steps.append(step)
        return step
    
    def increment_comparisons(self):
        """Track a comparison operation."""
        self.total_comparisons += 1
    
    def increment_swaps(self):
        """Track a swap operation."""
        self.total_swaps += 1
    
    def increment_shifts(self):
        """Track a shift/move operation."""
        self.total_shifts += 1
    
    def push_recursion(self, call_info: dict):
        """Track entering a recursive call."""
        self.current_recursion_depth += 1
        if self.current_recursion_depth > self.max_recursion_depth:
            self.max_recursion_depth = self.current_recursion_depth
        self.recursion_tree.append(call_info)
    
    def pop_recursion(self):
        """Track returning from a recursive call."""
        if self.current_recursion_depth > 0:
            self.current_recursion_depth -= 1
    
    def finalize(self):
        """Finalize the trace after execution completes.
        Updates total_steps in all step metrics.
        """
        total = len(self.steps)
        for step in self.steps:
            step.metrics['total_steps'] = total
    
    def get_step(self, step_number: int) -> Optional[AlgorithmStep]:
        """Get a specific step by number (1-indexed)."""
        if 1 <= step_number <= len(self.steps):
            return self.steps[step_number - 1]
        return None
    
    @property
    def total_steps(self) -> int:
        """Total number of execution steps."""
        return len(self.steps)
    
    @property
    def execution_time(self) -> float:
        """Total execution time in seconds."""
        if self.end_time and self.start_time:
            return self.end_time - self.start_time
        return 0.0
    
    def to_dict(self) -> dict:
        """Serialize the entire trace to a dictionary for JSON export."""
        return {
            'algorithm': self.algorithm_name,
            'input': self.input_data,
            'result': self.result,
            'total_steps': self.total_steps,
            'total_comparisons': self.total_comparisons,
            'total_swaps': self.total_swaps,
            'total_shifts': self.total_shifts,
            'max_recursion_depth': self.max_recursion_depth,
            'execution_time_ms': round(self.execution_time * 1000, 2),
            'steps': [self._step_to_dict(s) for s in self.steps]
        }
    
    def _step_to_dict(self, step: AlgorithmStep) -> dict:
        """Serialize a single step to a dictionary."""
        d = {
            'step_number': step.step_number,
            'operation': step.operation,
            'array_state': step.array_state,
            'active_indices': step.active_indices,
            'explanation': step.explanation,
            'code_line': step.code_line,
            'code_highlight': step.code_highlight,
            'metrics': step.metrics,
            'variables': step.variables,
            'pointers': step.pointers,
            'sorted_indices': step.sorted_indices,
            'timestamp': round(step.timestamp, 6)
        }
        if step.comparison:
            d['comparison'] = step.comparison
        if step.swap:
            d['swap'] = step.swap
        if step.pivot:
            d['pivot'] = step.pivot
        if step.recursion_state:
            d['recursion_state'] = step.recursion_state
        if step.partition_range:
            d['partition_range'] = step.partition_range
        if step.subarrays:
            d['subarrays'] = step.subarrays
        if step.search_range:
            d['search_range'] = step.search_range
        return d
    
    def get_summary(self) -> dict:
        """Get a summary of the execution for analytics."""
        return {
            'algorithm': self.algorithm_name,
            'input_size': len(self.input_data),
            'total_steps': self.total_steps,
            'comparisons': self.total_comparisons,
            'swaps': self.total_swaps,
            'shifts': self.total_shifts,
            'max_recursion_depth': self.max_recursion_depth,
            'execution_time_ms': round(self.execution_time * 1000, 2)
        }
