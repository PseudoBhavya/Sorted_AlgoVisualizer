"""
AlgoLens Pandas Analytics Engine
================================
Statistical analysis, aggregation, and empirical benchmarking using Pandas.
Covers Syllabus Unit 4 on Pandas DataFrames, Series, Groupby, Aggregations, and Pivots.
"""

import time
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from algolens.algorithms.registry import AlgorithmRegistry
from algolens.data.datasets import DatasetGenerator


class PerformanceAnalytics:
    """Benchmarking and comparative analysis engine backed by Pandas."""

    @staticmethod
    def compare_on_dataset(
        algorithm_names: List[str],
        data: List[int],
        **kwargs
    ) -> pd.DataFrame:
        """Run multiple algorithms on the exact same input dataset and compile a Pandas DataFrame.
        
        Args:
            algorithm_names: List of algorithm names (e.g. ['Quick Sort', 'Merge Sort', 'Bubble Sort'])
            data: Input dataset array
            **kwargs: Extra arguments (e.g. partition_scheme='hoare')
            
        Returns:
            pd.DataFrame containing comparative metrics for each algorithm
        """
        records = []
        n = len(data)
        
        for name in algorithm_names:
            try:
                algo = AlgorithmRegistry.get(name)
                # Clone data so each algorithm receives clean identical array
                test_arr = list(data)
                
                # Execute with timing
                t0 = time.perf_counter()
                trace = algo.execute(test_arr, **kwargs)
                t1 = time.perf_counter()
                
                wall_time_ms = (t1 - t0) * 1000.0
                
                records.append({
                    "Algorithm": algo.name,
                    "Category": algo.category,
                    "Input Size (n)": n,
                    "Comparisons": trace.total_comparisons,
                    "Swaps": trace.total_swaps,
                    "Shifts": trace.total_shifts,
                    "Total Steps": trace.total_steps,
                    "Max Recursion Depth": trace.max_recursion_depth,
                    "Execution Time (ms)": round(wall_time_ms, 3),
                    "Time Complexity (Avg)": algo.time_complexity_average,
                    "Space Complexity": algo.space_complexity,
                    "Stable": algo.is_stable,
                    "In-Place": algo.is_in_place
                })
            except Exception as e:
                records.append({
                    "Algorithm": name,
                    "Category": "Error",
                    "Input Size (n)": n,
                    "Comparisons": 0,
                    "Swaps": 0,
                    "Shifts": 0,
                    "Total Steps": 0,
                    "Max Recursion Depth": 0,
                    "Execution Time (ms)": 0.0,
                    "Time Complexity (Avg)": "N/A",
                    "Space Complexity": "N/A",
                    "Stable": False,
                    "In-Place": False,
                    "Error": str(e)
                })
        
        df = pd.DataFrame(records)
        
        # Add relative ranking columns using Pandas rank
        if not df.empty and "Execution Time (ms)" in df.columns:
            df["Speed Rank"] = df["Execution Time (ms)"].rank(method="min").astype(int)
            df["Comparison Rank"] = df["Comparisons"].rank(method="min").astype(int)
        
        return df

    @staticmethod
    def benchmark_scalability(
        algorithm_names: List[str],
        sizes: List[int] = [10, 20, 50, 100, 200],
        distribution: str = "random",
        runs_per_size: int = 3
    ) -> pd.DataFrame:
        """Benchmark algorithms across varying dataset sizes to empirically demonstrate Big-O growth curves.
        
        Uses Pandas GroupBy and aggregation functions.
        """
        all_runs = []
        
        for size in sizes:
            for run_idx in range(runs_per_size):
                if distribution == "nearly_sorted":
                    dataset = DatasetGenerator.nearly_sorted(size=size, seed=run_idx * 100 + size)
                elif distribution == "reversed":
                    dataset = DatasetGenerator.reversed_sorted(size=size, seed=run_idx * 100 + size)
                elif distribution == "few_unique":
                    dataset = DatasetGenerator.few_unique(size=size, seed=run_idx * 100 + size)
                else:
                    dataset = DatasetGenerator.random(size=size, seed=run_idx * 100 + size)
                
                for name in algorithm_names:
                    try:
                        algo = AlgorithmRegistry.get(name)
                        arr_copy = list(dataset)
                        
                        t0 = time.perf_counter()
                        trace = algo.execute(arr_copy)
                        t1 = time.perf_counter()
                        
                        all_runs.append({
                            "Algorithm": algo.name,
                            "Size": size,
                            "Run": run_idx + 1,
                            "Comparisons": trace.total_comparisons,
                            "Swaps": trace.total_swaps,
                            "Steps": trace.total_steps,
                            "Time_ms": (t1 - t0) * 1000.0
                        })
                    except Exception:
                        continue
        
        raw_df = pd.DataFrame(all_runs)
        if raw_df.empty:
            return raw_df
            
        # GroupBy Algorithm and Size to compute Mean and Std Dev
        summary = raw_df.groupby(["Algorithm", "Size"]).agg(
            Avg_Comparisons=("Comparisons", "mean"),
            Avg_Swaps=("Swaps", "mean"),
            Avg_Steps=("Steps", "mean"),
            Avg_Time_ms=("Time_ms", "mean"),
            Std_Time_ms=("Time_ms", "std")
        ).reset_index()
        
        # Round numeric values for clean UI presentation
        summary["Avg_Comparisons"] = summary["Avg_Comparisons"].round(1)
        summary["Avg_Swaps"] = summary["Avg_Swaps"].round(1)
        summary["Avg_Steps"] = summary["Avg_Steps"].round(1)
        summary["Avg_Time_ms"] = summary["Avg_Time_ms"].round(3)
        summary["Std_Time_ms"] = summary["Std_Time_ms"].fillna(0.0).round(4)
        
        return summary

    @staticmethod
    def generate_pivot_table(benchmark_df: pd.DataFrame, metric: str = "Avg_Comparisons") -> pd.DataFrame:
        """Create a pivot table with Algorithms as rows and Sizes as columns."""
        if benchmark_df.empty or metric not in benchmark_df.columns:
            return pd.DataFrame()
        return benchmark_df.pivot(index="Algorithm", columns="Size", values=metric)
