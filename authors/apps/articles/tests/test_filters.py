"""
tests for search filters
"""
import json
from urllib.parse import quote

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.articles.tests.test_data import TestData
from authors.apps.authentication.models import User


class Tests(TestCase, TestData):

    def setUp(self):
        """
        setup tests
        """
        User.objects.all().delete()
        Article.objects.all().delete()

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

    def test_searching_with_all_params(self):
        val = 0
        while val < 10:
            response = self.client.post(
                "/api/articles/", data=json.dumps(
                    self.post_article_tags), content_type='application/json')
            self.assertEqual(201, response.status_code)
            self.assertIn('article', response.json())
            self.assertIsInstance(response.json().get("article"), dict)
            val += 1

        response = self.client.get(
            "/api/articles/?author=iroq", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())
        self.assertIn('results', response.json().get("articles"))

        response = self.client.get(
            "/api/articles/?author=iroq&title={0}&tag=python".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())

        response = self.client.get(
            "/api/articles/?author=iroq&title={0}&tag=python".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())

        response = self.client.get(
            "/api/articles/?author=iroq&tag=python",
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())

        response = self.client.get(
            "/api/articles/?title={0}&tag=python".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())

        response = self.client.get(
            "/api/articles/?title={0}&author=iroq".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())

        response = self.client.get(
            "/api/articles/?author=iroq".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())

        response = self.client.get(
            "/api/articles/?title={0}".format(quote('Yet another Sand Blog')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())

        response = self.client.get(
            "/api/articles/?tag=python".format(quote('Yet another Sand Blogs')),
            content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('articles', response.json())
