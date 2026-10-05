"""
AlgoLens Data Handlers
======================
Comprehensive file input/output handlers covering:
- CSV (csv module and pandas)
- JSON (json module)
- XML (xml.etree.ElementTree)
- Plain Text (TXT)
- Binary Serialization (pickle / struct)
- Trace Export (JSON, CSV summary)

Demonstrates Syllabus Unit on File Handling, Serialization, and Data Formats.
"""

import os
import csv
import json
import pickle
import xml.etree.ElementTree as ET
from typing import Union, List, Dict, Any, Optional
import pandas as pd

from algolens.validation.validators import InputValidator, ValidationError


class FileHandlerError(Exception):
    """Base exception for file handler operations."""
    pass


class DataFileHandler:
    """Universal file import/export handler for AlgoLens."""
    
    @staticmethod
    def load_from_csv(filepath_or_buffer) -> List[Union[int, float]]:
        """Load numerical array from CSV file or StringIO buffer."""
        try:
            if hasattr(filepath_or_buffer, 'read'):
                # Handle file-like objects (e.g. Streamlit UploadedFile)
                content = filepath_or_buffer.getvalue().decode('utf-8')
                # Read via csv reader to strip potential header
                reader = csv.reader(content.splitlines())
                values = []
                for row in reader:
                    for cell in row:
                        cell_clean = cell.strip()
                        if cell_clean and InputValidator.NUMBER_PATTERN.match(cell_clean):
                            values.append(cell_clean)
                if not values:
                    raise ValidationError("No numeric values found in CSV.")
                return InputValidator.parse_array_input(",".join(values))
            
            with open(filepath_or_buffer, mode='r', encoding='utf-8') as f:
                reader = csv.reader(f)
                values = []
                for row in reader:
                    for cell in row:
                        cell_clean = cell.strip()
                        if cell_clean and InputValidator.NUMBER_PATTERN.match(cell_clean):
                            values.append(cell_clean)
                if not values:
                    raise ValidationError("No numeric values found in CSV.")
                return InputValidator.parse_array_input(",".join(values))
        except Exception as e:
            raise FileHandlerError(f"Error reading CSV: {str(e)}")

    @staticmethod
    def save_to_csv(data: List[Union[int, float]], filepath: str, header: Optional[str] = "value") -> str:
        """Export numerical array to CSV file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            with open(filepath, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                if header:
                    writer.writerow([header])
                for item in data:
                    writer.writerow([item])
            return filepath
        except Exception as e:
            raise FileHandlerError(f"Error writing CSV: {str(e)}")

    @staticmethod
    def load_from_json(filepath_or_buffer) -> List[Union[int, float]]:
        """Load numerical array from JSON file."""
        try:
            if hasattr(filepath_or_buffer, 'read'):
                content = filepath_or_buffer.getvalue().decode('utf-8')
                raw = json.loads(content)
            else:
                with open(filepath_or_buffer, mode='r', encoding='utf-8') as f:
                    raw = json.load(f)
            
            if isinstance(raw, list):
                return [int(x) if isinstance(x, (int, float)) and x == int(x) else float(x) for x in raw]
            elif isinstance(raw, dict) and "data" in raw and isinstance(raw["data"], list):
                return [int(x) if isinstance(x, (int, float)) and x == int(x) else float(x) for x in raw["data"]]
            else:
                raise ValidationError("JSON file must contain a top-level list of numbers or a 'data' array.")
        except Exception as e:
            raise FileHandlerError(f"Error reading JSON: {str(e)}")

    @staticmethod
    def save_to_json(data: Any, filepath: str, indent: int = 2) -> str:
        """Export data or trace to JSON file."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            with open(filepath, mode='w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, default=str)
            return filepath
        except Exception as e:
            raise FileHandlerError(f"Error writing JSON: {str(e)}")

    @staticmethod
    def load_from_xml(filepath_or_buffer) -> List[Union[int, float]]:
        """Load numerical array from XML format."""
        try:
            if hasattr(filepath_or_buffer, 'read'):
                content = filepath_or_buffer.getvalue().decode('utf-8')
                root = ET.fromstring(content)
            else:
                tree = ET.parse(filepath_or_buffer)
                root = tree.getroot()
            
            values = []
            for elem in root.iter():
                text = (elem.text or '').strip()
                if text and elem != root:
                    # Try parsing numbers
                    try:
                        val = float(text)
                        values.append(int(val) if val.is_integer() else val)
                    except ValueError:
                        continue
            
            if not values:
                raise ValidationError("No numeric elements found in XML structure.")
            return values
        except Exception as e:
            raise FileHandlerError(f"Error reading XML: {str(e)}")

    @staticmethod
    def save_to_xml(data: List[Union[int, float]], filepath: str, root_tag: str = "dataset") -> str:
        """Export numerical array to formatted XML."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            root = ET.Element(root_tag)
            for idx, val in enumerate(data):
                elem = ET.SubElement(root, "element", index=str(idx))
                elem.text = str(val)
            tree = ET.ElementTree(root)
            tree.write(filepath, encoding='utf-8', xml_declaration=True)
            return filepath
        except Exception as e:
            raise FileHandlerError(f"Error writing XML: {str(e)}")

    @staticmethod
    def load_from_txt(filepath_or_buffer) -> List[Union[int, float]]:
        """Load numbers from plain text."""
        try:
            if hasattr(filepath_or_buffer, 'read'):
                content = filepath_or_buffer.getvalue().decode('utf-8')
            else:
                with open(filepath_or_buffer, mode='r', encoding='utf-8') as f:
                    content = f.read()
            return InputValidator.parse_array_input(content)
        except Exception as e:
            raise FileHandlerError(f"Error reading TXT: {str(e)}")

    @staticmethod
    def save_to_txt(data: List[Union[int, float]], filepath: str, delimiter: str = ", ") -> str:
        """Export numbers to plain text."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            with open(filepath, mode='w', encoding='utf-8') as f:
                f.write(delimiter.join(str(x) for x in data))
            return filepath
        except Exception as e:
            raise FileHandlerError(f"Error writing TXT: {str(e)}")

    @staticmethod
    def save_binary(data: Any, filepath: str) -> str:
        """Binary serialization using pickle (covers Python binary I/O)."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        try:
            with open(filepath, mode='wb') as f:
                pickle.dump(data, f)
            return filepath
        except Exception as e:
            raise FileHandlerError(f"Error saving binary: {str(e)}")

    @staticmethod
    def load_binary(filepath_or_buffer) -> Any:
        """Binary deserialization using pickle."""
        try:
            if hasattr(filepath_or_buffer, 'read'):
                return pickle.loads(filepath_or_buffer.getvalue())
            with open(filepath_or_buffer, mode='rb') as f:
                return pickle.load(f)
        except Exception as e:
            raise FileHandlerError(f"Error reading binary: {str(e)}")

    @classmethod
    def export_trace_summary_csv(cls, trace_summary_data: List[Dict[str, Any]], filepath: str) -> str:
        """Export algorithm execution trace comparisons to CSV using pandas."""
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        df = pd.DataFrame(trace_summary_data)
        df.to_csv(filepath, index=False)
        return filepath
