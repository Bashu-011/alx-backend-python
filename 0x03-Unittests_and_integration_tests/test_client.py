#!/usr/bin/env python3


import unittest
from typing import Mapping, Sequence, Any, Dict, Tuple
from parameterized import parameterized
from unittest.mock import patch, MagicMock
from utils import get_json
from utils import access_nested_map
from utils import memoize
from client import GithubOrgClient


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
