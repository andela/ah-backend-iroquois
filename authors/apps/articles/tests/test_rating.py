"""
test article rating
"""
import json

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article, Rating
from authors.apps.articles.tests.test_data import TestData
from authors.apps.authentication.models import User


class Tests(TestCase, TestData):
    """
    tests for ratings
    """
    out_of_range_score = {
        "article": {"score": 7}
    }

    in_range_score = {
        "article": {"score": 3}
    }

    def setUp(self):
        """
        setup tests
        """
        User.objects.all().delete()
        Article.objects.all().delete()
        Rating.objects.all().delete()

        self.login_data = {"user": {"email": self.user_email, "password": self.password,
                                    }
                           }
        self.user_data = {"user": {"username": self.user_name, "email": self.user_email,
                                   "password": self.password,
                                   }
                          }
        self.client = APIClient()

        self.response = self.client.post(
            "/api/users/",
            self.user_data,
            format="json")
        self.user = User.objects.get(email=self.user_email)
        self.user.is_active = True
        self.user.is_email_verified = True
        self.user.save()
        self.response = self.client.post(
            "/api/users/login/",
            self.login_data,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('token', self.response.data)
        token = self.response.data.get("token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

    def test_rate_your_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_rate_another_persons_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        self.response = self.client.post(
            "/api/social/auth/google/",
            self.google_debug_token,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('auth_token', self.response.data)
        token = self.response.data.get("auth_token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), data=json.dumps(self.in_range_score),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())

    def test_rate_another_persons_article_with_out_of_range_score(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        self.response = self.client.post(
            "/api/social/auth/google/",
            self.google_debug_token,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('auth_token', self.response.data)
        token = self.response.data.get("auth_token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), data=json.dumps(self.out_of_range_score),
            content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_rate_article_not_found(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        self.response = self.client.post(
            "/api/social/auth/google/",
            self.google_debug_token,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('auth_token', self.response.data)
        token = self.response.data.get("auth_token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug") + "-san"

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), data=json.dumps(self.in_range_score),
            content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('article', response.json())

    def test_rate_article_that_has_been_rated(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        self.response = self.client.post(
            "/api/social/auth/google/",
            self.google_debug_token,
            format="json")
        self.assertEqual(status.HTTP_200_OK, self.response.status_code)
        self.assertIn('auth_token', self.response.data)
        token = self.response.data.get("auth_token", None)
        self.client.credentials(HTTP_AUTHORIZATION="Token {0}".format(token))

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        slug = response.json().get("article").get("results").get("slug")

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), data=json.dumps(self.in_range_score),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())

        response = self.client.post(
            "/api/articles/{0}/rate/".format(slug), data=json.dumps(self.in_range_score),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
