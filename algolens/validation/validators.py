"""
AlgoLens Input Validation Engine
================================
Regex-based input parsing and validation.
Covers Syllabus Unit on Regular Expressions (`re` module).
Handles comma-separated, space-separated, bracketed array strings,
floating point numbers, negative values, and search targets.
"""

import re
from typing import Union, Tuple, Optional


class ValidationError(ValueError):
    """Raised when user input fails validation."""
    pass


class InputValidator:
    """Provides regex-based parsing and validation for user-entered algorithm data."""
    
    # Matches individual valid numbers: integers and floating point, signed
    NUMBER_PATTERN = re.compile(r'^[+-]?(\d+(\.\d*)?|\.\d+)([eE][+-]?\d+)?$')
    
    # Matches clean comma/space/semicolon separated lists
    DELIMITER_SPLIT_PATTERN = re.compile(r'[,;\s]+')
    
    # Matches bracketed or parenthesized list wrappers: [ ... ] or ( ... ) or { ... }
    BRACKET_CLEAN_PATTERN = re.compile(r'^[\s\[\(\{]+|[\s\]\)\}]+$')
    
    # Matches alphanumeric dataset names with safe characters: letters, numbers, hyphens, underscores
    DATASET_NAME_PATTERN = re.compile(r'^[a-zA-Z0-9_\-\s]{1,50}$')
    
    # Detects disallowed dangerous characters in custom inputs
    INVALID_CHARS_PATTERN = re.compile(r'[^0-9\s,;.\-\+\[\]\(\)]')

    @classmethod
    def parse_array_input(
        cls, 
        raw_text: str, 
        min_elements: int = 1, 
        max_elements: int = 500,
        allow_float: bool = True
    ) -> list[Union[int, float]]:
        """Parse raw text string into a list of numbers using regex.
        
        Supports formats:
        - "45, 12, 85, 32, 89"
        - "45 12 85 32 89"
        - "[45, 12, 85, 32, 89]"
        - "45,12, 85 ; 32"
        - "-15.5, 0, 42, +7.8"
        
        Args:
            raw_text: Raw string entered by the user
            min_elements: Minimum required numbers
            max_elements: Maximum allowed numbers for UI stability
            allow_float: Whether floating point values are accepted
            
        Returns:
            List of parsed numbers (int or float)
            
        Raises:
            ValidationError: With descriptive diagnostic explanation
        """
        if not raw_text or not raw_text.strip():
            raise ValidationError("Input cannot be empty. Please enter a list of numbers.")
        
        text = raw_text.strip()
        
        # Check for illegal characters
        illegal = cls.INVALID_CHARS_PATTERN.findall(text)
        if illegal:
            unique_illegal = sorted(list(set(illegal)))
            raise ValidationError(
                f"Input contains illegal characters: {', '.join(repr(c) for c in unique_illegal)}. "
                "Only numbers, commas, spaces, decimals, and brackets are allowed."
            )
        
        # Strip outer brackets if present
        text = cls.BRACKET_CLEAN_PATTERN.sub('', text).strip()
        if not text:
            raise ValidationError("Input array is empty after stripping bracket delimiters.")
        
        # Tokenize using delimiter pattern
        tokens = [t for t in cls.DELIMITER_SPLIT_PATTERN.split(text) if t]
        
        if len(tokens) < min_elements:
            raise ValidationError(
                f"Array must contain at least {min_elements} element(s). Provided: {len(tokens)}."
            )
        
        if len(tokens) > max_elements:
            raise ValidationError(
                f"Array exceeds maximum allowed size of {max_elements} elements for visual performance. Provided: {len(tokens)}."
            )
        
        parsed_numbers = []
        for index, token in enumerate(tokens):
            if not cls.NUMBER_PATTERN.match(token):
                raise ValidationError(
                    f"Token #{index + 1} '{token}' is not a valid number."
                )
            try:
                if '.' in token or 'e' in token.lower():
                    if not allow_float:
                        raise ValidationError(
                            f"Floating point number '{token}' not allowed for this operation. Integers only."
                        )
                    val = float(token)
                    # Convert to int if exactly whole for cleaner visualization
                    if val.is_integer():
                        val = int(val)
                else:
                    val = int(token)
                parsed_numbers.append(val)
            except ValueError:
                raise ValidationError(f"Unable to parse number '{token}' at position {index + 1}.")
        
        return parsed_numbers

    @classmethod
    def parse_target_value(cls, raw_target: Union[str, int, float]) -> Union[int, float]:
        """Validate and parse a search target value."""
        if raw_target is None:
            raise ValidationError("Search target value cannot be empty.")
            
        target_str = str(raw_target).strip()
        if not target_str:
            raise ValidationError("Search target cannot be empty.")
            
        if not cls.NUMBER_PATTERN.match(target_str):
            raise ValidationError(f"Search target '{target_str}' is not a valid number.")
            
        val = float(target_str)
        if val.is_integer():
            return int(val)
        return val

    @classmethod
    def validate_dataset_name(cls, name: str) -> str:
        """Validate custom dataset name."""
        if not name or not name.strip():
            raise ValidationError("Dataset name cannot be empty.")
        clean_name = name.strip()
        if not cls.DATASET_NAME_PATTERN.match(clean_name):
            raise ValidationError(
                "Dataset name must be 1-50 characters alphanumeric, spaces, hyphens, or underscores only."
            )
        return clean_name
