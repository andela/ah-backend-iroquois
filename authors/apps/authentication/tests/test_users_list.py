"""
This module tests UsersListAPIView.
"""

from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTest
from authors.apps.authentication.models import User


class UsersListAPIViewTestCase(TestCase, BaseTest):
    """
    Test suite for the return of a list of 
    users and thier profiles.
    """

    def setUp(self):
        """Define the test client."""
        BaseTest.__init__(self)
        self.client = APIClient()
        self.user = User.objects.create_user(
            self.user_name, self.user_email, self.password)
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")

    def test_users_profile_list_return(self):
        """
        Test the successful return of a list of users
        with their profiles.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.get("/api/users/users_list/")
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertIn('users', self.response.data)

    def test_unauthenticated_user_denial(self):
        """
        Test that unauthenticated user can not access the endpoint.
        """

        self.response = self.client.get("/api/users/users_list/")
        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            'Authentication credentials were not provided.', self.response.data['detail'])
