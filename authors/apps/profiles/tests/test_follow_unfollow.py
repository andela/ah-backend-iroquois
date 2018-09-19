from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.profiles.tests.base_test import BaseTest


class TestFollowUnfollow(TestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        # create a new user
        self.user = User.objects.create_user(self.user_name, self.user_email, self.password)
        # activate user account and login
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        # create second user
        self.second_user = User.objects.create_user('second_user', 'second@exists.com', self.password)
        # activate user account and login
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

    def test_follow_user(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.post('/api/profile/{}/follow/'.format(self.second_user.username))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_follow_self(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.post('/api/profile/{}/follow/'.format(self.user.username))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_follow_user_404(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.post('/api/profile/{}/follow/'.format('non-user'))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_following(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.client.post('/api/profile/{}/follow/'.format(self.second_user.username))
        self.response = self.client.post('/api/profile/{}/follow/'.format(self.second_user.username))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user(self):

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.client.post('/api/profile/{}/follow/'.format(self.second_user.username))
        self.response = self.client.delete('/api/profile/{}/unfollow/'.format(self.second_user.username))
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)

    def test_unfollow_user_not_followed(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.delete('/api/profile/{}/unfollow/'.format(self.second_user.username))
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfollow_user_404(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.delete('/api/profile/{}/unfollow/'.format('non-user'))
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.response.json(), {'detail': 'Profile with this username was not found.'})
