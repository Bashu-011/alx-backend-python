#!/usr/bin/env python3
"""Unit tests for utils.py (Task 0: parameterize access_nested_map)."""

import unittest
from typing import Mapping, Sequence, Any, Dict, Tuple
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function."""

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        expected: Any
    ) -> None:
        """It should return the value found by following the key path."""
        self.assertEqual(access_nested_map(nested_map, path), expected)
        # Body is 1 line of assertion as required.


if __name__ == "__main__":
    unittest.main()
