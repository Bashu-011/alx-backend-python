#!/usr/bin/env python3
"""
Unit tests for client.py's GithubOrgClient class.

This module contains unit tests for:
- GithubOrgClient.org
- GithubOrgClient._public_repos_url
- GithubOrgClient.public_repos
"""

import unittest
from unittest.mock import Mock, patch, PropertyMock
from parameterized import parameterized, parameterized_class

from client import TEST_PAYLOAD, GithubOrgClient


@parameterized_class(
    ("org_payload", "repos_payload", "expected_repos", "apache2_repos"),
    TEST_PAYLOAD,
)
class TestGithubOrgClient(unittest.TestCase):
    """Unit tests for the GithubOrgClient class"""

    @parameterized.expand([
        ("google",),
        ("abc",),
    ])
    @patch("client.get_json")
    def test_org(self, org_name, mock_get_json):
        """Test that GithubOrgClient.org returns the correct value"""
        expected_payload = {"login": org_name}
        mock_get_json.return_value = expected_payload

        client = GithubOrgClient(org_name)
        self.assertEqual(client.org, expected_payload)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    def test_public_repos_url(self):
        """Test that _public_repos_url returns the right URL"""
        expected_url = "https://api.github.com/orgs/google/repos"
        with patch(
            "client.GithubOrgClient.org",
            new_callable=PropertyMock,
        ) as mock_org:
            mock_org.return_value = {"repos_url": expected_url}
            client = GithubOrgClient("google")
            self.assertEqual(client._public_repos_url, expected_url)

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False),
    ])
    def test_has_license(self, repo, license_key, expected):
        """Test GithubOrgClient.has_license method with different licenses"""
        self.assertEqual(
            GithubOrgClient.has_license(repo, license_key),
            expected,
        )

    @classmethod
    def setUpClass(cls):
        """Mock requests.get"""
        cls.get_patcher = patch("client.requests.get")
        cls.mock_get = cls.get_patcher.start()

        # Define a side_effect function to return different URLs
        def get_side_effect(url, *args, **kwargs):
            mock_resp = Mock()
            if url == cls.org_payload["repos_url"]:
                mock_resp.json.return_value = cls.repos_payload
            else:
                mock_resp.json.return_value = {}
            return mock_resp

        cls.mock_get.side_effect = get_side_effect

    @classmethod
    def tearDownClass(cls):
        """Stop patching requests.get"""
        cls.get_patcher.stop()

    def test_public_repos(self):
        """Test that public_repos returns the correct repo names"""
        client = GithubOrgClient("google")
        repos = client.public_repos()
        self.assertEqual(repos, self.expected_repos)

    def test_public_repos_with_license(self):
        """Filtering repositories by license"""
        client = GithubOrgClient("google")
        repos = client.public_repos(license="apache-2.0")
        self.assertEqual(repos, self.apache2_repos)
