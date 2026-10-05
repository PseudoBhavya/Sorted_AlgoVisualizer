"""
AlgoLens Searching Algorithms
=============================
Linear Search and Binary Search implementations with complete execution traces.
Every probe, comparison, boundary update, and state transition is captured.
"""

from .base import SearchingAlgorithm, InvalidInputError
from .steps import ExecutionTrace


class LinearSearch(SearchingAlgorithm):
    """Linear Search (Sequential Search) — checks each element one by one."""
    
    @property
    def name(self) -> str:
        return "Linear Search"
    
    @property
    def description(self) -> str:
        return (
            "Sequentially checks each element of the list in order until a match "
            "is found or the whole list has been searched. Does not require the array to be sorted."
        )
    
    @property
    def time_complexity_best(self) -> str:
        return "O(1)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def source_code(self) -> list:
        return [
            "def linear_search(arr, target):",
            "    for i in range(len(arr)):",
            "        if arr[i] == target:",
            "            return i",
            "    return -1"
        ]
    
    def _search(self, arr: list, target, trace: ExecutionTrace, **kwargs) -> int:
        n = len(arr)
        
        for i in range(n):
            trace.total_comparisons += 1
            is_match = (arr[i] == target)
            
            trace.add_step(
                operation='COMPARISON',
                array_state=arr,
                active_indices=[i],
                pointers={'current': i},
                comparison={
                    'left_index': i,
                    'right_index': -1,
                    'left_value': arr[i],
                    'right_value': target,
                    'result': is_match
                },
                explanation=(
                    f"Checking index {i}: arr[{i}] = {arr[i]}. "
                    f"Is {arr[i]} == {target}? {'Yes! Target found.' if is_match else 'No, advancing to next element.'}"
                ),
                code_line=3,
                code_highlight=f"if arr[{i}] == {target}:",
                variables={'i': i, 'target': target, 'arr[i]': arr[i], 'found': is_match}
            )
            
            if is_match:
                return i
        
        return -1


class BinarySearch(SearchingAlgorithm):
    """Binary Search — logarithmic divide-and-conquer search on sorted arrays."""
    
    @property
    def name(self) -> str:
        return "Binary Search"
    
    @property
    def description(self) -> str:
        return (
            "Efficiently searches a sorted array by repeatedly dividing the search "
            "interval in half. Compares the target value to the middle element."
        )
    
    @property
    def time_complexity_best(self) -> str:
        return "O(1)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def source_code(self) -> list:
        return [
            "def binary_search(arr, target):",
            "    low = 0",
            "    high = len(arr) - 1",
            "    while low <= high:",
            "        mid = (low + high) // 2",
            "        if arr[mid] == target:",
            "            return mid",
            "        elif arr[mid] < target:",
            "            low = mid + 1",
            "        else:",
            "            high = mid - 1",
            "    return -1"
        ]
    
    def _search(self, arr: list, target, trace: ExecutionTrace, **kwargs) -> int:
        n = len(arr)
        if n == 0:
            return -1
        
        # Binary search requires sorted array; check if sorted
        is_sorted = all(arr[i] <= arr[i + 1] for i in range(n - 1))
        if not is_sorted:
            # Sort array for search visualization and document step
            arr.sort()
            trace.add_step(
                operation='PREPARE',
                array_state=arr,
                explanation="Binary Search requires sorted input. Pre-sorted array before beginning search.",
                code_line=1,
                code_highlight="# Pre-sorting array for binary search",
                variables={'target': target, 'n': n, 'pre_sorted': True}
            )
        
        low = 0
        high = n - 1
        
        trace.add_step(
            operation='POINTER_MOVE',
            array_state=arr,
            active_indices=[low, high],
            pointers={'low': low, 'high': high},
            search_range={'low': low, 'mid': -1, 'high': high},
            explanation=f"Initialized search bounds: low = {low} (value: {arr[low]}), high = {high} (value: {arr[high]}).",
            code_line=2,
            code_highlight="low = 0; high = len(arr) - 1",
            variables={'low': low, 'high': high, 'target': target}
        )
        
        while low <= high:
            mid = (low + high) // 2
            mid_val = arr[mid]
            
            trace.add_step(
                operation='CALCULATE_MID',
                array_state=arr,
                active_indices=[mid],
                pointers={'low': low, 'mid': mid, 'high': high},
                search_range={'low': low, 'mid': mid, 'high': high},
                explanation=(
                    f"Calculate midpoint: mid = ({low} + {high}) // 2 = {mid}. "
                    f"Inspecting arr[{mid}] = {mid_val}."
                ),
                code_line=5,
                code_highlight=f"mid = ({low} + {high}) // 2",
                variables={'low': low, 'mid': mid, 'high': high, 'arr[mid]': mid_val, 'target': target}
            )
            
            trace.total_comparisons += 1
            is_match = (mid_val == target)
            
            trace.add_step(
                operation='COMPARISON',
                array_state=arr,
                active_indices=[mid],
                pointers={'low': low, 'mid': mid, 'high': high},
                search_range={'low': low, 'mid': mid, 'high': high},
                comparison={
                    'left_index': mid,
                    'right_index': -1,
                    'left_value': mid_val,
                    'right_value': target,
                    'result': is_match
                },
                explanation=(
                    f"Comparing arr[{mid}] ({mid_val}) with target ({target}). "
                    f"{'Found exact match!' if is_match else f'{mid_val} != {target}'}"
                ),
                code_line=6,
                code_highlight=f"if arr[{mid}] == {target}:",
                variables={'low': low, 'mid': mid, 'high': high, 'arr[mid]': mid_val, 'target': target}
            )
            
            if is_match:
                return mid
            
            trace.total_comparisons += 1
            if mid_val < target:
                trace.add_step(
                    operation='NARROW_RANGE',
                    array_state=arr,
                    active_indices=[mid],
                    pointers={'low': low, 'mid': mid, 'high': high},
                    search_range={'low': low, 'mid': mid, 'high': high},
                    explanation=(
                        f"arr[{mid}] ({mid_val}) < target ({target}). "
                        f"Target must be in the right half. Eliminating range [{low}..{mid}], updating low = {mid + 1}."
                    ),
                    code_line=9,
                    code_highlight=f"low = {mid + 1}",
                    variables={'low': mid + 1, 'high': high, 'eliminated': f"[{low}..{mid}]"}
                )
                low = mid + 1
            else:
                trace.add_step(
                    operation='NARROW_RANGE',
                    array_state=arr,
                    active_indices=[mid],
                    pointers={'low': low, 'mid': mid, 'high': high},
                    search_range={'low': low, 'mid': mid, 'high': high},
                    explanation=(
                        f"arr[{mid}] ({mid_val}) > target ({target}). "
                        f"Target must be in the left half. Eliminating range [{mid}..{high}], updating high = {mid - 1}."
                    ),
                    code_line=11,
                    code_highlight=f"high = {mid - 1}",
                    variables={'low': low, 'high': mid - 1, 'eliminated': f"[{mid}..{high}]"}
                )
                high = mid - 1
        
        return -1
