"""
Test articles
"""
import json

import unittest

from rest_framework import status
from rest_framework.test import APIClient

from authors.apps.articles.models import Article
from authors.apps.authentication.models import User
from .test_data import TestData


class Tests(unittest.TestCase, TestData):

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

    def test_post_new_article(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article), content_type='application/json')
        self.assertEqual(201, response.status_code)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_article_slug(self):
        val = 0
        while val < 10:
            response = self.client.post(
                "/api/articles/", data=json.dumps(
                    self.post_article), content_type='application/json')
            self.assertEqual(201, response.status_code)
            self.assertIn('article', response.json())
            self.assertIsInstance(response.json().get("article"), dict)
            val += 1

    def test_post_article_missing_data(self):
        response = self.client.post(
            "/api/articles/", data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('errors', response.json())

    def test_list_zero_article(self):
        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_list_one_article(self):
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

        # test for invalid query params
        response = self.client.get(
            "/api/articles/?offset=3&limit=3e", content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertIn('article', response.json())

    def test_list_specific_article(self):
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

        slug = response.json().get("article").get("slug")

        response = self.client.get(
            "/api/articles/{0}/".format(slug), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_delete_specific_article(self):
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

        slug = response.json().get("article").get("slug")

        response = self.client.delete(
            "/api/articles/{0}/".format(slug), content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertIn('detail', response.data)
        self.assertIsInstance(response.data.get("detail"), str)

    def test_delete_not_found_article(self):
        response = self.client.delete(
            "/api/articles/54/", content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('detail', response.data)
        self.assertIsInstance(response.data.get("detail"), str)

    def test_list_many_articles(self):
        val = 0
        while val < 3:
            response = self.client.post(
                "/api/articles/", data=json.dumps(
                    self.post_article), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertIn('article', response.json())
            self.assertIsInstance(response.json().get("article"), dict)
            val += 1

        response = self.client.get(
            "/api/articles/", content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("articles"), list)
        self.assertEqual(len(response.json().get("articles")), 3)

    def test_update_article(self):
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

        slug = response.json().get("article").get("slug")

        response = self.client.put(
            "/api/articles/{0}/".format(slug), data=json.dumps(
                self.update_article), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

    def test_update_article_missing_data_and_not_exist(self):
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

        slug = response.json().get("article").get("slug")

        response = self.client.put(
            "/api/articles/{0}/".format(slug), data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 202)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)

        # test article does not exist
        response = self.client.put(
            "/api/articles/45/", data=json.dumps(
                self.post_article_missing_data), content_type='application/json')
        self.assertEqual(response.status_code, 404)
        self.assertIn('article', response.json())
        self.assertIsInstance(response.json().get("article"), dict)
