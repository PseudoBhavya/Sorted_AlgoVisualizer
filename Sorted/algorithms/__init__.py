# AlgoLens Algorithm Engine
# Core algorithm framework with OOP architecture

from .base import Algorithm, SortingAlgorithm, SearchingAlgorithm
from .steps import AlgorithmStep, ExecutionTrace
from .sorting import (
    BubbleSort, SelectionSort, InsertionSort,
    MergeSort, QuickSort, HeapSort
)
from .searching import LinearSearch, BinarySearch
from .daa_fundamentals import (
    MinMaxLinear, MinMaxDivideConquer, DynamicArrayInsertion,
    KBitCounter, ClosestPairBruteForce, ClosestPairDivideConquer,
    MatrixMultiplicationStandard, FibonacciIterative,
    FibonacciRecursive, SumOfDigits
)
from .ai_search import (
    DepthFirstSearch, BreadthFirstSearch, GreedyBestFirstSearch,
    AStarSearch, WeightedAStarSearch, AISearchComparison
)
from .theory import DAATheoryRegistry
from .registry import AlgorithmRegistry

__all__ = [
    'Algorithm', 'SortingAlgorithm', 'SearchingAlgorithm',
    'AlgorithmStep', 'ExecutionTrace',
    'BubbleSort', 'SelectionSort', 'InsertionSort',
    'MergeSort', 'QuickSort', 'HeapSort',
    'LinearSearch', 'BinarySearch',
    'MinMaxLinear', 'MinMaxDivideConquer', 'DynamicArrayInsertion',
    'KBitCounter', 'ClosestPairBruteForce', 'ClosestPairDivideConquer',
    'MatrixMultiplicationStandard', 'FibonacciIterative',
    'FibonacciRecursive', 'SumOfDigits',
    'DepthFirstSearch', 'BreadthFirstSearch', 'GreedyBestFirstSearch',
    'AStarSearch', 'WeightedAStarSearch', 'AISearchComparison',
    'DAATheoryRegistry',
    'AlgorithmRegistry'
]
