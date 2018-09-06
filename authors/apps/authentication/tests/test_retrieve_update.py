"""This module tests the retrieve and update of a user."""
from datetime import datetime, timedelta
from django.test import TestCase
from django.conf import settings

from rest_framework.test import APIClient
from rest_framework import status

import jwt


from authors.apps.authentication.models import User
from authors.apps.authentication.tests.base_test import BaseTest


class UserRetrieveUpdateAPIViewTestCase(TestCase, BaseTest):
    """Test suite for the api User retrieve and update."""

    @staticmethod
    def generate_a_token():
        """Generate a token with a non existing user id."""
        expiration_time = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': 7,
            'exp': expiration_time
        }, settings.SECRET_KEY, algorithm='HS256')

        return token.decode('utf-8')

    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.user = User.objects.create_user(
                        self.user_name, self.user_email, self.password)
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post("/api/users/login/",
                                               self.login_data,
                                               format="json")
        self.user_get_response = self.client.get("/api/user/")
        self.user_put_response = self.client.put("/api/user/")


    def test_non_authorized_user_blocked(self):
        """Test the api can block a non authorized"""

        self.assertEqual(self.user_get_response.status_code,
                         status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.user_put_response.status_code,
                         status.HTTP_403_FORBIDDEN)

    def test_invalid_token(self):
        """Test the return of an error when an invalid token is used."""
        self.client.credentials(
            HTTP_AUTHORIZATION='Token vnvnvnvnvnvnnvnvnvnvnvn')
        self.response = self.client.get("/api/user/")
        self.assertEqual('Invalid token. Please log in again.',
                         self.response.data['detail'])

    def test_no_user_found(self):
        """Test the return of an error when no user matching the token was found."""
        non_existing_user_token = UserRetrieveUpdateAPIViewTestCase.generate_a_token()
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + non_existing_user_token)
        self.response = self.client.get("/api/user/")
        self.assertEqual('No user matching this token was found.',
                         self.response.data['detail'])

    def test_a_valid_token_used(self):
        """
        Test the successful use of a token by reaching an endpoint
        which requires a login
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.get("/api/user/")
        self.assertEqual(self.response.status_code,
                         status.HTTP_200_OK)

    def test_one_length_token_provided(self):
        """
        Test that an error is returned when only one word is provided in the
        header. It should be 'Token xxxx'. So if only one is provided, the end
        point cannot be accessed.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token')
        self.response = self.client.get("/api/user/")
        self.assertEqual('Incomplete authentication details provided',
                         self.response.data['detail'])

    def test_more_than_two_length_token_provided(self):
        """
        Test that an error is returned when more than two words are provided in the
        header. It should be 'Token xxxx'. So if more than two is provided, the end
        point cannot be accessed.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token xxxx yyyy')
        self.response = self.client.get("/api/user/")
        self.assertEqual('Excess authentication details provided',
                         self.response.data['detail'])

    def test_wrong_header_prefix_provide(self):
        """
        Test that an error is returned upon using providing a wrong header prefix
        in the credentials. It should be 'Token'. Else an error is returned.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Tokening xxxx')
        self.response = self.client.get("/api/user/")
        self.assertEqual('Unknown header prefix was provided.',
                         self.response.data['detail'])

    def test_a_deactivated_user(self):
        """
        Test the return of an error when a deactivated user tries to
        reach an endpoint that requires authentication.
        """
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.user.is_active = False
        self.user.save()

        self.response = self.client.get("/api/user/")
        self.assertEqual('This user has been deactivated.',
                         self.response.data['detail'])

    # Test update user info
    def test_update_user_password(self):
        """test update user """

        token = self.login_response.data['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        self.update_user = self.client.put("/api/user/",

                                           data={
                                               "user": {
                                                   "username": self.user_name,
                                                   "email": self.user_email,
                                                   "password": self.password
                                               }
                                           }
                                           ,
                                           format="json")
        self.assertEqual(self.update_user.status_code, status.HTTP_200_OK)

