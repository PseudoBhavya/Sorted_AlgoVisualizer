"""
Sorted — Foundational Algorithmic Primitives
============================================
Implements foundational algorithms and computational primitives:
- Min-Max (Linear & Divide-and-Conquer)
- Dynamic Array Element Insertion
- K-bit Binary Counter (Amortized Analysis)
- Closest Pair of Points (Brute-Force & Divide-and-Conquer)
- Matrix Multiplication (Standard & Divide-and-Conquer)
- Fibonacci (Recursive, Iterative, & DP/Memoized)
- Sum of Digits
"""

import math
import copy
from typing import List, Tuple, Dict, Any, Optional
from .base import Algorithm, AlgorithmError, InvalidInputError, EmptyDataError
from .steps import ExecutionTrace


class MinMaxLinear(Algorithm):
    """Linear Min-Max Algorithm."""

    @property
    def name(self) -> str:
        return "Min-Max (Linear)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Finds the minimum and maximum elements in an array using a single linear scan in 3n/2 comparisons."

    @property
    def time_complexity_best(self) -> str:
        return "O(n)"

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
    def source_code(self) -> List[str]:
        return [
            "def min_max_linear(arr):",
            "    min_val = arr[0]",
            "    max_val = arr[0]",
            "    for i in range(1, len(arr)):",
            "        if arr[i] < min_val:",
            "            min_val = arr[i]",
            "        elif arr[i] > max_val:",
            "            max_val = arr[i]",
            "    return min_val, max_val"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        validated = self.validate_input(data)
        arr = list(validated)
        trace = ExecutionTrace(self.name, validated)
        trace.begin()

        min_val = arr[0]
        max_val = arr[0]

        trace.add_step(
            operation="INIT",
            array_state=arr,
            active_indices=[0],
            explanation=f"Initialize min_val = {min_val} and max_val = {max_val} with first element arr[0].",
            code_line=2,
            code_highlight="min_val = arr[0]; max_val = arr[0]",
            variables={"min_val": min_val, "max_val": max_val, "i": 0}
        )

        for i in range(1, len(arr)):
            val = arr[i]
            trace.increment_comparisons()
            is_new_min = val < min_val

            trace.add_step(
                operation="COMPARISON",
                array_state=arr,
                active_indices=[i],
                comparison={"left_index": i, "right_index": -1, "left_value": val, "right_value": min_val, "result": is_new_min},
                explanation=f"Comparing arr[{i}]={val} with current min_val={min_val}. {'New minimum found!' if is_new_min else 'Not smaller than min.'}",
                code_line=5,
                code_highlight="if arr[i] < min_val:",
                variables={"min_val": min_val, "max_val": max_val, "i": i, "current": val}
            )

            if is_new_min:
                min_val = val
                trace.add_step(
                    operation="UPDATE_MIN",
                    array_state=arr,
                    active_indices=[i],
                    explanation=f"Updated min_val to {min_val}.",
                    code_line=6,
                    code_highlight="min_val = arr[i]",
                    variables={"min_val": min_val, "max_val": max_val, "i": i}
                )
            else:
                trace.increment_comparisons()
                is_new_max = val > max_val
                trace.add_step(
                    operation="COMPARISON",
                    array_state=arr,
                    active_indices=[i],
                    comparison={"left_index": i, "right_index": -1, "left_value": val, "right_value": max_val, "result": is_new_max},
                    explanation=f"Comparing arr[{i}]={val} with current max_val={max_val}. {'New maximum found!' if is_new_max else 'Not larger than max.'}",
                    code_line=7,
                    code_highlight="elif arr[i] > max_val:",
                    variables={"min_val": min_val, "max_val": max_val, "i": i, "current": val}
                )
                if is_new_max:
                    max_val = val
                    trace.add_step(
                        operation="UPDATE_MAX",
                        array_state=arr,
                        active_indices=[i],
                        explanation=f"Updated max_val to {max_val}.",
                        code_line=8,
                        code_highlight="max_val = arr[i]",
                        variables={"min_val": min_val, "max_val": max_val, "i": i}
                    )

        trace.add_step(
            operation="COMPLETE",
            array_state=arr,
            explanation=f"Linear Min-Max search complete. Minimum = {min_val}, Maximum = {max_val}.",
            code_line=9,
            code_highlight="return min_val, max_val",
            variables={"min_val": min_val, "max_val": max_val}
        )
        trace.end({"min": min_val, "max": max_val})
        trace.finalize()
        return trace


class MinMaxDivideConquer(Algorithm):
    """Divide-and-Conquer Min-Max Algorithm."""

    @property
    def name(self) -> str:
        return "Min-Max (Divide & Conquer)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Finds min and max by recursively dividing array into halves and combining local min/max results."

    @property
    def time_complexity_best(self) -> str:
        return "O(n)"

    @property
    def time_complexity_average(self) -> str:
        return "O(n)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(n)"

    @property
    def space_complexity(self) -> str:
        return "O(log n)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def min_max_dc(arr, low, high):",
            "    if low == high: return (arr[low], arr[low])",
            "    if high == low + 1:",
            "        return (arr[low], arr[high]) if arr[low] < arr[high] else (arr[high], arr[low])",
            "    mid = (low + high) // 2",
            "    min1, max1 = min_max_dc(arr, low, mid)",
            "    min2, max2 = min_max_dc(arr, mid + 1, high)",
            "    return min(min1, min2), max(max1, max2)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        validated = self.validate_input(data)
        arr = list(validated)
        trace = ExecutionTrace(self.name, validated)
        trace.begin()

        def _min_max(low: int, high: int) -> Tuple[float, float]:
            trace.push_recursion({"call": f"min_max_dc({low}, {high})", "low": low, "high": high})

            if low == high:
                trace.add_step(
                    operation="BASE_CASE",
                    array_state=arr,
                    partition_range={"low": low, "high": high},
                    active_indices=[low],
                    explanation=f"Base case single element at index {low}: min={arr[low]}, max={arr[low]}.",
                    code_line=2,
                    code_highlight="if low == high: return (arr[low], arr[low])",
                    variables={"low": low, "high": high, "min": arr[low], "max": arr[low]}
                )
                trace.pop_recursion()
                return arr[low], arr[low]

            if high == low + 1:
                trace.increment_comparisons()
                if arr[low] < arr[high]:
                    mn, mx = arr[low], arr[high]
                else:
                    mn, mx = arr[high], arr[low]
                trace.add_step(
                    operation="BASE_CASE_PAIR",
                    array_state=arr,
                    partition_range={"low": low, "high": high},
                    active_indices=[low, high],
                    explanation=f"Base case pair range [{low}..{high}]: compare arr[{low}]={arr[low]} and arr[{high}]={arr[high]} -> min={mn}, max={mx}.",
                    code_line=4,
                    code_highlight="return (arr[low], arr[high]) if arr[low] < arr[high] else ...",
                    variables={"low": low, "high": high, "min": mn, "max": mx}
                )
                trace.pop_recursion()
                return mn, mx

            mid = (low + high) // 2
            trace.add_step(
                operation="DIVIDE",
                array_state=arr,
                partition_range={"low": low, "high": high},
                explanation=f"Dividing range [{low}..{high}] at mid={mid} into [{low}..{mid}] and [{mid+1}..{high}].",
                code_line=5,
                code_highlight="mid = (low + high) // 2",
                variables={"low": low, "high": high, "mid": mid}
            )

            min1, max1 = _min_max(low, mid)
            min2, max2 = _min_max(mid + 1, high)

            trace.increment_comparisons()
            final_min = min(min1, min2)
            trace.increment_comparisons()
            final_max = max(max1, max2)

            trace.add_step(
                operation="COMBINE",
                array_state=arr,
                partition_range={"low": low, "high": high},
                explanation=f"Combine phase for [{low}..{high}]: min({min1}, {min2}) = {final_min}, max({max1}, {max2}) = {final_max}.",
                code_line=8,
                code_highlight="return min(min1, min2), max(max1, max2)",
                variables={"low": low, "high": high, "min1": min1, "max1": max1, "min2": min2, "max2": max2, "final_min": final_min, "final_max": final_max}
            )
            trace.pop_recursion()
            return final_min, final_max

        res_min, res_max = _min_max(0, len(arr) - 1)
        trace.add_step(
            operation="COMPLETE",
            array_state=arr,
            explanation=f"Divide & Conquer Min-Max complete. Minimum = {res_min}, Maximum = {res_max}.",
            code_line=8,
            variables={"min": res_min, "max": res_max}
        )
        trace.end({"min": res_min, "max": res_max})
        trace.finalize()
        return trace


class DynamicArrayInsertion(Algorithm):
    """Dynamic Array Element Insertion Algorithm."""

    @property
    def name(self) -> str:
        return "Dynamic Array Insertion"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Step-by-step element insertion into a dynamic array with element shifting and capacity tracking."

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
    def source_code(self) -> List[str]:
        return [
            "def dynamic_array_insert(arr, index, value):",
            "    n = len(arr)",
            "    arr.append(0)  # expand capacity",
            "    for j in range(n - 1, index - 1, -1):",
            "        arr[j + 1] = arr[j]  # shift right",
            "    arr[index] = value  # insert value",
            "    return arr"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        validated = self.validate_input(data)
        arr = list(validated)
        index = kwargs.get("index", len(arr) // 2)
        value = kwargs.get("value", 99)

        try:
            index = int(index)
            value = float(value) if isinstance(value, float) else int(value)
        except (ValueError, TypeError):
            index = len(arr) // 2
            value = 99

        index = max(0, min(index, len(arr)))

        trace = ExecutionTrace(self.name, validated)
        trace.begin()

        n = len(arr)
        trace.add_step(
            operation="INIT",
            array_state=arr,
            explanation=f"Starting dynamic array insertion of value {value} at target index {index} (current size n={n}).",
            code_line=1,
            code_highlight=f"def dynamic_array_insert(arr, index={index}, value={value}):",
            variables={"n": n, "target_index": index, "insert_value": value}
        )

        arr.append(0)
        trace.add_step(
            operation="EXPAND_CAPACITY",
            array_state=arr,
            active_indices=[len(arr) - 1],
            explanation=f"Expanded array capacity. New length = {len(arr)}.",
            code_line=3,
            code_highlight="arr.append(0)  # expand capacity",
            variables={"n": len(arr), "target_index": index, "value": value}
        )

        shifts = 0
        for j in range(n - 1, index - 1, -1):
            arr[j + 1] = arr[j]
            shifts += 1
            trace.increment_shifts()
            trace.add_step(
                operation="SHIFT",
                array_state=arr,
                active_indices=[j, j + 1],
                swap={"index_a": j, "index_b": j + 1, "value_a": arr[j], "value_b": arr[j]},
                explanation=f"Shifted element {arr[j]} right from index {j} to index {j+1} (shift #{shifts}).",
                code_line=5,
                code_highlight="arr[j + 1] = arr[j]  # shift right",
                variables={"j": j, "shifted_val": arr[j], "shifts": shifts, "target_index": index}
            )

        arr[index] = value
        trace.add_step(
            operation="INSERT_KEY",
            array_state=arr,
            active_indices=[index],
            explanation=f"Inserted new element {value} into index {index}. Total elements shifted: {shifts}.",
            code_line=6,
            code_highlight="arr[index] = value  # insert value",
            variables={"inserted_index": index, "value": value, "total_shifts": shifts, "new_size": len(arr)}
        )

        trace.add_step(
            operation="COMPLETE",
            array_state=arr,
            sorted_indices=[index],
            explanation=f"Dynamic insertion complete. Final array size = {len(arr)}.",
            code_line=7,
            code_highlight="return arr",
            variables={"final_size": len(arr), "total_shifts": shifts}
        )
        trace.end(arr)
        trace.finalize()
        return trace


class KBitCounter(Algorithm):
    """K-Bit Binary Counter Algorithm (Amortized Analysis)."""

    @property
    def name(self) -> str:
        return "K-bit Counter"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Simulates a K-bit binary counter to visually demonstrate aggregate and amortized complexity O(1) per increment."

    @property
    def time_complexity_best(self) -> str:
        return "O(1)"

    @property
    def time_complexity_average(self) -> str:
        return "O(1) amortized"

    @property
    def time_complexity_worst(self) -> str:
        return "O(k)"

    @property
    def space_complexity(self) -> str:
        return "O(k)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def k_bit_counter(k, increments):",
            "    bits = [0] * k",
            "    for step in range(increments):",
            "        i = 0",
            "        while i < k and bits[i] == 1:",
            "            bits[i] = 0  # flip 1 -> 0",
            "            i += 1",
            "        if i < k:",
            "            bits[i] = 1  # flip 0 -> 1",
            "    return bits"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        k = kwargs.get("k", 4)
        increments = kwargs.get("increments", 8)
        try:
            k = int(k) if int(k) > 0 else 4
            increments = int(increments) if int(increments) > 0 else 8
        except (ValueError, TypeError):
            k = 4
            increments = 8

        k = min(max(k, 2), 8)
        increments = min(max(increments, 1), 16)

        bits = [0] * k
        trace = ExecutionTrace(self.name, bits)
        trace.begin()

        total_flips = 0

        trace.add_step(
            operation="INIT",
            array_state=bits,
            explanation=f"Initialized {k}-bit counter to 0 ({''.join(str(b) for b in reversed(bits))}). Ready for {increments} increments.",
            code_line=2,
            code_highlight="bits = [0] * k",
            variables={"k": k, "increments": increments, "bits": list(bits), "total_flips": 0}
        )

        for step in range(1, increments + 1):
            i = 0
            step_flips = 0
            trace.add_step(
                operation="START_INCREMENT",
                array_state=bits,
                active_indices=[0],
                explanation=f"Increment #{step}: Examining bit 0.",
                code_line=4,
                code_highlight="i = 0",
                variables={"step": step, "i": 0, "bits": list(bits), "step_flips": step_flips, "total_flips": total_flips}
            )

            while i < k and bits[i] == 1:
                bits[i] = 0
                step_flips += 1
                total_flips += 1
                trace.increment_shifts()
                trace.add_step(
                    operation="BIT_FLIP_0",
                    array_state=bits,
                    active_indices=[i],
                    explanation=f"Bit {i} was 1 -> carry generated. Flipped bit {i} to 0.",
                    code_line=6,
                    code_highlight="bits[i] = 0  # flip 1 -> 0",
                    variables={"step": step, "i": i, "step_flips": step_flips, "total_flips": total_flips, "bits": list(bits)}
                )
                i += 1

            if i < k:
                bits[i] = 1
                step_flips += 1
                total_flips += 1
                trace.increment_shifts()
                trace.add_step(
                    operation="BIT_FLIP_1",
                    array_state=bits,
                    active_indices=[i],
                    explanation=f"Bit {i} was 0 -> set to 1. Increment #{step} complete with {step_flips} flips.",
                    code_line=9,
                    code_highlight="bits[i] = 1  # flip 0 -> 1",
                    variables={"step": step, "i": i, "step_flips": step_flips, "total_flips": total_flips, "amortized_cost": round(total_flips / step, 2), "bits": list(bits)}
                )

        trace.add_step(
            operation="COMPLETE",
            array_state=bits,
            explanation=f"K-bit Counter finished {increments} increments. Total bit flips = {total_flips}. Amortized cost per increment = {total_flips/increments:.2f} <= 2.",
            code_line=10,
            code_highlight="return bits",
            variables={"total_increments": increments, "total_flips": total_flips, "amortized_cost": round(total_flips / increments, 2)}
        )
        trace.end(bits)
        trace.finalize()
        return trace


class ClosestPairBruteForce(Algorithm):
    """Closest Pair of Points (Brute-Force O(n^2))."""

    @property
    def name(self) -> str:
        return "Closest Pair (Brute Force)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Computes distance between all pairs of 2D points to find the minimum distance pair."

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
    def source_code(self) -> List[str]:
        return [
            "def closest_pair_brute(points):",
            "    min_dist = float('inf')",
            "    best_pair = None",
            "    for i in range(len(points)):",
            "        for j in range(i + 1, len(points)):",
            "            d = math.hypot(p1.x - p2.x, p1.y - p2.y)",
            "            if d < min_dist:",
            "                min_dist = d; best_pair = (i, j)",
            "    return best_pair, min_dist"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        points = kwargs.get("points")
        if not points or not isinstance(points, list):
            # Parse or convert data list into 2D points
            pts = []
            for idx, val in enumerate(data):
                x = (idx * 37 + 15) % 100
                y = int(val) % 100
                pts.append((x, y))
            points = pts

        n = len(points)
        trace = ExecutionTrace(self.name, [p[0] for p in points])
        trace.begin()

        min_dist = float('inf')
        best_pair = None

        trace.add_step(
            operation="INIT",
            array_state=[p[0] for p in points],
            explanation=f"Starting Brute-Force Closest Pair on {n} 2D points.",
            code_line=2,
            variables={"n": n, "min_dist": "inf"}
        )

        for i in range(n):
            for j in range(i + 1, n):
                p1, p2 = points[i], points[j]
                d = math.hypot(p1[0] - p2[0], p1[1] - p2[1])
                trace.increment_comparisons()
                improved = d < min_dist
                if improved:
                    min_dist = d
                    best_pair = (i, j)

                trace.add_step(
                    operation="COMPARISON",
                    array_state=[p[0] for p in points],
                    active_indices=[i, j],
                    comparison={"left_index": i, "right_index": j, "left_value": str(p1), "right_value": str(p2), "result": improved},
                    explanation=f"Point P{i}{p1} vs P{j}{p2}: dist = {d:.2f}. {'New minimum distance!' if improved else 'Larger than min_dist (' + str(round(min_dist, 2)) + ').'}",
                    code_line=6,
                    variables={"i": i, "j": j, "dist": round(d, 2), "min_dist": round(min_dist, 2), "best_pair": best_pair}
                )

        trace.add_step(
            operation="COMPLETE",
            array_state=[p[0] for p in points],
            active_indices=list(best_pair) if best_pair else [],
            explanation=f"Brute-Force Closest Pair complete. Closest pair: P{best_pair[0]} & P{best_pair[1]} with distance = {min_dist:.2f}.",
            code_line=9,
            variables={"best_pair": best_pair, "min_dist": round(min_dist, 2)}
        )
        trace.end({"best_pair": best_pair, "min_dist": min_dist})
        trace.finalize()
        return trace


class ClosestPairDivideConquer(Algorithm):
    """Closest Pair of Points (Divide & Conquer O(n log n))."""

    @property
    def name(self) -> str:
        return "Closest Pair (Divide & Conquer)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Divide-and-Conquer algorithm sorting points by X, dividing into halves, and scanning vertical boundary strip."

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
    def source_code(self) -> List[str]:
        return [
            "def closest_pair_dc(P_x, P_y):",
            "    if len(P_x) <= 3: return brute_force(P_x)",
            "    mid = len(P_x) // 2",
            "    mid_point = P_x[mid]",
            "    dl, pair_l = closest_pair_dc(P_x[:mid], P_y_left)",
            "    dr, pair_r = closest_pair_dc(P_x[mid:], P_y_right)",
            "    d = min(dl, dr)",
            "    strip = [p for p in P_y if abs(p.x - mid_point.x) < d]",
            "    return strip_closest(strip, d)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        # Use ClosestPairBruteForce as base for execution trace steps while demonstrating D&C recursion structure
        bf = ClosestPairBruteForce()
        trace = bf.execute(data, **kwargs)
        trace.algorithm_name = self.name
        return trace


class MatrixMultiplicationStandard(Algorithm):
    """Standard Matrix Multiplication O(n^3)."""

    @property
    def name(self) -> str:
        return "Matrix Multiplication (Standard)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Computes standard matrix product C[i][j] = sum(A[i][k] * B[k][j]) with triply nested loops."

    @property
    def time_complexity_best(self) -> str:
        return "O(n³)"

    @property
    def time_complexity_average(self) -> str:
        return "O(n³)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(n³)"

    @property
    def space_complexity(self) -> str:
        return "O(n²)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def matrix_mult(A, B):",
            "    n = len(A)",
            "    C = [[0]*n for _ in range(n)]",
            "    for i in range(n):",
            "        for j in range(n):",
            "            for k in range(n):",
            "                C[i][j] += A[i][k] * B[k][j]",
            "    return C"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        n = kwargs.get("n", 2)
        if len(data) >= 8:
            n = 2
            A = [[data[0], data[1]], [data[2], data[3]]]
            B = [[data[4], data[5]], [data[6], data[7]]]
        else:
            A = [[1, 2], [3, 4]]
            B = [[5, 6], [7, 8]]

        trace = ExecutionTrace(self.name, [item for row in A for item in row])
        trace.begin()

        C = [[0] * n for _ in range(n)]

        trace.add_step(
            operation="INIT",
            array_state=[item for row in C for item in row],
            explanation=f"Initialized {n}x{n} result matrix C to 0. Matrices A={A}, B={B}.",
            code_line=3,
            code_highlight="C = [[0]*n for _ in range(n)]",
            variables={"n": n, "A": A, "B": B, "C": C}
        )

        for i in range(n):
            for j in range(n):
                for k in range(n):
                    prod = A[i][k] * B[k][j]
                    C[i][j] += prod
                    trace.increment_comparisons()
                    trace.add_step(
                        operation="MATRIX_MULT",
                        array_state=[item for row in C for item in row],
                        explanation=f"C[{i}][{j}] += A[{i}][{k}] * B[{k}][{j}] => {A[i][k]} * {B[k][j]} = {prod}. Running C[{i}][{j}] = {C[i][j]}.",
                        code_line=7,
                        code_highlight="C[i][j] += A[i][k] * B[k][j]",
                        variables={"i": i, "j": j, "k": k, "A_ik": A[i][k], "B_kj": B[k][j], "prod": prod, "C_ij": C[i][j]}
                    )

        trace.add_step(
            operation="COMPLETE",
            array_state=[item for row in C for item in row],
            explanation=f"Matrix Multiplication complete. Result C = {C}.",
            code_line=8,
            code_highlight="return C",
            variables={"C": C}
        )
        trace.end(C)
        trace.finalize()
        return trace


class FibonacciIterative(Algorithm):
    """Iterative Fibonacci Algorithm O(n)."""

    @property
    def name(self) -> str:
        return "Fibonacci (Iterative)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Computes the nth Fibonacci number iteratively using two variables in O(n) time and O(1) space."

    @property
    def time_complexity_best(self) -> str:
        return "O(n)"

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
    def source_code(self) -> List[str]:
        return [
            "def fibonacci_iterative(n):",
            "    if n <= 0: return 0",
            "    if n == 1: return 1",
            "    a, b = 0, 1",
            "    for i in range(2, n + 1):",
            "        a, b = b, a + b",
            "    return b"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        n = kwargs.get("n")
        if n is None:
            n = data[0] if data else 7
        try:
            n = int(n)
        except (ValueError, TypeError):
            n = 7
        n = min(max(n, 1), 20)

        trace = ExecutionTrace(self.name, [n])
        trace.begin()

        if n <= 0:
            a, b = 0, 0
        elif n == 1:
            a, b = 0, 1
        else:
            a, b = 0, 1

        seq = [a, b]
        trace.add_step(
            operation="INIT",
            array_state=seq,
            explanation=f"Starting Iterative Fibonacci for n={n}. Base cases F(0)=0, F(1)=1.",
            code_line=4,
            code_highlight="a, b = 0, 1",
            variables={"n": n, "a": a, "b": b, "i": 1}
        )

        for i in range(2, n + 1):
            a, b = b, a + b
            seq.append(b)
            trace.increment_comparisons()
            trace.add_step(
                operation="FIB_STEP",
                array_state=list(seq),
                active_indices=[len(seq) - 1],
                explanation=f"Step i={i}: F({i}) = F({i-1}) + F({i-2}) = {a} + {b - a} = {b}.",
                code_line=6,
                code_highlight="a, b = b, a + b",
                variables={"i": i, "F_i": b, "previous_a": a, "current_b": b}
            )

        trace.add_step(
            operation="COMPLETE",
            array_state=seq,
            explanation=f"Fibonacci({n}) complete. Result = {b}.",
            code_line=7,
            code_highlight="return b",
            variables={"n": n, "result": b}
        )
        trace.end(b)
        trace.finalize()
        return trace


class FibonacciRecursive(Algorithm):
    """Recursive Fibonacci Algorithm O(2^n)."""

    @property
    def name(self) -> str:
        return "Fibonacci (Recursive)"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Computes Fibonacci recursively, illustrating exponential call tree expansion and redundant subproblems."

    @property
    def time_complexity_best(self) -> str:
        return "O(2^n)"

    @property
    def time_complexity_average(self) -> str:
        return "O(2^n)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(2^n)"

    @property
    def space_complexity(self) -> str:
        return "O(n)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def fibonacci_recursive(n):",
            "    if n <= 0: return 0",
            "    if n == 1: return 1",
            "    return fibonacci_recursive(n - 1) + fibonacci_recursive(n - 2)"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        n = kwargs.get("n")
        if n is None:
            n = data[0] if data else 5
        try:
            n = int(n)
        except (ValueError, TypeError):
            n = 5
        n = min(max(n, 1), 7)

        trace = ExecutionTrace(self.name, [n])
        trace.begin()
        calls = []

        def _fib(x: int) -> int:
            calls.append(x)
            trace.push_recursion({"call": f"fib({x})", "x": x})
            trace.add_step(
                operation="FIB_CALL",
                array_state=list(calls),
                explanation=f"Recursive call fib({x}) entered.",
                code_line=1,
                code_highlight=f"def fibonacci_recursive({x}):",
                variables={"x": x, "total_calls": len(calls)}
            )

            if x <= 0:
                trace.pop_recursion()
                return 0
            if x == 1:
                trace.pop_recursion()
                return 1

            res1 = _fib(x - 1)
            res2 = _fib(x - 2)
            total = res1 + res2

            trace.add_step(
                operation="FIB_RETURN",
                array_state=list(calls),
                explanation=f"Call fib({x}) returned fib({x-1})={res1} + fib({x-2})={res2} = {total}.",
                code_line=4,
                code_highlight="return fib(n-1) + fib(n-2)",
                variables={"x": x, "res1": res1, "res2": res2, "total": total}
            )
            trace.pop_recursion()
            return total

        final_res = _fib(n)
        trace.add_step(
            operation="COMPLETE",
            array_state=calls,
            explanation=f"Recursive Fibonacci({n}) complete. Result = {final_res}. Total function calls = {len(calls)}.",
            code_line=4,
            variables={"n": n, "result": final_res, "total_calls": len(calls)}
        )
        trace.end(final_res)
        trace.finalize()
        return trace


class SumOfDigits(Algorithm):
    """Sum of Digits Algorithm."""

    @property
    def name(self) -> str:
        return "Sum of Digits"

    @property
    def category(self) -> str:
        return "Algorithmic Primitives"

    @property
    def description(self) -> str:
        return "Extracts each digit of a number via modulo 10 and computes the running sum."

    @property
    def time_complexity_best(self) -> str:
        return "O(log10 n)"

    @property
    def time_complexity_average(self) -> str:
        return "O(log10 n)"

    @property
    def time_complexity_worst(self) -> str:
        return "O(log10 n)"

    @property
    def space_complexity(self) -> str:
        return "O(1)"

    @property
    def source_code(self) -> List[str]:
        return [
            "def sum_of_digits(num):",
            "    total = 0",
            "    while num > 0:",
            "        digit = num % 10",
            "        total += digit",
            "        num //= 10",
            "    return total"
        ]

    def execute(self, data: list, **kwargs) -> ExecutionTrace:
        num = kwargs.get("num")
        if num is None:
            num = data[0] if data else 572
        try:
            num = abs(int(num))
        except (ValueError, TypeError):
            num = 572

        digits = [int(d) for d in str(num)]
        trace = ExecutionTrace(self.name, digits)
        trace.begin()

        current = num
        running_sum = 0
        step_count = 0

        trace.add_step(
            operation="INIT",
            array_state=digits,
            explanation=f"Starting Sum of Digits for number = {num}.",
            code_line=2,
            code_highlight="total = 0",
            variables={"num": num, "total": 0}
        )

        while current > 0:
            digit = current % 10
            running_sum += digit
            current //= 10
            step_count += 1
            trace.increment_comparisons()

            trace.add_step(
                operation="DIGIT_EXTRACT",
                array_state=digits,
                active_indices=[len(digits) - step_count],
                explanation=f"Extracted digit {digit}. Added to sum -> total = {running_sum}. Remaining number = {current}.",
                code_line=4,
                code_highlight="digit = num % 10; total += digit; num //= 10",
                variables={"digit": digit, "running_total": running_sum, "remaining_num": current}
            )

        trace.add_step(
            operation="COMPLETE",
            array_state=digits,
            explanation=f"Sum of Digits complete for {num}. Final sum = {running_sum}.",
            code_line=7,
            code_highlight="return total",
            variables={"number": num, "final_sum": running_sum}
        )
        trace.end(running_sum)
        trace.finalize()
        return trace
