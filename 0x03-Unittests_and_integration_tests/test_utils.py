#!/usr/bin/env python3
"""Unit tests for utils.py(Task 0)"""

import unittest
from typing import Mapping, Sequence, Any, Dict, Tuple
from parameterized import parameterized
from utils import access_nested_map


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

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
        """It should return the value found by following path"""
        self.assertEqual(access_nested_map(nested_map, path), expected)


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access_nested_map function"""

    @parameterized.expand([
        ( {}, ("a",), "a" ),
        ( {"a": 1}, ("a", "b"), "b" ),
    ])
    def test_access_nested_map_exception(
        self,
        nested_map: Mapping[str, Any],
        path: Sequence[str],
        missing_key: str
    ) -> None:
        """Test that a KeyError is raised for missing key"""
        
        #assertRaises to check that a KeyError is raised
        with self.assertRaises(KeyError) as cm:
            access_nested_map(nested_map, path)

        # Check keyError message is as expected
        self.assertEqual(str(cm.exception), f"'{missing_key}'")



if __name__ == "__main__":
    unittest.main()
