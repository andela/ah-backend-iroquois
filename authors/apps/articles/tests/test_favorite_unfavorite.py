import json
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

from authors.apps.authentication.models import User
from authors.apps.profiles.tests.base_test import BaseTest
from .test_data import TestData


class TestFavoriteUnfavorite(TestCase, BaseTest, TestData):
    def setUp(self):
        BaseTest.__init__(self)
        self.client = APIClient()
        self.user = User.objects.create_user(self.user_name, self.user_email, self.password)
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()

        self.login_response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.second_user = User.objects.create_user(
            "username_two", "second_email@gmail.com", "password"
        )
        self.second_user = User.objects.get(email="second_email@gmail.com")
        self.second_user.is_active = True
        self.second_user.is_email_verified = True
        self.second_user.save()

        self.login_second = self.client.post("/api/users/login/",data={"user": {
                                                 "email": "second_email@gmail.com",
                                                 "password": "password", }},
                                             format="json")

    def test_favorite_article(self):
        self.client.post("/api/users/login/", self.login_response.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')

        self.client.post("/api/users/login/", self.login_second.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_second.data['token'])
        resp = self.client.get(
            "/api/articles/", content_type='application/json')

        slug = resp.json()['article']['results']['slug']
        self.response = self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.response.json()['favorites_count'], 1)
        self.assertIsInstance(self.response.json()['author']['favorites'], list)

    def test_favorite_article_404(self):
        self.client.post("/api/users/login/", self.login_response.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')

        self.client.post("/api/users/login/", self.login_second.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_second.data['token'])

        self.response = self.client.post('/api/articles/{}/favorite/'.format('hhsdjchsbcnxbshbc'))
        self.assertEqual(self.response.json(), {'detail': 'An article with this slug was not found.'})
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)

    def test_already_favorited(self):

        self.client.post("/api/users/login/", self.login_response.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])

        self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')

        self.client.post("/api/users/login/", self.login_second.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_second.data['token'])
        resp = self.client.get(
            "/api/articles/", content_type='application/json')
        slug = resp.json()['article']['results']['slug']
        self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.response = self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.assertEqual(self.response.json(), {'message': 'You have already favorited this article'})
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_favorite_own_article(self):
        # first user login
        self.client.post("/api/users/login/", self.login_response.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        # first user post article
        self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        resp = self.client.get(
            "/api/articles/", content_type='application/json')
        slug = resp.json()['article']['results']['slug']
        self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.response = self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.assertEqual(self.response.json(), {'error': 'You cannot favorite your own article'})
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_unfavorite_article(self):
        # first user login
        self.client.post("/api/users/login/", self.login_response.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        # first user post article
        self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        # second user login
        self.client.post("/api/users/login/", self.login_second.data, format="json")
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_second.data['token'])
        resp = self.client.get(
            "/api/articles/", content_type='application/json')

        slug = resp.json()['article']['results']['slug']
        self.client.post('/api/articles/{}/favorite/'.format(slug))
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format(slug), content_type='application/json')
        self.assertEqual(self.response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.response.json()['favorites_count'], 0)
        self.assertIsInstance(self.response.json()['author']['favorites'], list)
        self.assertEqual(len(self.response.json()['author']['favorites']), 0)

    def test_unfavorite_article_not_favorited(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_second.data['token'])
        self.client.post("/api/articles/", data=json.dumps(self.post_article), content_type='application/json')
        resp = self.client.get(
            "/api/articles/", content_type='application/json')
        slug = resp.json()['article']['results']['slug']
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format(slug), content_type='application/json')
        self.assertEqual(self.response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(self.response.json(), {'message': 'This article is not in your favorites list'})

    def test_unfavorite_article_404(self):
        self.client.credentials(
            HTTP_AUTHORIZATION='Token ' + self.login_response.data['token'])
        self.response = self.client.delete('/api/articles/{}/unfavorite/'.format('hsdbfjsbjfbjs'), content_type='application/json')
        self.assertEqual(self.response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(self.response.json(), {'detail': 'An article with this slug was not found.'})
