"""This module tests the login and registration of a user."""
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.models import User

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
        self.user = User.objects.get(email=self.user_email)

    def test_api_can_register_a_user(self):
        """Test the api can register a user."""
        self.assertEqual(status.HTTP_201_CREATED, self.response.status_code)
        self.assertIn('message', self.response.data)

    def test_api_can_login_a_user(self):
        """Test the api can login a user."""
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('token', self.response.data)

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
            self.invalid_reg_data,
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

    def test_register_with_invalid_username(self):
        """Test if the username is invalid """
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "&*@#$",
                    "email": 'kakecom@gmail.com',
                    "password": "irquoa12345678",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Invalid Username , it contains invalid characters.',
                         self.response.json()['errors']['error'][0])

    def test_no_password_login(self):
        """Test no password logging in."""
        self.response = self.client.post(
            "/api/users/",
            self.no_password_login,
            format="json")
        self.assertEqual('This field may not be null.',
                         self.response.json()['errors']['password'][0])
        self.assertEqual(self.response.status_code,
                         status.HTTP_400_BAD_REQUEST)

    def test_wrong_email(self):
        """Test if the email is wrong"""
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "Iroqua",
                    "email": 'kakegmailcom',
                    "password": "irquoa12345678",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Enter a valid email address.',
                         self.response.json()['errors']['email'][0])

    def test_password_length(self):

        """Test if the password is alphanumeric """
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "kake",
                    "email": 'kakegmail.com',
                    "password": "12345l",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('Ensure this field has at least 8 characters.',
                         self.response.json()['errors']['password'][0])

    def test_password_not_alphanumeric(self):
        """Test if the password is alphanumeric """
        self.response = self.client.post(
            "/api/users/",
            {"user": {
                "username": "kake",
                "email": 'kakegmail.com',
                "password": "1234456789",
            }
            },
            format="json"
        )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_registration_successful(self):

        """Test if the password length is greater than 8 characters  """
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "kake",
                    "email": 'kake@gmail.com',
                    "password": "123445abcdefghijk",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_no_email_registration(self):

        """Test if the password length is greater than 8 characters  """
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "kake",
                    "email": "",
                    "password": "123445abcdefghijk",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('This field may not be blank.',
                         self.response.json()['errors']['email'][0])

    def test_no_password_registration(self):

        """Test if the password length is greater than 8 characters  """
        self.response = self.client.post(
                "/api/users/",
                {"user": {
                    "username": "kake",
                    "email": "huxy@gmail.com",
                    "password": "",
                }
                },
                format="json"
            )
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual('This field may not be blank.',
                         self.response.json()['errors']['password'][0])
