"""This module tests the login and registration of a user."""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.tests.base_test import BaseTest


class RegistrationAPIViewTestCase(TestCase, BaseTest):
    """Test suite for the api views."""

    def setUp(self):
        """Define the test client and other test variables."""
        BaseTest.__init__(self)
        self.client = APIClient()
        self.response = self.client.post(
            "/api/users/",
            self.user_data,
            format="json")

    def test_api_can_register_a_user(self):
        """Test the api can register a user."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_api_can_login_a_user(self):
        """Test the api can login a user."""
        self.response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        """Test a user can not login with invalid details."""
        self.response = self.client.post(
            "/api/users/login/",
            self.invalid_login_data,
            format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_invalid_registration(self):
        """Test a user can not login with invalid details."""
        self.response = self.client.post(
            "/api/users/",
            self.user_data,
            format="json")
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_wrong_email_on_login(self):
        """Test an error is returned when missing an email address in login credentials."""
        self.response = self.client.post(
            "/api/users/login/",
            {"user": {
                "email": 'kake@gmail.com',
                "password": "fakemail",
            }
            },
            format="json")
        self.assertEqual('A user with this email and password was not found.',
                         self.response.json()['errors']['error'][0])
