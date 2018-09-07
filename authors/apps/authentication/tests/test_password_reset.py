"""This module tests the password reset functionality of a user."""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTest
from authors.apps.authentication.models import User


class PasswordResetTestCase(TestCase, BaseTest):
    """ This class defines the test suite for password reset """

    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

        # create a new user
        self.user = User.objects.create_user(
            self.user_name, self.user_email, self.password
        )

        # invoke a password reset email
        self.response = self.client.post("/api/users/reset/password",
                                         self.invoke_email,
                                         format="json")

        # This email is not associated with a user
        self.email_404 = {
            "user": {
                "email": "email_404@none.com"
            }
        }

        # Here we don't pass in an email
        self.empty_email = {
            "user": {
                "email": ""
            }
        }

    def test_invoke_password_reset(self):
        """ Test that password reset email is sent
            The user with this email exists
        """

        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_email_does_not_exist(self):
        """ Test user can not invoke password reset for email that does not exist"""

        self.response = self.client.post(
            "/api/users/reset/password",
            self.email_404,
            format="json"

        )

        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    def test_with_no_email(self):
        """ Test a user can not invoke password reset with no email """

        self.response = self.client.post(
            "/api/users/reset/password",
            self.empty_email,
            format="json"
        )

        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(self.response.json()['errors'],
                         {'email': ['This field may not be blank.']})

