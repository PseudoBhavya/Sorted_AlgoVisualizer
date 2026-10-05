"""
AlgoLens Benchmark Dataset Generator
====================================
Generates standard educational and benchmark datasets:
- Random Uniform
- Nearly Sorted (few inversions)
- Reversed / Descending (Worst Case for some sorts)
- Few Unique / Many Duplicates
- Gaussian / Normal Distribution
- Edge Cases (Empty, Single, Two, Already Sorted, All Identical)
"""

import random
from typing import List, Dict


class DatasetGenerator:
    """Provides standard and customizable benchmark datasets."""

    # Classic 12-element array matching the Stitch reference workspace
    DEFAULT_WORKSPACE_DATA = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 93, 8]
    
    PRESETS: Dict[str, List[int]] = {
        "Stitch Workspace Default": [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 93, 8],
        "Nearly Sorted (12 items)": [5, 10, 15, 20, 35, 30, 40, 45, 60, 55, 70, 80],
        "Reverse Sorted (12 items)": [95, 88, 76, 65, 54, 43, 38, 29, 21, 14, 9, 3],
        "Many Duplicates (12 items)": [12, 45, 12, 85, 45, 12, 85, 12, 45, 85, 12, 45],
        "Few Elements (5 items)": [42, 17, 93, 8, 55],
        "QuickSort Lomuto Worst Case (Sorted)": [10, 20, 30, 40, 50, 60, 70, 80, 90, 100],
        "Alternating Peaks": [10, 90, 15, 85, 20, 80, 25, 75, 30, 70, 35, 65]
    }

    @staticmethod
    def random(size: int = 12, min_val: int = 1, max_val: int = 100, seed: int = None) -> List[int]:
        """Generate random uniform integers."""
        if seed is not None:
            random.seed(seed)
        return [random.randint(min_val, max_val) for _ in range(size)]

    @staticmethod
    def nearly_sorted(size: int = 12, swap_count: int = 2, seed: int = None) -> List[int]:
        """Generate a sorted array with a small number of random swaps."""
        if seed is not None:
            random.seed(seed)
        arr = sorted([random.randint(1, 100) for _ in range(size)])
        for _ in range(min(swap_count, size // 2)):
            i = random.randint(0, size - 1)
            j = random.randint(0, size - 1)
            arr[i], arr[j] = arr[j], arr[i]
        return arr

    @staticmethod
    def reversed_sorted(size: int = 12, seed: int = None) -> List[int]:
        """Generate strictly descending array."""
        if seed is not None:
            random.seed(seed)
        arr = sorted([random.randint(1, 100) for _ in range(size)], reverse=True)
        return arr

    @staticmethod
    def few_unique(size: int = 12, unique_count: int = 3, seed: int = None) -> List[int]:
        """Generate array containing only a few unique values (many duplicates)."""
        if seed is not None:
            random.seed(seed)
        uniques = random.sample(range(5, 95), min(unique_count, size))
        return [random.choice(uniques) for _ in range(size)]

    @staticmethod
    def all_identical(size: int = 12, value: int = 42) -> List[int]:
        """Generate array where every element is identical."""
        return [value] * size

    @staticmethod
    def get_preset(name: str) -> List[int]:
        """Get pre-configured preset array by name."""
        if name in DatasetGenerator.PRESETS:
            return list(DatasetGenerator.PRESETS[name])
        return list(DatasetGenerator.DEFAULT_WORKSPACE_DATA)

    @classmethod
    def list_presets(cls) -> List[str]:
        """List all available preset names."""
        return list(cls.PRESETS.keys())
