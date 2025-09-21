#!/usr/bin/env python3


import unittest
from typing import Mapping, Sequence, Any, Dict, Tuple
from parameterized import parameterized
from unittest.mock import PropertyMock, patch, MagicMock
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

    
    def test_public_repos_url(self):
        """
        Test that _public_repos_url will return the correct URL
        based on the mocked property.
        """
        #fake payload for the property
        test_payload = {"repos_url": "https://api.github.com/orgs/google/repos"}

        #patch the org property
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = test_payload

            client = GithubOrgClient("google")
            result = client._public_repos_url

            #assert that they are matching
            self.assertEqual(result, test_payload["repos_url"])


    @patch("client.get_json")
    def test_public_repos(self, mock_get_json):
        """Test that public_repos returns the expected list"""
        fake_payload = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
        ]
        mock_get_json.return_value = fake_payload

        expected_repos = ["repo1", "repo2"]

        with patch(
            "client.GithubOrgClient._public_repos_url",
            new_callable=PropertyMock,
        ) as mock_repos_url:
            mock_repos_url.return_value = "https://api.github.com/orgs/test-org/repos"

            client = GithubOrgClient("test-org")
            result = client.public_repos()

            #assert and ensure that they match
            self.assertEqual(result, expected_repos)

            #assert the mocks that are called once
            mock_repos_url.assert_called_once()
            mock_get_json.assert_called_once_with(
                "https://api.github.com/orgs/test-org/repos"
            )

