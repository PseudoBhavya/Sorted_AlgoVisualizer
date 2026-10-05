"""
AlgoLens Algorithm Base Classes
================================
Abstract base classes implementing the OOP architecture.

Hierarchy:
    Algorithm (ABC)
    ├── SortingAlgorithm (ABC)
    │   ├── BubbleSort
    │   ├── SelectionSort
    │   ├── InsertionSort
    │   ├── MergeSort
    │   ├── QuickSort
    │   └── HeapSort
    └── SearchingAlgorithm (ABC)
        ├── LinearSearch
        └── BinarySearch

Uses:
- Abstract classes (abc module)
- Inheritance
- Polymorphism
- Exception handling
"""

from abc import ABC, abstractmethod
from typing import Optional
from .steps import ExecutionTrace


class AlgorithmError(Exception):
    """Base exception for algorithm-related errors."""
    pass


class InvalidInputError(AlgorithmError):
    """Raised when input data is invalid."""
    pass


class EmptyDataError(AlgorithmError):
    """Raised when input data is empty."""
    pass


class AlgorithmNotFoundError(AlgorithmError):
    """Raised when a requested algorithm doesn't exist."""
    pass


class Algorithm(ABC):
    """Abstract base class for all algorithms in AlgoLens.
    
    Every algorithm must:
    1. Define its metadata (name, category, complexities)
    2. Implement execute() to run with trace generation
    3. Provide its source code for display
    4. Validate its input
    """
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Human-readable algorithm name."""
        pass
    
    @property
    @abstractmethod
    def category(self) -> str:
        """Algorithm category: 'Sorting', 'Searching', etc."""
        pass
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Brief description of the algorithm."""
        pass
    
    @property
    @abstractmethod
    def time_complexity_best(self) -> str:
        """Best-case time complexity."""
        pass
    
    @property
    @abstractmethod
    def time_complexity_average(self) -> str:
        """Average-case time complexity."""
        pass
    
    @property
    @abstractmethod
    def time_complexity_worst(self) -> str:
        """Worst-case time complexity."""
        pass
    
    @property
    @abstractmethod
    def space_complexity(self) -> str:
        """Space complexity."""
        pass
    
    @property
    @abstractmethod
    def source_code(self) -> list[str]:
        """Source code lines for display in the code panel."""
        pass
    
    @property
    def is_stable(self) -> bool:
        """Whether the algorithm is stable."""
        return False
    
    @property
    def is_in_place(self) -> bool:
        """Whether the algorithm sorts in-place."""
        return True
    
    @property
    def is_implemented(self) -> bool:
        """Whether this algorithm is fully implemented."""
        return True
    
    def validate_input(self, data: list) -> list:
        """Validate and sanitize input data.
        
        Args:
            data: Input list
            
        Returns:
            Validated list of numbers
            
        Raises:
            EmptyDataError: If data is empty
            InvalidInputError: If data contains non-numeric values
        """
        if data is None:
            raise EmptyDataError("Input data cannot be None.")
        if not isinstance(data, (list, tuple)):
            raise InvalidInputError(f"Expected a list, got {type(data).__name__}.")
        if len(data) == 0:
            raise EmptyDataError("Input data cannot be empty.")
        
        validated = []
        for i, val in enumerate(data):
            try:
                validated.append(int(val) if isinstance(val, (int, float)) and val == int(val) else float(val))
            except (ValueError, TypeError):
                raise InvalidInputError(
                    f"Invalid value at index {i}: '{val}'. Expected a number."
                )
        return validated
    
    @abstractmethod
    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        """Execute the algorithm on the given data, generating a complete trace.
        
        Args:
            data: Input data list
            **kwargs: Algorithm-specific parameters
            
        Returns:
            ExecutionTrace with all steps recorded
        """
        pass
    
    def get_info(self) -> dict:
        """Get algorithm metadata as a dictionary."""
        return {
            'name': self.name,
            'category': self.category,
            'description': self.description,
            'time_complexity': {
                'best': self.time_complexity_best,
                'average': self.time_complexity_average,
                'worst': self.time_complexity_worst
            },
            'space_complexity': self.space_complexity,
            'stable': self.is_stable,
            'in_place': self.is_in_place,
            'implemented': self.is_implemented
        }


class SortingAlgorithm(Algorithm):
    """Abstract base class for all sorting algorithms.
    
    Sorting algorithms take a list of numbers and produce
    a sorted list along with a complete execution trace.
    """
    
    @property
    def category(self) -> str:
        return "Sorting"
    
    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        """Execute the sorting algorithm.
        
        Args:
            data: List of numbers to sort
            **kwargs: Algorithm-specific parameters
            
        Returns:
            ExecutionTrace with all steps
        """
        validated = self.validate_input(data)
        arr = list(validated)
        trace = ExecutionTrace(self.name, validated)
        trace.begin()
        
        # Add initial state step
        trace.add_step(
            operation='INIT',
            array_state=arr,
            explanation=f"Starting {self.name} on {len(arr)} elements.",
            code_line=1,
            code_highlight=f"def {self.name.lower().replace(' ', '_')}(arr):",
            variables={'n': len(arr)}
        )
        
        # Run the actual sort (implemented by each subclass)
        result = self._sort(arr, trace, **kwargs)
        
        # Add completion step
        trace.add_step(
            operation='COMPLETE',
            array_state=result,
            sorted_indices=list(range(len(result))),
            explanation=f"{self.name} complete. Array is now sorted.",
            code_line=len(self.source_code),
            code_highlight="return arr",
            variables={'n': len(result), 'sorted': True}
        )
        
        trace.end(result)
        trace.finalize()
        return trace
    
    @abstractmethod
    def _sort(self, arr: list, trace: ExecutionTrace, **kwargs) -> list:
        """Internal sorting implementation that records trace steps.
        
        Args:
            arr: Mutable list to sort
            trace: Execution trace to record steps into
            
        Returns:
            Sorted list
        """
        pass


class SearchingAlgorithm(Algorithm):
    """Abstract base class for all searching algorithms.
    
    Searching algorithms take a list and a target, and produce
    the index of the target (or -1) along with a complete trace.
    """
    
    @property
    def category(self) -> str:
        return "Searching"
    
    @property
    def is_in_place(self) -> bool:
        return True  # Searching doesn't modify the array
    
    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        """Execute the searching algorithm.
        
        Args:
            data: List to search in
            **kwargs: Must include 'target' - the value to search for
            
        Returns:
            ExecutionTrace with all steps
        """
        target = kwargs.get('target')
        if target is None:
            raise InvalidInputError("Search target must be provided.")
        
        try:
            target = int(target) if isinstance(target, (int, float)) and target == int(target) else float(target)
        except (ValueError, TypeError):
            raise InvalidInputError(f"Invalid search target: '{target}'. Expected a number.")
        
        validated = self.validate_input(data)
        arr = list(validated)
        trace = ExecutionTrace(self.name, validated)
        trace.begin()
        
        # Add initial state step
        trace.add_step(
            operation='INIT',
            array_state=arr,
            explanation=f"Starting {self.name} for target {target} in {len(arr)} elements.",
            code_line=1,
            variables={'target': target, 'n': len(arr)}
        )
        
        # Run the actual search
        clean_kwargs = {k: v for k, v in kwargs.items() if k != 'target'}
        result = self._search(arr, target, trace, **clean_kwargs)
        
        # Add completion step
        if result >= 0:
            trace.add_step(
                operation='FOUND',
                array_state=arr,
                active_indices=[result],
                explanation=f"Target {target} found at index {result}.",
                code_line=len(self.source_code),
                variables={'target': target, 'result': result, 'found': True}
            )
        else:
            trace.add_step(
                operation='NOT_FOUND',
                array_state=arr,
                explanation=f"Target {target} not found in the array.",
                code_line=len(self.source_code),
                variables={'target': target, 'result': -1, 'found': False}
            )
        
        trace.end(result)
        trace.finalize()
        return trace
    
    @abstractmethod
    def _search(self, arr: list, target, trace: ExecutionTrace, **kwargs) -> int:
        """Internal search implementation that records trace steps.
        
        Args:
            arr: List to search in
            target: Value to search for
            trace: Execution trace to record steps into
            
        Returns:
            Index of target, or -1 if not found
        """
        pass
