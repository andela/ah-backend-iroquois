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

    def test_wrong_token_on_confirm_registration(self):
        self.user1 = User.objects.get(email=self.user_email)
        self.uid = force_text(urlsafe_base64_encode(self.user1.email.encode("utf8")))
        self.response = self.client.get(
            "/api/users/activate_account/{}/gfgcgffdxfd/".format(self.uid),
            format="json")
        self.assertEqual(403, self.response.status_code)
        self.assertEqual('Invalid token. Please log in again.',
                         self.response.json()['detail'])

    def test_correct_token_on_confirm_registration(self):
        self.user1 = User.objects.get(email=self.user_email)
        self.uid = force_text(urlsafe_base64_encode(self.user1.email.encode("utf8")))
        self.token = self.user1.token
        self.response = self.client.get(
            "/api/users/activate_account/{}/{}/".format(self.uid, self.token),
            format="json")
        self.assertEqual(200, self.response.status_code)
        self.assertEqual('Email verified, continue to login',
                         self.response.json()['message'])
        self.response = self.client.get(
            "/api/users/activate_account/{}/{}/".format(self.uid, self.token),
            format="json")
        self.assertEqual('Email is already verified, continue to login',
                         self.response.json()['message'])

    def test_api_Doesnt_login_an_unverified_user(self):
        """Test the api can login a user."""
        self.user.is_active = True
        self.user.is_email_verified = False
        self.user.save()
        self.response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.assertEqual(status.HTTP_400_BAD_REQUEST, self.response.status_code)
        self.assertEqual('An account with this email is not verified.',
                         self.response.json()['errors']['error'][0])

    def test_invalid_activation_link(self):
        self.user1 = User.objects.get(email=self.user_email)
        self.token = self.user1.token
        self.response = self.client.get(
            "/api/users/activate_account/fcfcfcafd/{}/".format(self.token),
            format="json")
        self.assertIn('error', self.response.data)


