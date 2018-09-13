from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status
from authors.apps.authentication.tests.base_test import BaseTest
from authors.apps.authentication.models import User
from authors.apps.profiles.models import UserProfile
from .base_test import BaseTest


class TestProfile(TestCase, BaseTest):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()

        # create a new user
        self.user = User.objects.create_user(
            self.user_name, self.user_email, self.password
        )
        self.bio = "That's me"
        self.location = "kampala-uganda"
        self.first_name = "first_name"
        self.last_name = "last_name"
        self.profile_data = {
                    "profile": {
                              "username": self.user_name,
                              "email": self.user_email,
                              "password": self.password,
                              "first_name": self.first_name,
                              "last_name": self.last_name,
                              "location": self.location,
                              "bio": self.bio


                            }

                }
        self.llist_profile = {
                    "profile": {
                              "username": "",
                              "email": self.user_email,
                              "password": self.password,
                              "first_name": self.first_name,
                              "last_name": self.last_name,
                              "location": self.location,
                              "bio": self.bio


                            }

                }

    def test_profile_created(self):
        """Test the api can login a user."""

        self.get_profile = UserProfile.objects.get(
                user__username=self.user_name
            )

        self.queryset = UserProfile.objects.all()

        self.assertEqual(len(self.queryset), 1)

        self.assertEqual(self.get_profile.__str__(), None)

    def test_retrieve_profile(self):
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.fetch_profile_response = self.client.get("/api/profile/{}/".format(self.user_name))

        self.assertEqual(self.fetch_profile_response.status_code,
                         status.HTTP_200_OK)

        # default profile after registration
        self.assertEqual(self.fetch_profile_response.json(),
                         {'profile': {'bio': None,
                                      'first_name': None,
                                      'last_name': None,
                                      'location': None,
                                      'username': self.user_name}}
                         )

    def test_update_profile(self):
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.fetch_profile_response = self.client.put("/api/user/update/profile/",
                                                      data=self.profile_data,
                                                      format='json')

        self.assertEqual(self.fetch_profile_response.status_code,
                         status.HTTP_200_OK)

        self.assertEqual(self.fetch_profile_response.json(),
                         {"profile": {'bio': self.bio,
                                      'first_name': self.first_name,
                                      'last_name': self.last_name,
                                      'location': self.location,
                                      'username': self.user_name}}
                         )

    def test_update_with_existing_username(self):

        self.response = self.client.post("/api/users/",
                                         data=self.second_user,
                                         format='json')

        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.fetch_profile_response = self.client.put("/api/user/update/profile/",
                                                      data={
                                                          "profile": {
                                                            'bio': self.bio,
                                                            'first_name': self.first_name,
                                                            'last_name': self.last_name,
                                                            'location': self.location,
                                                            'username': "second_user"
                                                      }
                                                      },
                                                      format='json')

        self.assertEqual(self.fetch_profile_response.status_code,
                         status.HTTP_400_BAD_REQUEST)

        self.assertEqual(self.fetch_profile_response.json(),
                         {"profile": {"error": "Username or email already exist, recheck and try again"}})

    def test_profile_username_404(self):
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")

        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.profile_response_404 = self.client.get("/api/profile/{}/".format("username_404"))

        self.assertEqual(self.profile_response_404.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.profile_response_404.json(),
                         {'profile': {'detail': 'The requested profile does not exist'}})









