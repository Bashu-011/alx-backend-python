#!/usr/bin/env python3
"""Unit tests for utils.py(Task 0)"""

import unittest
from typing import Mapping, Sequence, Any, Dict, Tuple
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from utils import get_json
from utils import access_nested_map
from utils import memoize
from client import GithubOrgClient


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


class TestGetJson(unittest.TestCase):
    """Tests for the get_json()"""

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')  #mocking the request
    def test_get_json(self, test_url: str, test_payload: dict, mock_get: MagicMock) -> None:
        """Test that get_json returns the expected result without making an actual HTTP call."""

        #create a mock json
        mock_response = MagicMock()
        mock_response.json.return_value = test_payload

        #return mock responses
        mock_get.return_value = mock_response

        #use the getJson func
        result = get_json(test_url)

        #ensure that the mock is called only once
        mock_get.assert_called_once_with(test_url)

        #result is the same as the payload
        self.assertEqual(result, test_payload)


class TestMemoize(unittest.TestCase):
    """Testing the memoize decorator"""

    @patch.object(object, 'a_method', return_value=42)  #mocking a_methos
    def test_memoize(self, mock_a_method):
        """Test that a_method is called once when a_property accessed mulitiple times"""

        #test class that uses memoize property
        class TestClass:
            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()

        #test class instance
        test_object = TestClass()

        #call property to test above
        result_1 = test_object.a_property
        result_2 = test_object.a_property

        #checkthat method is called once
        mock_a_method.assert_called_once()

        #assert that both results are the same
        self.assertEqual(result_1, result_2)


class TestGithubOrgClient(unittest.TestCase):
    """Tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")  #get_json function
    def test_org(self, org_name, mock_get_json):
        """Test that the org method returns the correct value and calls get_json once"""

        #define the expected payload
        test_payload = {"repos_url": f"https://api.github.com/orgs/{org_name}/repos"}

        #configure the mock to return the payload
        mock_get_json.return_value = test_payload

        #instansiate githubOrgclient
        client = GithubOrgClient(org_name)

        #call the org method
        result = client.org()

        #check get_json() is called once
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

        #assert the result
        self.assertEqual(result, test_payload)



if __name__ == "__main__":
    unittest.main()

