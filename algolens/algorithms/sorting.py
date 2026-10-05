"""
AlgoLens Sorting Algorithms
=============================
All sorting algorithm implementations with step-by-step execution traces.
Each algorithm generates detailed AlgorithmStep objects that capture
every comparison, swap, pointer movement, and decision.

Quick Sort is the FLAGSHIP algorithm with the most detailed trace.
"""

import copy
from .base import SortingAlgorithm
from .steps import ExecutionTrace


class BubbleSort(SortingAlgorithm):
    """Bubble Sort — repeatedly swaps adjacent elements."""
    
    @property
    def name(self) -> str:
        return "Bubble Sort"
    
    @property
    def description(self) -> str:
        return "Repeatedly steps through the list, compares adjacent elements, and swaps them if they are in the wrong order. The pass through the list is repeated until no swaps are needed."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n²)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def is_stable(self) -> bool:
        return True
    
    @property
    def source_code(self) -> list:
        return [
            "def bubble_sort(arr):",
            "    n = len(arr)",
            "    for i in range(n - 1):",
            "        swapped = False",
            "        for j in range(n - 1 - i):",
            "            if arr[j] > arr[j + 1]:",
            "                arr[j], arr[j+1] = arr[j+1], arr[j]",
            "                swapped = True",
            "        if not swapped:",
            "            break",
            "    return arr"
        ]
    
    def _sort(self, arr, trace, **kwargs):
        n = len(arr)
        sorted_indices = []
        
        for i in range(n - 1):
            swapped = False
            
            trace.add_step(
                operation='PASS_START',
                array_state=arr,
                active_indices=[],
                sorted_indices=list(sorted_indices),
                explanation=f"Starting pass {i + 1}. Elements after index {n - 1 - i} are sorted.",
                code_line=3,
                code_highlight=f"for i in range(n - 1):  # i = {i}",
                variables={'i': i, 'n': n, 'pass': i + 1},
                pointers={'i': i, 'sorted_boundary': n - 1 - i}
            )
            
            for j in range(n - 1 - i):
                # Comparison step
                trace.increment_comparisons()
                comp_result = arr[j] > arr[j + 1]
                
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[j, j + 1],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': j, 'right_index': j + 1,
                        'left_value': arr[j], 'right_value': arr[j + 1],
                        'result': comp_result
                    },
                    explanation=f"Compare {arr[j]} (index {j}) with {arr[j+1]} (index {j+1}). "
                               f"{'They are out of order — swap needed.' if comp_result else 'They are in order — no swap needed.'}",
                    code_line=6,
                    code_highlight=f"if arr[{j}] > arr[{j+1}]:  # {arr[j]} > {arr[j+1]}",
                    variables={'i': i, 'j': j, 'comparing': f"{arr[j]} vs {arr[j+1]}"},
                    pointers={'j': j, 'j+1': j + 1, 'sorted_boundary': n - 1 - i}
                )
                
                if comp_result:
                    # Swap step
                    trace.increment_swaps()
                    val_a, val_b = arr[j], arr[j + 1]
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    swapped = True
                    
                    trace.add_step(
                        operation='SWAP',
                        array_state=arr,
                        active_indices=[j, j + 1],
                        sorted_indices=list(sorted_indices),
                        swap={
                            'index_a': j, 'index_b': j + 1,
                            'value_a': val_a, 'value_b': val_b
                        },
                        explanation=f"Swap {val_a} and {val_b}. {val_b} moves left, {val_a} bubbles right.",
                        code_line=7,
                        code_highlight=f"arr[{j}], arr[{j+1}] = arr[{j+1}], arr[{j}]",
                        variables={'i': i, 'j': j, 'swapped': True},
                        pointers={'j': j, 'j+1': j + 1, 'sorted_boundary': n - 1 - i}
                    )
            
            # Mark the element that bubbled to its final position
            sorted_indices.append(n - 1 - i)
            
            if not swapped:
                trace.add_step(
                    operation='EARLY_EXIT',
                    array_state=arr,
                    sorted_indices=list(range(n)),
                    explanation=f"No swaps occurred in pass {i + 1}. Array is already sorted — early termination.",
                    code_line=10,
                    code_highlight="break  # No swaps in this pass",
                    variables={'i': i, 'swapped': False}
                )
                break
        
        return arr


class SelectionSort(SortingAlgorithm):
    """Selection Sort — finds minimum and places it at the beginning."""
    
    @property
    def name(self) -> str:
        return "Selection Sort"
    
    @property
    def description(self) -> str:
        return "Divides the array into sorted and unsorted regions. Repeatedly selects the minimum element from the unsorted region and places it at the end of the sorted region."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n²)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n²)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def source_code(self) -> list:
        return [
            "def selection_sort(arr):",
            "    n = len(arr)",
            "    for i in range(n - 1):",
            "        min_idx = i",
            "        for j in range(i + 1, n):",
            "            if arr[j] < arr[min_idx]:",
            "                min_idx = j",
            "        if min_idx != i:",
            "            arr[i], arr[min_idx] = arr[min_idx], arr[i]",
            "    return arr"
        ]
    
    def _sort(self, arr, trace, **kwargs):
        n = len(arr)
        sorted_indices = []
        
        for i in range(n - 1):
            min_idx = i
            
            trace.add_step(
                operation='SCAN_START',
                array_state=arr,
                active_indices=[i],
                sorted_indices=list(sorted_indices),
                explanation=f"Looking for the minimum element in the unsorted region [{i}..{n-1}]. Current minimum is {arr[i]} at index {i}.",
                code_line=4,
                code_highlight=f"min_idx = {i}",
                variables={'i': i, 'min_idx': i, 'min_value': arr[i]},
                pointers={'current_position': i, 'min_idx': i}
            )
            
            for j in range(i + 1, n):
                trace.increment_comparisons()
                comp_result = arr[j] < arr[min_idx]
                
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[j, min_idx],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': j, 'right_index': min_idx,
                        'left_value': arr[j], 'right_value': arr[min_idx],
                        'result': comp_result
                    },
                    explanation=f"Compare {arr[j]} (index {j}) with current minimum {arr[min_idx]} (index {min_idx}). "
                               f"{'New minimum found!' if comp_result else 'Current minimum is still smaller.'}",
                    code_line=6,
                    code_highlight=f"if arr[{j}] < arr[{min_idx}]:  # {arr[j]} < {arr[min_idx]}",
                    variables={'i': i, 'j': j, 'min_idx': min_idx, 'min_value': arr[min_idx]},
                    pointers={'current_position': i, 'scanning': j, 'min_idx': min_idx}
                )
                
                if comp_result:
                    min_idx = j
            
            if min_idx != i:
                trace.increment_swaps()
                val_a, val_b = arr[i], arr[min_idx]
                arr[i], arr[min_idx] = arr[min_idx], arr[i]
                
                trace.add_step(
                    operation='SWAP',
                    array_state=arr,
                    active_indices=[i, min_idx],
                    sorted_indices=list(sorted_indices),
                    swap={
                        'index_a': i, 'index_b': min_idx,
                        'value_a': val_a, 'value_b': val_b
                    },
                    explanation=f"Place minimum value {val_b} at position {i} by swapping with {val_a}.",
                    code_line=9,
                    code_highlight=f"arr[{i}], arr[{min_idx}] = arr[{min_idx}], arr[{i}]",
                    variables={'i': i, 'min_idx': min_idx},
                    pointers={'current_position': i, 'min_idx': min_idx}
                )
            
            sorted_indices.append(i)
        
        sorted_indices.append(n - 1)
        return arr


class InsertionSort(SortingAlgorithm):
    """Insertion Sort — builds sorted array one element at a time."""
    
    @property
    def name(self) -> str:
        return "Insertion Sort"
    
    @property
    def description(self) -> str:
        return "Builds the sorted array one item at a time by taking each element and inserting it into its correct position among the previously sorted elements."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n²)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def is_stable(self) -> bool:
        return True
    
    @property
    def source_code(self) -> list:
        return [
            "def insertion_sort(arr):",
            "    for i in range(1, len(arr)):",
            "        key = arr[i]",
            "        j = i - 1",
            "        while j >= 0 and arr[j] > key:",
            "            arr[j + 1] = arr[j]",
            "            j -= 1",
            "        arr[j + 1] = key",
            "    return arr"
        ]
    
    def _sort(self, arr, trace, **kwargs):
        n = len(arr)
        sorted_indices = [0]  # First element is trivially sorted
        
        for i in range(1, n):
            key = arr[i]
            j = i - 1
            
            trace.add_step(
                operation='KEY_SELECT',
                array_state=arr,
                active_indices=[i],
                sorted_indices=list(sorted_indices),
                explanation=f"Select key = {key} at index {i}. Will insert into the sorted portion [0..{i-1}].",
                code_line=3,
                code_highlight=f"key = arr[{i}]  # key = {key}",
                variables={'i': i, 'key': key, 'j': j},
                pointers={'key_position': i, 'sorted_end': i - 1}
            )
            
            shifted = False
            while j >= 0 and arr[j] > key:
                trace.increment_comparisons()
                
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[j, j + 1],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': j, 'right_index': None,
                        'left_value': arr[j], 'right_value': key,
                        'result': True
                    },
                    explanation=f"{arr[j]} > {key}, so shift {arr[j]} one position to the right.",
                    code_line=5,
                    code_highlight=f"while j >= 0 and arr[{j}] > key:  # {arr[j]} > {key}",
                    variables={'i': i, 'key': key, 'j': j},
                    pointers={'comparing': j, 'insert_gap': j + 1}
                )
                
                trace.increment_shifts()
                arr[j + 1] = arr[j]
                shifted = True
                
                trace.add_step(
                    operation='SHIFT',
                    array_state=arr,
                    active_indices=[j, j + 1],
                    sorted_indices=list(sorted_indices),
                    explanation=f"Shift {arr[j]} from index {j} to index {j + 1}.",
                    code_line=6,
                    code_highlight=f"arr[{j+1}] = arr[{j}]",
                    variables={'i': i, 'key': key, 'j': j},
                    pointers={'shift_from': j, 'shift_to': j + 1}
                )
                
                j -= 1
            
            if j >= 0:
                trace.increment_comparisons()
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[j],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': j, 'right_index': None,
                        'left_value': arr[j], 'right_value': key,
                        'result': False
                    },
                    explanation=f"{arr[j]} ≤ {key}. Found the insertion position.",
                    code_line=5,
                    code_highlight=f"# arr[{j}] = {arr[j]} ≤ key = {key} → stop",
                    variables={'i': i, 'key': key, 'j': j}
                )
            
            arr[j + 1] = key
            
            trace.add_step(
                operation='INSERT',
                array_state=arr,
                active_indices=[j + 1],
                sorted_indices=list(sorted_indices) + [i] if not shifted else list(sorted_indices),
                explanation=f"Insert key {key} at index {j + 1}.",
                code_line=8,
                code_highlight=f"arr[{j+1}] = key  # Place {key} at index {j+1}",
                variables={'i': i, 'key': key, 'j': j, 'insert_at': j + 1},
                pointers={'inserted_at': j + 1}
            )
            
            sorted_indices = list(range(i + 1))
        
        return arr


class MergeSort(SortingAlgorithm):
    """Merge Sort — divide and conquer with merging."""
    
    @property
    def name(self) -> str:
        return "Merge Sort"
    
    @property
    def description(self) -> str:
        return "Divide and conquer algorithm that recursively halves the array into singular sub-arrays, then merges ordered halves into auxiliary memory. Guarantees O(n log n) in all cases."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(n)"
    
    @property
    def is_stable(self) -> bool:
        return True
    
    @property
    def is_in_place(self) -> bool:
        return False
    
    @property
    def source_code(self) -> list:
        return [
            "def merge_sort(arr, low, high):",
            "    if low < high:",
            "        mid = (low + high) // 2",
            "        merge_sort(arr, low, mid)",
            "        merge_sort(arr, mid + 1, high)",
            "        merge(arr, low, mid, high)",
            "",
            "def merge(arr, low, mid, high):",
            "    left = arr[low:mid+1]",
            "    right = arr[mid+1:high+1]",
            "    i = j = 0",
            "    k = low",
            "    while i < len(left) and j < len(right):",
            "        if left[i] <= right[j]:",
            "            arr[k] = left[i]",
            "            i += 1",
            "        else:",
            "            arr[k] = right[j]",
            "            j += 1",
            "        k += 1",
            "    while i < len(left):",
            "        arr[k] = left[i]",
            "        i += 1; k += 1",
            "    while j < len(right):",
            "        arr[k] = right[j]",
            "        j += 1; k += 1"
        ]
    
    def _sort(self, arr, trace, **kwargs):
        self._merge_sort(arr, 0, len(arr) - 1, trace, sorted_indices=[])
        return arr
    
    def _merge_sort(self, arr, low, high, trace, sorted_indices):
        if low >= high:
            return
        
        mid = (low + high) // 2
        
        trace.push_recursion({
            'call': f"mergeSort({low}, {high})",
            'low': low, 'high': high, 'mid': mid,
            'depth': trace.current_recursion_depth,
            'status': 'ACTIVE'
        })
        
        trace.add_step(
            operation='DIVIDE',
            array_state=arr,
            active_indices=list(range(low, high + 1)),
            sorted_indices=list(sorted_indices),
            explanation=f"Divide array[{low}..{high}] at midpoint {mid}. Left: [{low}..{mid}], Right: [{mid+1}..{high}].",
            code_line=3,
            code_highlight=f"mid = ({low} + {high}) // 2  # mid = {mid}",
            variables={'low': low, 'high': high, 'mid': mid},
            partition_range={'low': low, 'high': high},
            recursion_state={
                'depth': trace.current_recursion_depth,
                'call': f"mergeSort({low}, {high})",
                'left_call': f"mergeSort({low}, {mid})",
                'right_call': f"mergeSort({mid+1}, {high})"
            },
            subarrays={
                'left': arr[low:mid+1],
                'right': arr[mid+1:high+1]
            }
        )
        
        # Recurse left
        self._merge_sort(arr, low, mid, trace, sorted_indices)
        # Recurse right
        self._merge_sort(arr, mid + 1, high, trace, sorted_indices)
        # Merge
        self._merge(arr, low, mid, high, trace, sorted_indices)
        
        trace.pop_recursion()
    
    def _merge(self, arr, low, mid, high, trace, sorted_indices):
        left = arr[low:mid+1]
        right = arr[mid+1:high+1]
        
        trace.add_step(
            operation='MERGE_START',
            array_state=arr,
            active_indices=list(range(low, high + 1)),
            sorted_indices=list(sorted_indices),
            explanation=f"Merge sorted subarrays [{low}..{mid}] = {left} and [{mid+1}..{high}] = {right}.",
            code_line=8,
            code_highlight=f"merge(arr, {low}, {mid}, {high})",
            variables={'low': low, 'mid': mid, 'high': high},
            subarrays={'left': left, 'right': right},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"merge({low}, {mid}, {high})"}
        )
        
        i = j = 0
        k = low
        
        while i < len(left) and j < len(right):
            trace.increment_comparisons()
            comp_result = left[i] <= right[j]
            
            if comp_result:
                trace.add_step(
                    operation='MERGE_COMPARE',
                    array_state=arr,
                    active_indices=[k],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': low + i, 'right_index': mid + 1 + j,
                        'left_value': left[i], 'right_value': right[j],
                        'result': True
                    },
                    explanation=f"Compare left[{i}]={left[i]} ≤ right[{j}]={right[j]}. Place {left[i]} at position {k}.",
                    code_line=14,
                    code_highlight=f"if left[{i}] <= right[{j}]:  # {left[i]} <= {right[j]}",
                    variables={'i': i, 'j': j, 'k': k},
                    subarrays={'left': left, 'right': right, 'left_idx': i, 'right_idx': j},
                    pointers={'merge_write': k}
                )
                arr[k] = left[i]
                i += 1
            else:
                trace.add_step(
                    operation='MERGE_COMPARE',
                    array_state=arr,
                    active_indices=[k],
                    sorted_indices=list(sorted_indices),
                    comparison={
                        'left_index': low + i, 'right_index': mid + 1 + j,
                        'left_value': left[i], 'right_value': right[j],
                        'result': False
                    },
                    explanation=f"Compare left[{i}]={left[i]} > right[{j}]={right[j]}. Place {right[j]} at position {k}.",
                    code_line=18,
                    code_highlight=f"arr[{k}] = right[{j}]  # Place {right[j]}",
                    variables={'i': i, 'j': j, 'k': k},
                    subarrays={'left': left, 'right': right, 'left_idx': i, 'right_idx': j},
                    pointers={'merge_write': k}
                )
                arr[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            arr[k] = left[i]
            trace.add_step(
                operation='MERGE_COPY',
                array_state=arr,
                active_indices=[k],
                sorted_indices=list(sorted_indices),
                explanation=f"Copy remaining left[{i}]={left[i]} to position {k}.",
                code_line=22,
                code_highlight=f"arr[{k}] = left[{i}]",
                variables={'i': i, 'k': k},
                pointers={'merge_write': k}
            )
            i += 1
            k += 1
        
        while j < len(right):
            arr[k] = right[j]
            trace.add_step(
                operation='MERGE_COPY',
                array_state=arr,
                active_indices=[k],
                sorted_indices=list(sorted_indices),
                explanation=f"Copy remaining right[{j}]={right[j]} to position {k}.",
                code_line=25,
                code_highlight=f"arr[{k}] = right[{j}]",
                variables={'j': j, 'k': k},
                pointers={'merge_write': k}
            )
            j += 1
            k += 1
        
        trace.add_step(
            operation='MERGE_COMPLETE',
            array_state=arr,
            active_indices=list(range(low, high + 1)),
            sorted_indices=list(sorted_indices),
            explanation=f"Merge complete for [{low}..{high}]. Result: {arr[low:high+1]}.",
            code_line=8,
            code_highlight=f"# Merged: {arr[low:high+1]}",
            subarrays={'merged': arr[low:high+1]},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"merge({low}, {mid}, {high})"}
        )


class QuickSort(SortingAlgorithm):
    """Quick Sort — FLAGSHIP algorithm with the most detailed trace.
    
    Supports both Hoare and Lomuto partition schemes.
    Default: Hoare partition (dual pointer).
    """
    
    @property
    def name(self) -> str:
        return "Quick Sort"
    
    @property
    def description(self) -> str:
        return "Partition-exchange sort utilizing pivot element invariant resolution. Recursively decomposes unsorted slices into left and right sub-arrays bounding the selected pivot."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n²)"
    
    @property
    def space_complexity(self) -> str:
        return "O(log n)"
    
    @property
    def source_code(self) -> list:
        return [
            "def quick_sort(arr, low, high):",
            "    if low < high:",
            "        pi = partition(arr, low, high)",
            "        quick_sort(arr, low, pi)",
            "        quick_sort(arr, pi + 1, high)",
            "",
            "def partition(arr, low, high):",
            "    pivot = arr[low]",
            "    i = low - 1",
            "    j = high + 1",
            "    while True:",
            "        i += 1",
            "        while arr[i] < pivot: i += 1",
            "        j -= 1",
            "        while arr[j] > pivot: j -= 1",
            "        if i >= j: return j",
            "        arr[i], arr[j] = arr[j], arr[i]  # Swap",
        ]
    
    def _sort(self, arr, trace, **kwargs):
        scheme = kwargs.get('partition_scheme', 'hoare')
        self._sorted_indices = []
        if scheme == 'lomuto':
            self._quick_sort_lomuto(arr, 0, len(arr) - 1, trace)
        else:
            self._quick_sort_hoare(arr, 0, len(arr) - 1, trace)
        return arr
    
    # ─── HOARE PARTITION (Default / Flagship) ──────────────────────
    
    def _quick_sort_hoare(self, arr, low, high, trace):
        if low >= high:
            if low == high:
                self._sorted_indices.append(low)
            return
        
        trace.push_recursion({
            'call': f"quickSort({low}, {high})",
            'low': low, 'high': high,
            'depth': trace.current_recursion_depth,
            'status': 'ACTIVE'
        })
        
        trace.add_step(
            operation='RECURSIVE_CALL',
            array_state=arr,
            active_indices=list(range(low, high + 1)),
            sorted_indices=list(self._sorted_indices),
            explanation=f"Recursive call: quickSort({low}, {high}). Subarray has {high - low + 1} elements.",
            code_line=1,
            code_highlight=f"quick_sort(arr, {low}, {high})",
            variables={'low': low, 'high': high, 'size': high - low + 1},
            partition_range={'low': low, 'high': high},
            recursion_state={
                'depth': trace.current_recursion_depth,
                'call': f"quickSort({low}, {high})"
            }
        )
        
        pi = self._hoare_partition(arr, low, high, trace)
        
        trace.add_step(
            operation='PARTITION_DONE',
            array_state=arr,
            active_indices=[pi],
            sorted_indices=list(self._sorted_indices),
            explanation=f"Partition complete. Pivot boundary at index {pi}. Left partition: [{low}..{pi}], Right partition: [{pi+1}..{high}].",
            code_line=3,
            code_highlight=f"pi = partition(arr, {low}, {high})  # pi = {pi}",
            variables={'low': low, 'high': high, 'pi': pi},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"quickSort({low}, {high})"}
        )
        
        # Recurse left
        self._quick_sort_hoare(arr, low, pi, trace)
        # Recurse right
        self._quick_sort_hoare(arr, pi + 1, high, trace)
        
        trace.pop_recursion()
    
    def _hoare_partition(self, arr, low, high, trace):
        pivot_value = arr[low]
        pivot_index = low
        i = low - 1
        j = high + 1
        
        trace.add_step(
            operation='PIVOT_SELECT',
            array_state=arr,
            active_indices=[pivot_index],
            sorted_indices=list(self._sorted_indices),
            pivot={'value': pivot_value, 'index': pivot_index},
            explanation=f"Pivot selected: {pivot_value} (first element at index {pivot_index}). Initialize i = {i}, j = {j}.",
            code_line=8,
            code_highlight=f"pivot = arr[{low}]  # pivot = {pivot_value}",
            variables={'low': low, 'high': high, 'pivot': pivot_value},
            pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
        )
        
        while True:
            # Advance left pointer
            i += 1
            while arr[i] < pivot_value:
                trace.increment_comparisons()
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[i],
                    sorted_indices=list(self._sorted_indices),
                    pivot={'value': pivot_value, 'index': pivot_index},
                    comparison={
                        'left_index': i, 'right_index': pivot_index,
                        'left_value': arr[i], 'right_value': pivot_value,
                        'result': True
                    },
                    explanation=f"{arr[i]} < pivot {pivot_value}, so the left pointer advances past index {i}.",
                    code_line=13,
                    code_highlight=f"while arr[{i}] < pivot:  # {arr[i]} < {pivot_value} → advance",
                    variables={'low': low, 'high': high, 'pivot': pivot_value},
                    pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                    partition_range={'low': low, 'high': high},
                    recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
                )
                i += 1
            
            trace.increment_comparisons()
            trace.add_step(
                operation='POINTER_STOP',
                array_state=arr,
                active_indices=[i],
                sorted_indices=list(self._sorted_indices),
                pivot={'value': pivot_value, 'index': pivot_index},
                comparison={
                    'left_index': i, 'right_index': pivot_index,
                    'left_value': arr[i], 'right_value': pivot_value,
                    'result': False
                },
                explanation=f"Left pointer stops at index {i} (value {arr[i]}). {arr[i]} ≥ pivot {pivot_value}.",
                code_line=13,
                code_highlight=f"# arr[{i}] = {arr[i]} ≥ pivot → left stops",
                variables={'low': low, 'high': high, 'pivot': pivot_value},
                pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                partition_range={'low': low, 'high': high},
                recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
            )
            
            # Advance right pointer
            j -= 1
            while arr[j] > pivot_value:
                trace.increment_comparisons()
                trace.add_step(
                    operation='COMPARISON',
                    array_state=arr,
                    active_indices=[j],
                    sorted_indices=list(self._sorted_indices),
                    pivot={'value': pivot_value, 'index': pivot_index},
                    comparison={
                        'left_index': j, 'right_index': pivot_index,
                        'left_value': arr[j], 'right_value': pivot_value,
                        'result': True
                    },
                    explanation=f"{arr[j]} > pivot {pivot_value}, so the right pointer advances past index {j}.",
                    code_line=15,
                    code_highlight=f"while arr[{j}] > pivot:  # {arr[j]} > {pivot_value} → advance",
                    variables={'low': low, 'high': high, 'pivot': pivot_value},
                    pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                    partition_range={'low': low, 'high': high},
                    recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
                )
                j -= 1
            
            trace.increment_comparisons()
            trace.add_step(
                operation='POINTER_STOP',
                array_state=arr,
                active_indices=[j],
                sorted_indices=list(self._sorted_indices),
                pivot={'value': pivot_value, 'index': pivot_index},
                comparison={
                    'left_index': j, 'right_index': pivot_index,
                    'left_value': arr[j], 'right_value': pivot_value,
                    'result': False
                },
                explanation=f"Right pointer stops at index {j} (value {arr[j]}). {arr[j]} ≤ pivot {pivot_value}.",
                code_line=15,
                code_highlight=f"# arr[{j}] = {arr[j]} ≤ pivot → right stops",
                variables={'low': low, 'high': high, 'pivot': pivot_value},
                pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                partition_range={'low': low, 'high': high},
                recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
            )
            
            # Check if pointers crossed
            if i >= j:
                trace.add_step(
                    operation='POINTERS_CROSSED',
                    array_state=arr,
                    active_indices=[j],
                    sorted_indices=list(self._sorted_indices),
                    pivot={'value': pivot_value, 'index': pivot_index},
                    explanation=f"Pointers crossed (i={i} ≥ j={j}). Partition boundary is at index {j}. All elements left of {j} are ≤ {pivot_value}, all right are ≥ {pivot_value}.",
                    code_line=16,
                    code_highlight=f"if i >= j: return j  # i={i} >= j={j} → return {j}",
                    variables={'low': low, 'high': high, 'pivot': pivot_value, 'i': i, 'j': j},
                    pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                    partition_range={'low': low, 'high': high},
                    recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
                )
                return j
            
            # Swap
            trace.increment_swaps()
            val_i, val_j = arr[i], arr[j]
            arr[i], arr[j] = arr[j], arr[i]
            
            trace.add_step(
                operation='SWAP',
                array_state=arr,
                active_indices=[i, j],
                sorted_indices=list(self._sorted_indices),
                pivot={'value': pivot_value, 'index': pivot_index},
                swap={
                    'index_a': i, 'index_b': j,
                    'value_a': val_i, 'value_b': val_j
                },
                explanation=f"Swap {val_i} (index {i}) and {val_j} (index {j}). These elements are on opposite, incorrect sides of the pivot and are exchanged to restore invariant boundaries.",
                code_line=17,
                code_highlight=f"arr[{i}], arr[{j}] = arr[{j}], arr[{i}]  # Swap {val_i} ↔ {val_j}",
                variables={'low': low, 'high': high, 'pivot': pivot_value, 'i': i, 'j': j},
                pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                partition_range={'low': low, 'high': high},
                recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
            )
    
    # ─── LOMUTO PARTITION ──────────────────────────────────────────
    
    def _quick_sort_lomuto(self, arr, low, high, trace):
        if low >= high:
            if low == high:
                self._sorted_indices.append(low)
            return
        
        trace.push_recursion({
            'call': f"quickSort({low}, {high})",
            'low': low, 'high': high,
            'depth': trace.current_recursion_depth,
            'status': 'ACTIVE'
        })
        
        trace.add_step(
            operation='RECURSIVE_CALL',
            array_state=arr,
            active_indices=list(range(low, high + 1)),
            sorted_indices=list(self._sorted_indices),
            explanation=f"Recursive call: quickSort({low}, {high}).",
            code_line=1,
            code_highlight=f"quick_sort(arr, {low}, {high})",
            variables={'low': low, 'high': high},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"quickSort({low}, {high})"}
        )
        
        pi = self._lomuto_partition(arr, low, high, trace)
        
        self._sorted_indices.append(pi)
        
        trace.add_step(
            operation='PARTITION_DONE',
            array_state=arr,
            active_indices=[pi],
            sorted_indices=list(self._sorted_indices),
            explanation=f"Pivot {arr[pi]} is now at its final sorted position (index {pi}).",
            code_line=3,
            code_highlight=f"pi = partition(arr, {low}, {high})  # pi = {pi}",
            variables={'low': low, 'high': high, 'pi': pi},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"quickSort({low}, {high})"}
        )
        
        self._quick_sort_lomuto(arr, low, pi - 1, trace)
        self._quick_sort_lomuto(arr, pi + 1, high, trace)
        
        trace.pop_recursion()
    
    def _lomuto_partition(self, arr, low, high, trace):
        pivot_value = arr[high]
        pivot_index = high
        i = low - 1
        
        trace.add_step(
            operation='PIVOT_SELECT',
            array_state=arr,
            active_indices=[pivot_index],
            sorted_indices=list(self._sorted_indices),
            pivot={'value': pivot_value, 'index': pivot_index},
            explanation=f"Lomuto: Pivot selected: {pivot_value} (last element at index {pivot_index}). i = {i}.",
            code_line=8,
            code_highlight=f"pivot = arr[{high}]  # pivot = {pivot_value}",
            variables={'low': low, 'high': high, 'pivot': pivot_value, 'i': i},
            pointers={'i': i, 'pivot_index': pivot_index},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
        )
        
        for j in range(low, high):
            trace.increment_comparisons()
            comp_result = arr[j] <= pivot_value
            
            trace.add_step(
                operation='COMPARISON',
                array_state=arr,
                active_indices=[j, pivot_index],
                sorted_indices=list(self._sorted_indices),
                pivot={'value': pivot_value, 'index': pivot_index},
                comparison={
                    'left_index': j, 'right_index': pivot_index,
                    'left_value': arr[j], 'right_value': pivot_value,
                    'result': comp_result
                },
                explanation=f"Compare {arr[j]} (index {j}) with pivot {pivot_value}. "
                           f"{'Less or equal — move to left partition.' if comp_result else 'Greater — stays in right partition.'}",
                code_line=13,
                code_highlight=f"if arr[{j}] <= pivot:  # {arr[j]} {'<=' if comp_result else '>'} {pivot_value}",
                variables={'low': low, 'high': high, 'pivot': pivot_value, 'i': i, 'j': j},
                pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                partition_range={'low': low, 'high': high},
                recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
            )
            
            if comp_result:
                i += 1
                if i != j:
                    trace.increment_swaps()
                    val_i, val_j = arr[i], arr[j]
                    arr[i], arr[j] = arr[j], arr[i]
                    
                    trace.add_step(
                        operation='SWAP',
                        array_state=arr,
                        active_indices=[i, j],
                        sorted_indices=list(self._sorted_indices),
                        pivot={'value': pivot_value, 'index': pivot_index},
                        swap={
                            'index_a': i, 'index_b': j,
                            'value_a': val_i, 'value_b': val_j
                        },
                        explanation=f"Swap {val_i} (index {i}) and {val_j} (index {j}) to maintain partition invariant.",
                        code_line=17,
                        code_highlight=f"arr[{i}], arr[{j}] = arr[{j}], arr[{i}]",
                        variables={'low': low, 'high': high, 'pivot': pivot_value, 'i': i, 'j': j},
                        pointers={'i': i, 'j': j, 'pivot_index': pivot_index},
                        partition_range={'low': low, 'high': high},
                        recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
                    )
        
        # Place pivot in final position
        trace.increment_swaps()
        val_i1, val_p = arr[i + 1], arr[high]
        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        
        trace.add_step(
            operation='PIVOT_PLACE',
            array_state=arr,
            active_indices=[i + 1, high],
            sorted_indices=list(self._sorted_indices),
            pivot={'value': pivot_value, 'index': i + 1},
            swap={
                'index_a': i + 1, 'index_b': high,
                'value_a': val_i1, 'value_b': val_p
            },
            explanation=f"Place pivot {pivot_value} at its final position (index {i + 1}).",
            code_line=17,
            code_highlight=f"arr[{i+1}], arr[{high}] = arr[{high}], arr[{i+1}]",
            variables={'low': low, 'high': high, 'pivot': pivot_value, 'final_pos': i + 1},
            pointers={'pivot_final': i + 1},
            partition_range={'low': low, 'high': high},
            recursion_state={'depth': trace.current_recursion_depth, 'call': f"partition({low}, {high})"}
        )
        
        return i + 1


class HeapSort(SortingAlgorithm):
    """Heap Sort — uses a binary heap data structure."""
    
    @property
    def name(self) -> str:
        return "Heap Sort"
    
    @property
    def description(self) -> str:
        return "Builds a max-heap from the array, then repeatedly extracts the maximum element and places it at the end. Uses the heap property to efficiently find the maximum."
    
    @property
    def time_complexity_best(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_average(self) -> str:
        return "O(n log n)"
    
    @property
    def time_complexity_worst(self) -> str:
        return "O(n log n)"
    
    @property
    def space_complexity(self) -> str:
        return "O(1)"
    
    @property
    def source_code(self) -> list:
        return [
            "def heap_sort(arr):",
            "    n = len(arr)",
            "    # Build max heap",
            "    for i in range(n // 2 - 1, -1, -1):",
            "        heapify(arr, n, i)",
            "    # Extract elements",
            "    for i in range(n - 1, 0, -1):",
            "        arr[0], arr[i] = arr[i], arr[0]",
            "        heapify(arr, i, 0)",
            "",
            "def heapify(arr, n, i):",
            "    largest = i",
            "    left = 2 * i + 1",
            "    right = 2 * i + 2",
            "    if left < n and arr[left] > arr[largest]:",
            "        largest = left",
            "    if right < n and arr[right] > arr[largest]:",
            "        largest = right",
            "    if largest != i:",
            "        arr[i], arr[largest] = arr[largest], arr[i]",
            "        heapify(arr, n, largest)"
        ]
    
    def _sort(self, arr, trace, **kwargs):
        n = len(arr)
        sorted_indices = []
        
        # Build max heap
        trace.add_step(
            operation='BUILD_HEAP',
            array_state=arr,
            explanation=f"Building max-heap from {n} elements.",
            code_line=4,
            code_highlight="for i in range(n // 2 - 1, -1, -1):",
            variables={'n': n}
        )
        
        for i in range(n // 2 - 1, -1, -1):
            self._heapify(arr, n, i, trace, sorted_indices, phase='build')
        
        trace.add_step(
            operation='HEAP_BUILT',
            array_state=arr,
            explanation=f"Max-heap built. Maximum element is {arr[0]} at root (index 0).",
            code_line=5,
            code_highlight="# Max heap built",
            variables={'n': n, 'max': arr[0]}
        )
        
        # Extract elements
        for i in range(n - 1, 0, -1):
            # Swap root with last unsorted element
            trace.increment_swaps()
            val_0, val_i = arr[0], arr[i]
            arr[0], arr[i] = arr[i], arr[0]
            sorted_indices.append(i)
            
            trace.add_step(
                operation='EXTRACT_MAX',
                array_state=arr,
                active_indices=[0, i],
                sorted_indices=list(sorted_indices),
                swap={'index_a': 0, 'index_b': i, 'value_a': val_0, 'value_b': val_i},
                explanation=f"Extract max {val_0}: swap with {val_i} at index {i}. {val_0} is now in final position.",
                code_line=8,
                code_highlight=f"arr[0], arr[{i}] = arr[{i}], arr[0]",
                variables={'heap_size': i, 'extracted': val_0}
            )
            
            self._heapify(arr, i, 0, trace, sorted_indices, phase='extract')
        
        sorted_indices.append(0)
        return arr
    
    def _heapify(self, arr, n, i, trace, sorted_indices, phase='build'):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2
        
        if left < n:
            trace.increment_comparisons()
            if arr[left] > arr[largest]:
                largest = left
        
        if right < n:
            trace.increment_comparisons()
            if arr[right] > arr[largest]:
                largest = right
        
        if largest != i:
            trace.increment_swaps()
            val_i, val_l = arr[i], arr[largest]
            arr[i], arr[largest] = arr[largest], arr[i]
            
            child_type = "left" if largest == left else "right"
            trace.add_step(
                operation='HEAPIFY',
                array_state=arr,
                active_indices=[i, largest],
                sorted_indices=list(sorted_indices),
                swap={'index_a': i, 'index_b': largest, 'value_a': val_i, 'value_b': val_l},
                explanation=f"Heapify: {child_type} child {val_l} (index {largest}) > parent {val_i} (index {i}). Swap to maintain heap property.",
                code_line=20,
                code_highlight=f"arr[{i}], arr[{largest}] = arr[{largest}], arr[{i}]",
                variables={
                    'i': i, 'largest': largest,
                    'parent': val_i, 'child': val_l,
                    'left': left if left < n else None,
                    'right': right if right < n else None
                },
                pointers={'parent': i, 'largest': largest}
            )
            
            self._heapify(arr, n, largest, trace, sorted_indices, phase)
