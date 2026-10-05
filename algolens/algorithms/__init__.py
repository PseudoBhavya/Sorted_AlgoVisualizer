# AlgoLens Algorithm Engine
# Core algorithm framework with OOP architecture

from .base import Algorithm, SortingAlgorithm, SearchingAlgorithm
from .steps import AlgorithmStep, ExecutionTrace
from .sorting import (
    BubbleSort, SelectionSort, InsertionSort,
    MergeSort, QuickSort, HeapSort
)
from .searching import LinearSearch, BinarySearch
from .registry import AlgorithmRegistry

__all__ = [
    'Algorithm', 'SortingAlgorithm', 'SearchingAlgorithm',
    'AlgorithmStep', 'ExecutionTrace',
    'BubbleSort', 'SelectionSort', 'InsertionSort',
    'MergeSort', 'QuickSort', 'HeapSort',
    'LinearSearch', 'BinarySearch',
    'AlgorithmRegistry'
]
