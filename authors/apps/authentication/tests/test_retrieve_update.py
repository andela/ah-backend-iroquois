"""This module tests the retrieve and update of a user."""
from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_test import BaseTest


class UserRetrieveUpdateAPIViewTestCase(TestCase, BaseTest):
    """Test suite for the api User retrieve and update."""

    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.user = User.objects.create_user(
            self.user_name, self.user_email, self.password)
        self.client.post("/api/users/login/",
                         self.login_data,
                         format="json")
        self.response = self.client.get("/api/user/")
        self.resp = self.client.put("/api/user/")

    def test_non_authorized_user_blocked(self):
        """Test the api can block a non authorized"""

        self.assertEqual(self.response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.resp.status_code, status.HTTP_403_FORBIDDEN)
