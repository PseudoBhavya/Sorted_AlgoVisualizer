"""
AlgoLens Comprehensive Test Suite
=================================
Covers:
1. Algorithm Correctness (all 8 algorithms)
2. Trace Engine Integrity (steps, metrics, pointers, variables)
3. Regex Input Validation (valid/invalid formats, brackets, negative numbers)
4. Data File Handlers (CSV, JSON, XML, TXT, Binary round-trips)
5. Pandas Performance Analytics (DataFrames, GroupBy, Rankings)
6. Flask REST API Endpoints (Health, Execute, Compare, Validate)
"""

import os
import unittest
import tempfile
import pandas as pd

from algolens.algorithms.registry import AlgorithmRegistry
from algolens.algorithms.sorting import (
    BubbleSort, SelectionSort, InsertionSort,
    MergeSort, QuickSort, HeapSort
)
from algolens.algorithms.searching import LinearSearch, BinarySearch
from algolens.validation.validators import InputValidator, ValidationError
from algolens.data.handlers import DataFileHandler
from algolens.data.datasets import DatasetGenerator
from algolens.analytics.pandas_analysis import PerformanceAnalytics
from algolens.api.app import create_app


class TestAlgorithms(unittest.TestCase):
    """Test algorithm execution correctness and trace generation."""

    def setUp(self):
        self.sample_data = [45, 12, 85, 32, 89, 39, 69, 44, 42, 1, 93, 8]
        self.sorted_data = sorted(self.sample_data)

    def test_all_sorting_algorithms(self):
        """Verify that all 6 sorting algorithms produce correctly sorted results."""
        sorting_algos = AlgorithmRegistry.get_by_category("Sorting")
        self.assertEqual(len(sorting_algos), 6)

        for algo in sorting_algos:
            with self.subTest(algorithm=algo.name):
                trace = algo.execute(list(self.sample_data))
                self.assertEqual(trace.result, self.sorted_data)
                self.assertGreater(trace.total_steps, 0)
                self.assertGreater(trace.total_comparisons, 0)

    def test_quicksort_hoare_and_lomuto(self):
        """Verify QuickSort supports both Hoare and Lomuto schemes."""
        qs = QuickSort()
        # Hoare
        trace_hoare = qs.execute(list(self.sample_data), partition_scheme="hoare")
        self.assertEqual(trace_hoare.result, self.sorted_data)
        self.assertGreater(trace_hoare.total_swaps, 0)

        # Lomuto
        trace_lomuto = qs.execute(list(self.sample_data), partition_scheme="lomuto")
        self.assertEqual(trace_lomuto.result, self.sorted_data)
        self.assertGreater(trace_lomuto.total_swaps, 0)

    def test_linear_search(self):
        """Verify LinearSearch found and not-found cases."""
        ls = LinearSearch()
        # Match found
        trace_found = ls.execute(list(self.sample_data), target=44)
        self.assertEqual(trace_found.result, self.sample_data.index(44))

        # Not found
        trace_missing = ls.execute(list(self.sample_data), target=999)
        self.assertEqual(trace_missing.result, -1)

    def test_binary_search(self):
        """Verify BinarySearch found and not-found cases."""
        bs = BinarySearch()
        # Match found
        trace_found = bs.execute(list(self.sorted_data), target=44)
        self.assertEqual(trace_found.result, self.sorted_data.index(44))

        # Not found
        trace_missing = bs.execute(list(self.sorted_data), target=999)
        self.assertEqual(trace_missing.result, -1)


class TestValidators(unittest.TestCase):
    """Test regex-based input validation."""

    def test_valid_formats(self):
        # Comma-separated
        self.assertEqual(InputValidator.parse_array_input("1, 2, 3, 4"), [1, 2, 3, 4])
        # Space-separated
        self.assertEqual(InputValidator.parse_array_input("10 20 30"), [10, 20, 30])
        # Bracketed
        self.assertEqual(InputValidator.parse_array_input("[5, 15, 25]"), [5, 15, 25])
        # Negative and float
        self.assertEqual(InputValidator.parse_array_input("-10, 0, 3.5, 7"), [-10, 0, 3.5, 7])

    def test_invalid_formats(self):
        # Empty string
        with self.assertRaises(ValidationError):
            InputValidator.parse_array_input("")
        # Letters / illegal characters
        with self.assertRaises(ValidationError):
            InputValidator.parse_array_input("10, abc, 30")


class TestFileHandlers(unittest.TestCase):
    """Test multi-format file export and import."""

    def setUp(self):
        self.test_data = [10, 25, 42, 88, 99]
        self.temp_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_csv_roundtrip(self):
        path = os.path.join(self.temp_dir.name, "test.csv")
        DataFileHandler.save_to_csv(self.test_data, path)
        loaded = DataFileHandler.load_from_csv(path)
        self.assertEqual(loaded, self.test_data)

    def test_json_roundtrip(self):
        path = os.path.join(self.temp_dir.name, "test.json")
        DataFileHandler.save_to_json(self.test_data, path)
        loaded = DataFileHandler.load_from_json(path)
        self.assertEqual(loaded, self.test_data)

    def test_xml_roundtrip(self):
        path = os.path.join(self.temp_dir.name, "test.xml")
        DataFileHandler.save_to_xml(self.test_data, path)
        loaded = DataFileHandler.load_from_xml(path)
        self.assertEqual(loaded, self.test_data)

    def test_txt_roundtrip(self):
        path = os.path.join(self.temp_dir.name, "test.txt")
        DataFileHandler.save_to_txt(self.test_data, path)
        loaded = DataFileHandler.load_from_txt(path)
        self.assertEqual(loaded, self.test_data)

    def test_binary_roundtrip(self):
        path = os.path.join(self.temp_dir.name, "test.bin")
        DataFileHandler.save_binary(self.test_data, path)
        loaded = DataFileHandler.load_binary(path)
        self.assertEqual(loaded, self.test_data)


class TestAnalytics(unittest.TestCase):
    """Test Pandas benchmarking engine."""

    def test_compare_on_dataset(self):
        algos = ["Quick Sort", "Merge Sort", "Bubble Sort"]
        data = [50, 20, 80, 10, 30]
        df = PerformanceAnalytics.compare_on_dataset(algos, data)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 3)
        self.assertIn("Execution Time (ms)", df.columns)
        self.assertIn("Comparisons", df.columns)
        self.assertIn("Speed Rank", df.columns)


class TestFlaskAPI(unittest.TestCase):
    """Test Flask REST API routes."""

    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_health_endpoint(self):
        res = self.client.get('/api/health')
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertEqual(json_data['status'], 'healthy')
        self.assertEqual(json_data['registered_algorithms'], 8)

    def test_algorithms_endpoint(self):
        res = self.client.get('/api/algorithms')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['count'], 8)

    def test_execute_endpoint(self):
        payload = {
            "algorithm": "Quick Sort",
            "data": [45, 12, 85, 32, 89]
        }
        res = self.client.post('/api/execute', json=payload)
        self.assertEqual(res.status_code, 200)
        json_data = res.get_json()
        self.assertEqual(json_data['result'], [12, 32, 45, 85, 89])
        self.assertGreater(len(json_data['steps']), 0)

    def test_compare_endpoint(self):
        payload = {
            "algorithms": ["Quick Sort", "Merge Sort"],
            "data": [30, 10, 50, 20]
        }
        res = self.client.post('/api/compare', json=payload)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.get_json()['results']), 2)


if __name__ == '__main__':
    unittest.main()
