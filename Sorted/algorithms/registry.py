"""
AlgoLens Algorithm Registry
===========================
Central factory and lookup registry for all available algorithms.
Implements the Registry / Factory design pattern.
"""

from typing import Type, Optional
from .base import Algorithm, AlgorithmNotFoundError
from .sorting import (
    BubbleSort, SelectionSort, InsertionSort,
    MergeSort, QuickSort, HeapSort
)
from .searching import LinearSearch, BinarySearch


class AlgorithmRegistry:
    """Registry maintaining all available algorithms in AlgoLens."""
    
    _algorithms: dict[str, Type[Algorithm]] = {}
    _instances: dict[str, Algorithm] = {}
    
    @classmethod
    def register(cls, algorithm_cls: Type[Algorithm]):
        """Register an algorithm class."""
        key = algorithm_cls().name.lower().replace(" ", "_")
        cls._algorithms[key] = algorithm_cls
        # Also register by exact lowercase name
        cls._algorithms[algorithm_cls().name.lower()] = algorithm_cls
    
    @classmethod
    def get(cls, name: str) -> Algorithm:
        """Get an algorithm instance by name (case-insensitive, spaces or underscores).
        
        Args:
            name: e.g. "Quick Sort", "quick_sort", "quicksort", "bubble"
            
        Returns:
            Algorithm instance
            
        Raises:
            AlgorithmNotFoundError: If no matching algorithm is found
        """
        key = name.strip().lower()
        alt_key = key.replace(" ", "_")
        compact_key = key.replace(" ", "").replace("_", "")
        
        # Exact or standard key lookup
        for test_key in [key, alt_key]:
            if test_key in cls._algorithms:
                algo_cls = cls._algorithms[test_key]
                if algo_cls not in cls._instances:
                    cls._instances[algo_cls] = algo_cls()
                return cls._instances[algo_cls]
        
        # Fuzzy / compact match lookup
        for reg_key, algo_cls in cls._algorithms.items():
            if reg_key.replace(" ", "").replace("_", "") == compact_key:
                if algo_cls not in cls._instances:
                    cls._instances[algo_cls] = algo_cls()
                return cls._instances[algo_cls]
        
        available = list({a().name for a in cls._algorithms.values()})
        raise AlgorithmNotFoundError(
            f"Algorithm '{name}' not found. Available algorithms: {', '.join(sorted(available))}"
        )
    
    @classmethod
    def get_all(cls) -> list[Algorithm]:
        """Return instances of all registered algorithms (unique)."""
        unique_classes = {cls._algorithms[k] for k in cls._algorithms}
        return [cls._get_or_create(c) for c in unique_classes]
    
    @classmethod
    def get_by_category(cls, category: str) -> list[Algorithm]:
        """Return algorithms filtered by category ('Sorting', 'Searching')."""
        return [algo for algo in cls.get_all() if algo.category.lower() == category.lower()]
    
    @classmethod
    def get_categories(cls) -> list[str]:
        """Return list of distinct categories."""
        return sorted(list({algo.category for algo in cls.get_all()}))
    
    @classmethod
    def list_all_info(cls) -> list[dict]:
        """Return metadata list of all registered algorithms."""
        return [algo.get_info() for algo in cls.get_all()]
    
    @classmethod
    def _get_or_create(cls, algo_cls: Type[Algorithm]) -> Algorithm:
        if algo_cls not in cls._instances:
            cls._instances[algo_cls] = algo_cls()
        return cls._instances[algo_cls]


# Auto-register all 8 core algorithms
AlgorithmRegistry.register(QuickSort)
AlgorithmRegistry.register(MergeSort)
AlgorithmRegistry.register(HeapSort)
AlgorithmRegistry.register(InsertionSort)
AlgorithmRegistry.register(SelectionSort)
AlgorithmRegistry.register(BubbleSort)
AlgorithmRegistry.register(BinarySearch)
AlgorithmRegistry.register(LinearSearch)
